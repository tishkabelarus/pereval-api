import sqlite3
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.db_file = 'pereval.db'
        
    def add_pereval(self, data):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Создаем пользователя
            user_data = data.get('user', {})
            cursor.execute(
                "INSERT INTO users (email, phone, fam, name, otc) VALUES (?, ?, ?, ?, ?)",
                (user_data.get('email'), user_data.get('phone'), user_data.get('fam'), 
                 user_data.get('name'), user_data.get('otc'))
            )
            user_id = cursor.lastrowid
            
            # Добавляем перевал
            cursor.execute(
                """INSERT INTO perevals 
                (beauty_title, title, other_titles, connect, 
                 latitude, longitude, height, user_id, area_id,
                 level_winter, level_summer, level_autumn, level_spring, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new')""",
                (
                    data.get('beautyTitle'), data.get('title'), data.get('other_titles'),
                    data.get('connect'), float(data.get('coords', {}).get('latitude', 0)),
                    float(data.get('coords', {}).get('longitude', 0)),
                    int(data.get('coords', {}).get('height', 0)), user_id, 1,
                    data.get('level', {}).get('winter'), data.get('level', {}).get('summer'),
                    data.get('level', {}).get('autumn'), data.get('level', {}).get('spring')
                )
            )
            pereval_id = cursor.lastrowid
            
            # Добавляем изображения
            images = data.get('images', {}).get('images', [])
            for img_data in images:
                cursor.execute(
                    """INSERT INTO pereval_images (pereval_id, title, file_path)
                     VALUES (?, ?, ?)""",
                    (pereval_id, img_data.get('title'), img_data.get('file_path'))
                )
            
            # Добавляем активности
            activities = data.get('activities', [])
            for activity_id in activities:
                cursor.execute(
                    """INSERT INTO pereval_activities (pereval_id, activity_type_id)
                     VALUES (?, ?)""",
                    (pereval_id, activity_id)
                )
            
            conn.commit()
            conn.close()
            
            return {'status': 200, 'message': 'Success', 'id': pereval_id}
            
        except Exception as e:
            return {'status': 500, 'message': f'Database error: {str(e)}', 'id': None}
    
    def get_pereval(self, pereval_id):
        """Получение перевала по ID"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.*, u.email, u.phone, u.fam, u.name, u.otc
                FROM perevals p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = ?
            """, (pereval_id,))
            
            pereval = cursor.fetchone()
            if not pereval:
                return None
            
            # Получаем изображения
            cursor.execute("""
                SELECT id, title, file_path, date_added
                FROM pereval_images
                WHERE pereval_id = ?
            """, (pereval_id,))
            images = cursor.fetchall()
            
            # Получаем активности
            cursor.execute("""
                SELECT sat.id, sat.title
                FROM pereval_activities pa
                JOIN spr_activities_types sat ON pa.activity_type_id = sat.id
                WHERE pa.pereval_id = ?
            """, (pereval_id,))
            activities = cursor.fetchall()
            
            conn.close()
            
            return {
                'id': pereval[0],
                'date_added': pereval[1],
                'beautyTitle': pereval[2],
                'title': pereval[3],
                'other_titles': pereval[4],
                'connect': pereval[5],
                'coords': {
                    'latitude': str(pereval[6]),
                    'longitude': str(pereval[7]),
                    'height': str(pereval[8])
                },
                'user': {
                    'email': pereval[13],
                    'phone': pereval[14],
                    'fam': pereval[15],
                    'name': pereval[16],
                    'otc': pereval[17]
                },
                'level': {
                    'winter': pereval[11],
                    'summer': pereval[12],
                    'autumn': pereval[13],
                    'spring': pereval[14]
                },
                'status': pereval[15],
                'images': [
                    {
                        'id': img[0],
                        'title': img[1],
                        'data': img[2],
                        'date_added': img[3]
                    } for img in images
                ],
                'activities': [
                    {
                        'id': act[0],
                        'title': act[1]
                    } for act in activities
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting pereval: {e}")
            return None
    
    def update_pereval(self, pereval_id, data):
        """Обновление перевала"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Проверяем статус перевала
            cursor.execute("SELECT status FROM perevals WHERE id = ?", (pereval_id,))
            result = cursor.fetchone()
            
            if not result:
                return {'state': 0, 'message': 'Pereval not found'}
            
            status = result[0]
            if status != 'new':
                return {'state': 0, 'message': f'Cannot edit pereval with status: {status}'}
            
            # Обновляем данные перевала (кроме user_id)
            update_fields = []
            update_values = []
            
            if 'beautyTitle' in data:
                update_fields.append("beauty_title = ?")
                update_values.append(data['beautyTitle'])
            
            if 'title' in data:
                update_fields.append("title = ?")
                update_values.append(data['title'])
            
            if 'other_titles' in data:
                update_fields.append("other_titles = ?")
                update_values.append(data['other_titles'])
            
            if 'connect' in data:
                update_fields.append("connect = ?")
                update_values.append(data['connect'])
            
            if 'coords' in data:
                coords = data['coords']
                if 'latitude' in coords:
                    update_fields.append("latitude = ?")
                    update_values.append(float(coords['latitude']))
                if 'longitude' in coords:
                    update_fields.append("longitude = ?")
                    update_values.append(float(coords['longitude']))
                if 'height' in coords:
                    update_fields.append("height = ?")
                    update_values.append(int(coords['height']))
            
            if 'level' in data:
                level = data['level']
                if 'winter' in level:
                    update_fields.append("level_winter = ?")
                    update_values.append(level['winter'])
                if 'summer' in level:
                    update_fields.append("level_summer = ?")
                    update_values.append(level['summer'])
                if 'autumn' in level:
                    update_fields.append("level_autumn = ?")
                    update_values.append(level['autumn'])
                if 'spring' in level:
                    update_fields.append("level_spring = ?")
                    update_values.append(level['spring'])
            
            if update_fields:
                update_query = f"UPDATE perevals SET {', '.join(update_fields)} WHERE id = ?"
                update_values.append(pereval_id)
                cursor.execute(update_query, update_values)
            
            # Обновляем изображения (удаляем старые, добавляем новые)
            if 'images' in data:
                cursor.execute("DELETE FROM pereval_images WHERE pereval_id = ?", (pereval_id,))
                images = data.get('images', {}).get('images', [])
                for img_data in images:
                    cursor.execute(
                        "INSERT INTO pereval_images (pereval_id, title, file_path) VALUES (?, ?, ?)",
                        (pereval_id, img_data.get('title'), img_data.get('file_path'))
                    )
            
            # Обновляем активности (удаляем старые, добавляем новые)
            if 'activities' in data:
                cursor.execute("DELETE FROM pereval_activities WHERE pereval_id = ?", (pereval_id,))
                activities = data.get('activities', [])
                for activity_id in activities:
                    cursor.execute(
                        "INSERT INTO pereval_activities (pereval_id, activity_type_id) VALUES (?, ?)",
                        (pereval_id, activity_id)
                    )
            
            conn.commit()
            conn.close()
            
            return {'state': 1, 'message': 'Success'}
            
        except Exception as e:
            logger.error(f"Error updating pereval: {e}")
            return {'state': 0, 'message': f'Database error: {str(e)}'}
    
    def get_pereval_by_user_email(self, email):
        """Получение всех перевалов пользователя по email"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.id, p.title, p.beauty_title, p.status, p.date_added
                FROM perevals p
                JOIN users u ON p.user_id = u.id
                WHERE u.email = ?
                ORDER BY p.date_added DESC
            """, (email,))
            
            perevals = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': p[0],
                    'title': p[1],
                    'beautyTitle': p[2],
                    'status': p[3],
                    'date_added': p[4]
                } for p in perevals
            ]
            
        except Exception as e:
            logger.error(f"Error getting perevals by email: {e}")
            return []

db_manager = DatabaseManager()