import sqlite3
import os
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.db_file = 'pereval.db'
        
    def add_pereval(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Создаем пользователя
            user_data = data.get('user', {})
            cursor.execute(
                "INSERT INTO users (email, phone, fam, name, otc) VALUES (?, ?, ?, ?, ?)",
                (
                    user_data.get('email'),
                    user_data.get('phone'),
                    user_data.get('fam'),
                    user_data.get('name'),
                    user_data.get('otc')
                )
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
                    data.get('beautyTitle'),
                    data.get('title'),
                    data.get('other_titles'),
                    data.get('connect'),
                    float(data.get('coords', {}).get('latitude', 0)),
                    float(data.get('coords', {}).get('longitude', 0)),
                    int(data.get('coords', {}).get('height', 0)),
                    user_id,
                    1,  # area_id по умолчанию
                    data.get('level', {}).get('winter'),
                    data.get('level', {}).get('summer'),
                    data.get('level', {}).get('autumn'),
                    data.get('level', {}).get('spring')
                )
            )
            pereval_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return {'status': 200, 'message': 'Success', 'id': pereval_id}
            
        except Exception as e:
            logger.error(f"Error adding pereval: {e}")
            return {'status': 500, 'message': f'Database error: {str(e)}', 'id': None}
    
    def get_pereval(self, pereval_id: int) -> Optional[Dict[str, Any]]:
        """Получение перевала по ID"""
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.*, u.email, u.phone, u.fam, u.name, u.otc
                FROM perevals p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = ?
            """, (pereval_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Создаем словарь с данными перевала
            pereval = {
                'id': row['id'],
                'date_added': row['date_added'],
                'beautyTitle': row['beauty_title'],
                'title': row['title'],
                'other_titles': row['other_titles'],
                'connect': row['connect'],
                'coords': {
                    'latitude': str(row['latitude']),
                    'longitude': str(row['longitude']),
                    'height': str(row['height'])
                },
                'user': {
                    'email': row['email'],
                    'phone': row['phone'],
                    'fam': row['fam'],
                    'name': row['name'],
                    'otc': row['otc']
                },
                'level': {
                    'winter': row['level_winter'],
                    'summer': row['level_summer'],
                    'autumn': row['level_autumn'],
                    'spring': row['level_spring']
                },
                'status': row['status']
            }
            
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
            
            pereval['images'] = [
                {
                    'id': img[0],
                    'title': img[1],
                    'data': img[2],
                    'date_added': img[3]
                } for img in images
            ]
            
            pereval['activities'] = [
                {
                    'id': act[0],
                    'title': act[1]
                } for act in activities
            ]
            
            return pereval
            
        except Exception as e:
            logger.error(f"Error getting pereval: {e}")
            return None
    
    def update_pereval(self, pereval_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
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
            
            # Обновляем данные перевала
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
            
            conn.commit()
            conn.close()
            
            return {'state': 1, 'message': 'Success'}
            
        except Exception as e:
            logger.error(f"Error updating pereval: {e}")
            return {'state': 0, 'message': f'Database error: {str(e)}'}
    
    def get_pereval_by_user_email(self, email: str) -> List[Dict[str, Any]]:
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

# Создаем экземпляр для импорта
db_manager = DatabaseManager()