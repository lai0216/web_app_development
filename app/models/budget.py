from app.models.db import get_db_connection
import logging

class Budget:
    @staticmethod
    def create(itinerary_id, category, amount, notes=None):
        """新增一筆預算記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO budgets (itinerary_id, category, amount, notes) VALUES (?, ?, ?, ?)',
                (itinerary_id, category, amount, notes)
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            logging.error(f"Error creating budget: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有預算記錄"""
        try:
            conn = get_db_connection()
            rows = conn.execute('SELECT * FROM budgets ORDER BY created_at DESC').fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting budgets: {e}")
            return []

    @staticmethod
    def get_by_id(budget_id):
        """取得單筆預算記錄"""
        try:
            conn = get_db_connection()
            row = conn.execute('SELECT * FROM budgets WHERE id = ?', (budget_id,)).fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            logging.error(f"Error getting budget {budget_id}: {e}")
            return None

    @staticmethod
    def get_by_itinerary(itinerary_id):
        """取得特定行程的所有預算項目"""
        try:
            conn = get_db_connection()
            rows = conn.execute(
                'SELECT * FROM budgets WHERE itinerary_id = ? ORDER BY created_at ASC',
                (itinerary_id,)
            ).fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting budgets for itinerary {itinerary_id}: {e}")
            return []

    @staticmethod
    def update(budget_id, category, amount, notes=None):
        """更新預算記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE budgets SET category = ?, amount = ?, notes = ? WHERE id = ?',
                (category, amount, notes, budget_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logging.error(f"Error updating budget {budget_id}: {e}")
            return False

    @staticmethod
    def delete(budget_id):
        """刪除預算記錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM budgets WHERE id = ?', (budget_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logging.error(f"Error deleting budget {budget_id}: {e}")
            return False
