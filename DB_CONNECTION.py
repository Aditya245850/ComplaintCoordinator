import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_PORT = os.environ.get('DB_PORT')


async def get_db_connection():
    return await psycopg.AsyncConnection.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        sslmode="require",
        sslrootcert=os.environ.get('DB_SSL_CERT', ''),
    )


async def init_db():
    conn = await get_db_connection()
    async with conn.cursor() as cur:
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        """)
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                category TEXT NOT NULL,
                count INTEGER DEFAULT 0
            );
        """)
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                category_id INTEGER REFERENCES categories(id),
                summary TEXT,
                sentiment TEXT
            );
        """)
    await conn.commit()
    await conn.close()
