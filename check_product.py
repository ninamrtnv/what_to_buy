from groq import Groq
import ast

import config
from add_item import add_new_item

client = Groq(
    api_key=config.GROQ_API_KEY
)


def check_products(user_id, dish):
    # Waiting for correct format answer form LLM
    while True:
        completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[
                {
                    "role": "system",
                    "content": "[product_1, product_2]"
                },
                {
                    "role": "user",
                    "content": f"Какие продукты нужны для {dish}? Ответь только массивом строк [product_1, product_2 ...]"
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        # Getting answer form LLM
        resp = completion.choices[0].message.content
        # If it's not array - try again
        if '[' not in resp or ']' not in resp:
            continue

        # Transform str='[a,b,c]' to list=[a,b,c]
        product_list = ast.literal_eval(resp)

        # Save to DB
        for product in product_list:
            add_new_item(user_id, product)

        return


