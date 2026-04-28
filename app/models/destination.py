from app.models.db import get_db_connection

class Destination:
    @staticmethod
    def create(itinerary_id, name, day_number, notes=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get the next order_index for the given day
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

    @staticmethod
    def get_by_itinerary_and_day(itinerary_id, day_number):
        conn = get_db_connection()
        destinations = conn.execute(
            'SELECT * FROM destinations WHERE itinerary_id = ? AND day_number = ? ORDER BY order_index ASC',
            (itinerary_id, day_number)
        ).fetchall()
        conn.close()
        return [dict(row) for row in destinations]

    @staticmethod
    def update_order(destination_id, new_order_index, new_day_number=None):
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

    @staticmethod
    def delete(destination_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM destinations WHERE id = ?', (destination_id,))
        conn.commit()
        conn.close()
