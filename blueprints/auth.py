from flask import Blueprint, redirect, render_template, request, session, url_for
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
def home():
    return render_template('home.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            if check_password_hash(result[0], password):
                session['username'] = username
                return redirect(url_for('dashboard.index'))
            else:
                error = "Password incorrect."
        else:
            error = "Login not found."

        return render_template('login.html', error=error)

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash),
        )
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]

        for category in CATEGORIES:
            cursor.execute(
                "INSERT INTO categories (user_id, category) VALUES (%s, %s);",
                (user_id, category),
            )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('home.html')
