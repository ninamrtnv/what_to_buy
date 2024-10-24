from telegram import  InlineKeyboardButton

# callback data
FIRST_PAGE_CALLBACK = 'page_0'
CHECK_PRODUCT_CALLBACK = 'check_products'
ADD_ITEM_CALLBACK = 'add_item'
CLEAR_LIST_CALLBACK = 'clear_list'
MAIN_MENU_CALLBACK = 'main_menu'

# buttons
fetch_list_button = [
    InlineKeyboardButton("Посмотреть список покупок", callback_data=FIRST_PAGE_CALLBACK),
]

check_products_for_dish_button = [
    InlineKeyboardButton("Узнать какие продукты нужны для блюда", callback_data=CHECK_PRODUCT_CALLBACK),
]

add_item_button = [
    InlineKeyboardButton("Добавить продукт в список", callback_data=ADD_ITEM_CALLBACK),
]

clear_list_button = [
    InlineKeyboardButton("Oчистить список", callback_data=CLEAR_LIST_CALLBACK),
]

main_menu_button = [
    InlineKeyboardButton("Главное меню", callback_data=MAIN_MENU_CALLBACK),
]

# keyboards
main_menu_keyboard = [
    fetch_list_button, check_products_for_dish_button
]

fetch_list_keyboard = [
    add_item_button, clear_list_button, main_menu_button
]

fetch_empty_list_keyboard = [
    add_item_button, main_menu_button
]

after_add_item_keyboard = [
    add_item_button, fetch_list_button, main_menu_button
]