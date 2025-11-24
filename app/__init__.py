from flask import Flask
import logging

def create_app():
    app = Flask(__name__)
    
    logging.basicConfig(level=logging.INFO)
    
    # Регистрируем blueprint БЕЗ префикса
    from app.routes.pereval import pereval_bp
    app.register_blueprint(pereval_bp)
    
    # Добавим корневой health check на всякий случай
    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200
    
    return app