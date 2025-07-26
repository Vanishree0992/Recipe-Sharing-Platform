import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///recipes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
