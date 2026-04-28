from app.models.db import get_db_connection
import logging

class Destination:
    @staticmethod
    def create(itinerary_id, name, day_number, notes=None):
        """新增一筆景點記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 取得該天數目前的最後順序，以便加入在最後面
            res = cursor.execute(
                'SELECT MAX(order_index) as max_order FROM destinations WHERE itinerary_id = ? AND day_number = ?',
                (itinerary_id, day_number)
            ).fetchone()
            next_order = (res['max_order'] or 0) + 1

            cursor.execute(
                'INSERT INTO destinations (itinerary_id, name, day_number, order_index, notes) VALUES (?, ?, ?, ?, ?)',
                (itinerary_id, name, day_number, next_order, notes)
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            logging.error(f"Error creating destination: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有景點記錄"""
        try:
            conn = get_db_connection()
            rows = conn.execute('SELECT * FROM destinations ORDER BY created_at DESC').fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting destinations: {e}")
            return []

    @staticmethod
    def get_by_id(destination_id):
        """取得單筆景點記錄"""
        try:
            conn = get_db_connection()
            row = conn.execute('SELECT * FROM destinations WHERE id = ?', (destination_id,)).fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            logging.error(f"Error getting destination {destination_id}: {e}")
            return None

    @staticmethod
    def get_by_itinerary_and_day(itinerary_id, day_number=None):
        """取得特定行程(或特定天數)的所有景點"""
        try:
            conn = get_db_connection()
            if day_number is not None:
                rows = conn.execute(
                    'SELECT * FROM destinations WHERE itinerary_id = ? AND day_number = ? ORDER BY order_index ASC',
                    (itinerary_id, day_number)
                ).fetchall()
            else:
                rows = conn.execute(
                    'SELECT * FROM destinations WHERE itinerary_id = ? ORDER BY day_number ASC, order_index ASC',
                    (itinerary_id,)
                ).fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting destinations for itinerary {itinerary_id}: {e}")
            return []

    @staticmethod
    def update(destination_id, name, day_number, notes=None):
        """更新景點記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE destinations SET name = ?, day_number = ?, notes = ? WHERE id = ?',
                (name, day_number, notes, destination_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logging.error(f"Error updating destination {destination_id}: {e}")
            return False

    @staticmethod
    def update_order(destination_id, new_order_index, new_day_number=None):
        """更新景點的拖曳排序"""
        try:
            conn = get_db_connection()
            if new_day_number is not None:
                conn.execute(
                    'UPDATE destinations SET order_index = ?, day_number = ? WHERE id = ?',
                    (new_order_index, new_day_number, destination_id)
                )
            else:
                conn.execute(
                    'UPDATE destinations SET order_index = ? WHERE id = ?',
                    (new_order_index, destination_id)
                )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logging.error(f"Error updating order for destination {destination_id}: {e}")
            return False

    @staticmethod
    def delete(destination_id):
        """刪除景點記錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM destinations WHERE id = ?', (destination_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logging.error(f"Error deleting destination {destination_id}: {e}")
            return False
