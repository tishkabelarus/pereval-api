from flask import Blueprint, request, jsonify
from app.models.database import db_manager

pereval_bp = Blueprint('pereval', __name__)

@pereval_bp.route('/submitData', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 400,
                'message': 'Empty request body',
                'id': None
            }), 400
        
        # Простая валидация
        required_fields = ['beautyTitle', 'title', 'coords', 'level', 'user']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 400,
                    'message': f'Missing required field: {field}',
                    'id': None
                }), 400
        
        result = db_manager.add_pereval(data)
        
        return jsonify({
            'status': result['status'],
            'message': result['message'],
            'id': result['id']
        }), result['status']
            
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Internal server error: {str(e)}',
            'id': None
        }), 500

@pereval_bp.route('/submitData/<int:pereval_id>', methods=['GET'])
def get_pereval(pereval_id):
    """Получение одной записи по ID"""
    try:
        pereval = db_manager.get_pereval(pereval_id)
        
        if not pereval:
            return jsonify({
                'status': 404,
                'message': 'Pereval not found',
                'data': None
            }), 404
        
        return jsonify({
            'status': 200,
            'message': 'Success',
            'data': pereval
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Internal server error: {str(e)}',
            'data': None
        }), 500

@pereval_bp.route('/submitData/<int:pereval_id>', methods=['PATCH'])
def update_pereval(pereval_id):
    """Редактирование существующей записи"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'state': 0,
                'message': 'Empty request body'
            }), 400
        
        result = db_manager.update_pereval(pereval_id, data)
        
        if result['state'] == 1:
            return jsonify({
                'state': 1,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'state': 0,
                'message': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'state': 0,
            'message': f'Internal server error: {str(e)}'
        }), 500

@pereval_bp.route('/submitData/', methods=['GET'])
def get_user_pereval():
    """Получение всех записей пользователя по email"""
    try:
        user_email = request.args.get('user__email')
        
        if not user_email:
            return jsonify({
                'status': 400,
                'message': 'Missing user__email parameter',
                'data': []
            }), 400
        
        perevals = db_manager.get_pereval_by_user_email(user_email)
        
        return jsonify({
            'status': 200,
            'message': 'Success',
            'data': perevals
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Internal server error: {str(e)}',
            'data': []
        }), 500

@pereval_bp.route('/health')
def health():
    return {'status': 'ok'}, 200