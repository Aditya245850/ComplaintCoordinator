import plotly.graph_objs as graph_obj

from DB_CONNECTION import get_db_connection

CATEGORIES = [
    'product-related',
    'service-related',
    'delivery-and-shipping',
    'billing-and-payments',
    'technical',
    'user-experience',
    'legal-and-compliance',
    'marketing-and-advertising',
    'returns-and-exchanges',
    'miscellaneous',
]


async def category_graph(username):
    conn = await get_db_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = (await cur.fetchone())[0]

        y_values = []
        for category in CATEGORIES:
            await cur.execute(
                "SELECT count FROM categories WHERE user_id = %s AND category = %s",
                (user_id, category)
            )
            y_values.append((await cur.fetchone())[0])

    await conn.close()

    figure = graph_obj.FigureWidget([graph_obj.Bar(x=CATEGORIES, y=y_values)])
    figure.update_layout(
        title={'text': "Complaint Tracker", 'font': {'color': 'white'}},
        xaxis_title="Subject",
        yaxis_title="Number of Complaints",
        xaxis=dict(title_font=dict(color='white'), tickfont=dict(color='white')),
        yaxis=dict(title_font=dict(color='white'), tickfont=dict(color='white')),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(51, 51, 51, 1)',
    )
    return figure.to_html(full_html=False)
