from app.models.db import get_db_connection

class Itinerary:
    @staticmethod
    def create(title, start_date=None, end_date=None):
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

    @staticmethod
    def get_all():
        conn = get_db_connection()
        itineraries = conn.execute('SELECT * FROM itineraries ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(row) for row in itineraries]

    @staticmethod
    def get_by_id(itinerary_id):
        conn = get_db_connection()
        itinerary = conn.execute('SELECT * FROM itineraries WHERE id = ?', (itinerary_id,)).fetchone()
        conn.close()
        return dict(itinerary) if itinerary else None

    @staticmethod
    def update(itinerary_id, title, start_date=None, end_date=None):
        conn = get_db_connection()
        conn.execute(
            'UPDATE itineraries SET title = ?, start_date = ?, end_date = ? WHERE id = ?',
            (title, start_date, end_date, itinerary_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(itinerary_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM itineraries WHERE id = ?', (itinerary_id,))
        conn.commit()
        conn.close()
