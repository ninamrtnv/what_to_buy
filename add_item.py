from psql import conn
import queries


def add_new_item(user_id, name):
    cur = conn.cursor()
    cur.execute(queries.add_item, (name, user_id))
    conn.commit()
    cur.close()