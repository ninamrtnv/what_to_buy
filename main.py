from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

import keyboards
import config
from add_item import add_new_item
from check_product import check_products
from delete_all_items import delete_all_items
from fetch_list import fetch_list, is_bought_emoji
from change_item_status import change_item_status
from keyboards import CLEAR_LIST_CALLBACK, ADD_ITEM_CALLBACK, CHECK_PRODUCT_CALLBACK, MAIN_MENU_CALLBACK

STATE_KEY = 'state'
NEW_PRODUCT_STATE = "new_product_state"
CHECK_PRODUCT_STATE = "check_product_state"


def clear_state(context):
    context.user_data[STATE_KEY] = None


async def start(update: Update, context):
    clear_state(context)
    msg = 'Выберите опцию:'
    if update.message is not None:
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboards.main_menu_keyboard))
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboards.main_menu_keyboard))


async def handle_button(update: Update, context):
    clear_state(context)
    query = update.callback_query
    await query.answer()

    if query.data.startswith('page_'):
        page_number = int(query.data.split('_')[-1])
        await fetch_list(update, page_number)
    elif is_bought_emoji(True) in query.data or is_bought_emoji(False) in query.data:
        parts = query.data.split('_')
        item_id = parts[1]
        page_number = parts[3]
        change_item_status(update.callback_query.from_user.id, item_id)
        await fetch_list(update, int(page_number))
    elif query.data == CLEAR_LIST_CALLBACK:
        delete_all_items(update)
        await fetch_list(update, 0)
    elif query.data == ADD_ITEM_CALLBACK:
        await query.edit_message_text(text="Введите продукт!")
        context.user_data[STATE_KEY] = NEW_PRODUCT_STATE
    elif query.data == CHECK_PRODUCT_CALLBACK:
        await query.edit_message_text(text="Введите название блюда!")
        context.user_data[STATE_KEY] = CHECK_PRODUCT_STATE
    elif query.data == MAIN_MENU_CALLBACK:
        await start(update, context)


async def handle_message(update: Update, context):
    user_id = update.message.from_user.id
    if context.user_data.get(STATE_KEY) == NEW_PRODUCT_STATE:
        pd = update.message.text
        add_new_item(user_id, pd)
        await update.message.reply_text(f'Вы добавили в лист "{pd}"! Добавьте еще продукт или посмотрите ваш лист.', reply_markup=InlineKeyboardMarkup(keyboards.after_add_item_keyboard))
    elif context.user_data.get(STATE_KEY) == CHECK_PRODUCT_STATE:
        dish = update.message.text
        check_products(user_id, dish)
        await update.message.reply_text(f'Продукты для этого блюда добавлены в лист!', reply_markup=InlineKeyboardMarkup(keyboards.main_menu_keyboard))
    else:
        await update.message.reply_text("Введите команду /start")

    clear_state(context)


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TG_BOT_API_KEY).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(handle_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("[INFO] Bot started")
    application.run_polling()