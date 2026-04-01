from DB_CONNECTION import get_db_connection


async def downloadContent(username):
    conn = await get_db_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = (await cur.fetchone())[0]

        await cur.execute("""
            SELECT complaints.summary, complaints.sentiment, categories.category
            FROM complaints
            JOIN categories ON complaints.category_id = categories.id
            WHERE complaints.user_id = %s
        """, (user_id,))

        complaints_details = [
            f"{summary} - Tone: {sentiment} - Type of complaint: {category}.\n"
            for summary, sentiment, category in await cur.fetchall()
        ]

    await conn.close()
    return complaints_details
