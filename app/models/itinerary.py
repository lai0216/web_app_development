from app.models.db import get_db_connection
import logging

class Itinerary:
    @staticmethod
    def create(title, start_date=None, end_date=None):
        """新增一筆行程記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO itineraries (title, start_date, end_date) VALUES (?, ?, ?)',
                (title, start_date, end_date)
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            logging.error(f"Error creating itinerary: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有行程記錄"""
        try:
            conn = get_db_connection()
            rows = conn.execute('SELECT * FROM itineraries ORDER BY created_at DESC').fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting itineraries: {e}")
            return []

    @staticmethod
    def get_by_id(itinerary_id):
        """取得單筆行程記錄"""
        try:
            conn = get_db_connection()
            row = conn.execute('SELECT * FROM itineraries WHERE id = ?', (itinerary_id,)).fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            logging.error(f"Error getting itinerary {itinerary_id}: {e}")
            return None

    @staticmethod
    def update(itinerary_id, title, start_date=None, end_date=None):
        """更新行程記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE itineraries SET title = ?, start_date = ?, end_date = ? WHERE id = ?',
                (title, start_date, end_date, itinerary_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logging.error(f"Error updating itinerary {itinerary_id}: {e}")
            return False

    @staticmethod
    def delete(itinerary_id):
        """刪除行程記錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM itineraries WHERE id = ?', (itinerary_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logging.error(f"Error deleting itinerary {itinerary_id}: {e}")
            return False
