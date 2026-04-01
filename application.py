import os

from dotenv import load_dotenv
from quart import Quart

from DB_CONNECTION import init_db

load_dotenv()


def create_app():
    app = Quart(__name__)
    app.secret_key = os.environ.get('SECRET_KEY')
    app.config['API_KEY'] = os.environ.get('OPENAI_API_KEY')

    upload_folder = 'uploads/'
    app.config['UPLOAD_FOLDER'] = upload_folder
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    from blueprints.auth import auth_bp
    from blueprints.dashboard import dashboard_bp
    from blueprints.uploads import uploads_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(uploads_bp)

    @app.before_serving
    async def startup():
        await init_db()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
