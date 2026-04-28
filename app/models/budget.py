from app.models.db import get_db_connection

class Budget:
    @staticmethod
    def create(itinerary_id, category, amount, notes=None):
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

    @staticmethod
    def get_by_itinerary(itinerary_id):
        conn = get_db_connection()
        budgets = conn.execute(
            'SELECT * FROM budgets WHERE itinerary_id = ? ORDER BY created_at ASC',
            (itinerary_id,)
        ).fetchall()
        conn.close()
        return [dict(row) for row in budgets]

    @staticmethod
    def update(budget_id, category, amount, notes=None):
        conn = get_db_connection()
        conn.execute(
            'UPDATE budgets SET category = ?, amount = ?, notes = ? WHERE id = ?',
            (category, amount, notes, budget_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(budget_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM budgets WHERE id = ?', (budget_id,))
        conn.commit()
        conn.close()
