from flask import Flask
from config import Config
from extensions import db, login_manager, migrate
from routes import bp as main_bp  # assuming your Blueprint is named 'bp' in routes.py

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register single blueprint
    app.register_blueprint(main_bp)

    # Create DB tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
