from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, \
    SelectMultipleField, FileField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class RecipeForm(FlaskForm):
    title = StringField('Recipe Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients (JSON format)', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    image = FileField('Recipe Image')
    dietary = SelectMultipleField('Dietary filters',
        choices=[('vegan','Vegan'),('vegetarian','Vegetarian'),
                 ('gluten_free','Gluten-Free'),('dairy_free','Dairy-Free')])

    submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1–5)', validators=[DataRequired()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit')

class LocationForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Search')