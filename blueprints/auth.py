from quart import Blueprint, redirect, render_template, request, url_for
from quart_auth import AuthUser, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from DB_CONNECTION import get_db_connection

auth_bp = Blueprint('auth', __name__)

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


@auth_bp.route('/')
async def home():
    return await render_template('home.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        form = await request.form
        username = form['username'].lower()
        password = form['password']

        conn = await get_db_connection()
        async with conn.cursor() as cur:
            await cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
            result = await cur.fetchone()
        await conn.close()

        if result:
            if check_password_hash(result[0], password):
                login_user(AuthUser(username))
                return redirect(url_for('dashboard.index'))
            else:
                error = "Password incorrect."
        else:
            error = "Login not found."

        return await render_template('login.html', error=error)

    return await render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == 'POST':
        form = await request.form
        username = form['username'].lower()
        password = form['password']
        password_hash = generate_password_hash(password)

        conn = await get_db_connection()
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash),
            )
            await cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = (await cur.fetchone())[0]

            for category in CATEGORIES:
                await cur.execute(
                    "INSERT INTO categories (user_id, category) VALUES (%s, %s);",
                    (user_id, category),
                )
        await conn.commit()
        await conn.close()

        return redirect(url_for('auth.login'))

    return await render_template('register.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
async def logout():
    logout_user()
    return await render_template('home.html')
