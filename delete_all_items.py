from telegram import Update
from psql import conn
import queries


def delete_all_items(update: Update):
    cur = conn.cursor()
    cur.execute(queries.delete_all_items, (update.callback_query.from_user.id,))
    conn.commit()
    cur.close()