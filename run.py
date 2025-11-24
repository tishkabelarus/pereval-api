from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения

app = create_app()

if __name__ == '__main__':
    # Получаем настройки из переменных окружения
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Получаем настройки БД (для логов)
    db_host = os.getenv('FSTR_DB_HOST', 'localhost')
    db_port = os.getenv('FSTR_DB_PORT', '5432')
    db_name = os.getenv('FSTR_DB_NAME', 'pereval')
    
    print(" Starting Pereval API")
    print(f"   Server: http://{host}:{port}")
    print(f"   Database: {db_host}:{db_port}/{db_name}")
    print(f"   Debug: {debug}")
    
    app.run(host=host, port=port, debug=debug)