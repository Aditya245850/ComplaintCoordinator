from DB_CONNECTION import get_db_connection


def downloadContent(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()[0]

    cursor.execute("""
        SELECT complaints.summary, complaints.sentiment, categories.category
        FROM complaints
        JOIN categories ON complaints.category_id = categories.id
        WHERE complaints.user_id = %s
    """, (user_id,))

    complaints_details = [
        f"{summary} - Tone: {sentiment} - Type of complaint: {category}.\n"
        for summary, sentiment, category in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return complaints_details
