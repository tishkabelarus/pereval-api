from flask import Blueprint, request, jsonify

# Создаем blueprint
pereval_bp = Blueprint('pereval', __name__)

# Импортируем после создания blueprint чтобы избежать циклических импортов
from app.models.database import db_manager

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