from psql import conn
import queries


def change_item_status(user_id, item_id):
    cur = conn.cursor()
    cur.execute(queries.change_item_status, (item_id, user_id,))
    conn.commit()
    cur.close()