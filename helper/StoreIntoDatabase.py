from DB_CONNECTION import get_db_connection


async def storeIntoDatabase(summary, category, sentiment, username):
    conn = await get_db_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = (await cur.fetchone())[0]

        await cur.execute(
            "SELECT id FROM categories WHERE user_id = %s AND category = %s",
            (user_id, category)
        )
        category_id = (await cur.fetchone())[0]

        await cur.execute(
            "INSERT INTO complaints (user_id, category_id, summary, sentiment) VALUES (%s, %s, %s, %s)",
            (user_id, category_id, summary, sentiment)
        )
        await cur.execute(
            "UPDATE categories SET count = count + 1 WHERE user_id = %s AND category = %s;",
            (user_id, category)
        )
    await conn.commit()
    await conn.close()
