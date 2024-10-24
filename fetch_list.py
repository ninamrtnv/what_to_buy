from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards import fetch_list_keyboard
from psql import conn
import queries
import keyboards


def is_bought_emoji(is_bought):
    if is_bought:
        return "❌"
    return "✅"


async def fetch_list(update: Update, page_number: int):
    chat_id = update.callback_query.from_user.id

    cur = conn.cursor()
    cur.execute(queries.fetch_list_count, (chat_id,))
    total_items = cur.fetchone()[0]
    cur.close()

    if total_items == 0:
        if update.message is not None:
            await update.message.reply_text('Кажется Ваш лист пуст, попробуйте добавить в него продукты.', reply_markup=InlineKeyboardMarkup(keyboards.fetch_empty_list_keyboard))
        else:
            await update.callback_query.edit_message_text('Кажется Ваш лист пуст, попробуйте добавить в него продукты.', reply_markup=InlineKeyboardMarkup(keyboards.fetch_empty_list_keyboard))
        return

    cur = conn.cursor()
    limit = queries.ITEMS_PER_PAGE
    offset = queries.ITEMS_PER_PAGE * page_number
    cur.execute(queries.fetch_list, (chat_id, limit, offset))
    items = cur.fetchall()
    cur.close()

    product_keyboard = [
        [InlineKeyboardButton(item[1], callback_data=f'item_{item[0]}'),
         InlineKeyboardButton(is_bought_emoji(item[2]), callback_data=f'item_{item[0]}_{is_bought_emoji(item[2])}_{page_number}')] for i, item in enumerate(items)
    ]

    navigation_buttons = []
    if page_number > 0:
        navigation_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f'page_{page_number - 1}'))
    if (offset + limit) < total_items:
        navigation_buttons.append(InlineKeyboardButton("Вперед ➡️", callback_data=f'page_{page_number + 1}'))

    if navigation_buttons:
        product_keyboard.append(navigation_buttons)

    for buttons in fetch_list_keyboard:
        product_keyboard.append(buttons)

    await update.callback_query.edit_message_text(text=f"✅- отметить как купленный продукт.\n❌- отметить как продукт, который нужно купить.\n\n Страница {page_number + 1}:", reply_markup=InlineKeyboardMarkup(product_keyboard))
