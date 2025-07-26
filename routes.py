from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from forms import LoginForm, RegisterForm, RecipeForm, ReviewForm, LocationForm
from models import User, Recipe, Review
from utils import convert_measure, estimate_nutrition
from werkzeug.utils import secure_filename
from config import Config
import json, os
from io import BytesIO
from reportlab.pdfgen import canvas
from extensions import db, login_manager

bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# --- Auth Routes ---
@bp.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('recipe_list'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.check_password(form.password.data):
            login_user(u)
            return redirect(url_for('recipe_list'))
        flash('Invalid credentials.')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Registration successful.')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# --- User Profile Route ---
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST' and 'avatar' in request.files:
        f = request.files['avatar']
        fname = secure_filename(f.filename)
        f.save(os.path.join(Config.UPLOAD_FOLDER, fname))
        current_user.avatar = fname
        # Update dietary preferences
        current_user.dietary = json.dumps(request.form.getlist('dietary'))
        db.session.commit()
        flash('Profile updated.')
        return redirect(url_for('profile'))
    dietary_prefs = json.loads(current_user.dietary or '[]')
    return render_template('profile.html', dietary=dietary_prefs)


# --- Recipe Routes ---
@bp.route('/recipes')
def recipe_list():
    recs = Recipe.query.all()
    return render_template('recipes/list.html', recipes=recs)

@bp.route('/recipes/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        ing = json.loads(form.ingredients.data)
        fname = None
        if form.image.data:
            fname = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(Config.UPLOAD_FOLDER, fname))
        r = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            author=current_user,
            image=fname,
            dietary=json.dumps(form.dietary.data)
        )
        db.session.add(r); db.session.commit()
        flash('Recipe added!')
        return redirect(url_for('recipe_list'))
    return render_template('recipes/new.html', form=form)

@bp.route('/recipes/<int:rid>', methods=['GET', 'POST'])
def recipe_detail(rid):
    r = Recipe.query.get_or_404(rid)
    form = ReviewForm()
    nutrition = estimate_nutrition(json.loads(r.ingredients))
    if form.validate_on_submit() and current_user.is_authenticated:
        rev = Review(rating=form.rating.data, comment=form.comment.data,
                     recipe=r, user=current_user)
        db.session.add(rev); db.session.commit()
        flash('Review added.')
        return redirect(url_for('recipe_detail', rid=rid))
    return render_template('recipes/detail.html', r=r, form=form,
                           nutrition=nutrition,
                           convert=convert_measure)


# --- Meal Planner Calendar ---
@bp.route('/planner')
@login_required
def planner():
    # placeholder: implement calendar drag/drop front-end
    return render_template('planner.html')


# --- Shopping List Generator ---
@bp.route('/shopping_list')
@login_required
def shopping_list():
    picked = request.args.getlist('recipe')
    items = []
    for rid in picked:
        rec = Recipe.query.get(int(rid))
        items.extend(json.loads(rec.ingredients))
    return render_template('shopping_list.html', items=items)


# --- Print-friendly Recipe View ---
@bp.route('/print_recipe/<int:rid>')
def print_recipe(rid):
    r = Recipe.query.get_or_404(rid)
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Recipe: {r.title}")
    y = 780
    p.drawString(100, y, "Ingredients:")
    for i in json.loads(r.ingredients):
        y -= 20
        p.drawString(120, y, f"{i.get('amount')} {i.get('unit')} {i.get('name')}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{r.title}.pdf",
                     mimetype='application/pdf')


# --- Social Sharing Link ---
@bp.route('/share/<int:rid>')
def share_recipe(rid):
    r = Recipe.query.get_or_404(rid)
    url = url_for('recipe_detail', rid=rid, _external=True)
    return render_template('share_view.html', recipe=r, share_url=url)
