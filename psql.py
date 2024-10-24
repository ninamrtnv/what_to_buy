import psycopg2

import config

conn = psycopg2.connect(database=config.PSQL_DB,
                        user=config.PSQL_USER,
                        password=config.PSQL_PASS,
                        host=config.PSQL_HOST,
                        port=config.PSQL_PORT)