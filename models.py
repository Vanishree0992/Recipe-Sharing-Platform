from extensions import db
from flask_login import UserMixin
from datetime import datetime
import json

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(200))
    dietary = db.Column(db.String(200), default='[]')

    recipes = db.relationship('Recipe', backref='author', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, pw):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, pw)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)  # JSON list
    instructions = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200))
    dietary = db.Column(db.String(200), default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviews = db.relationship('Review', backref='recipe', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
