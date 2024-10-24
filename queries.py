ITEMS_PER_PAGE = 5

fetch_list = '''
SELECT id, name, is_bought FROM products 
    WHERE deleted_at IS NULL AND chat_id = %s 
    ORDER BY is_bought
    LIMIT %s OFFSET %s
'''

fetch_list_count = '''
    SELECT count(*) FROM products WHERE deleted_at IS NULL AND chat_id = %s 
'''

change_item_status = '''
    UPDATE products SET is_bought = NOT is_bought WHERE id = %s AND chat_id = %s
'''

delete_all_items = '''
    UPDATE products SET deleted_at = now() WHERE chat_id = %s
'''

add_item = '''
INSERT INTO products (name, chat_id) VALUES (%s,%s)
'''
