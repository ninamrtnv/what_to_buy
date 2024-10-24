CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    name VARCHAR NOT NULL,
    is_bought BOOL NOT NULL DEFAULT False,

    created_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
)