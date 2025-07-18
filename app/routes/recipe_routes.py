import os
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app.models import db, Recipe
from datetime import datetime

recipe_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

UPLOAD_FOLDER = 'static/uploads'

def show():
    request.form.get('title')
    request.form.get('description')
    request.form.get('ingredients')
    request.form.get('instructions')
    request.form.get('time_of_eat')
    request.form.get('language')
    request.form.get('user_id', 1)
    return render_template('submit_recipe.html')

# Unified recipe creation (web + mobile)
@recipe_bp.route('/create', methods=['POST','GET'])
def create_recipe():
    if request.method == 'GET':
        return show()
    title = request.form.get('title')
    description = request.form.get('description')
    ingredients = request.form.get('ingredients')
    instructions = request.form.get('instructions')
    time_of_eat = request.form.get('time_of_eat')
    type_of_dish = request.form.get('type_of_dish')
    language = request.form.get('language')
    user_id = request.form.get('user_id', 1)  # Simulated user

    image = request.files.get('image')
    image_filename = None

    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, filename)
        image.save(image_path)
        image_filename = filename

    recipe = Recipe(
        title=title,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
        time_of_eat=time_of_eat,
        type_of_dish=type_of_dish,
        language=language,
        user_id=user_id,
        image=image_filename,
        created_at=datetime.utcnow()
    )

    db.session.add(recipe)
    db.session.commit()

    if request.accept_mimetypes.best == 'application/json':
        return jsonify({'message': 'Recipe created successfully', 'id': recipe.id}), 201

    flash('Recipe created successfully')
    return redirect(url_for('recipes.home'))

# Recipe Feed (Web) with filters and search
@recipe_bp.route('/')
def home():
    query = Recipe.query.order_by(Recipe.created_at.desc())

    # Filters
    time_of_eat = request.args.get('time_of_eat')
    type_of_dish = request.args.get('type_of_dish')
    language = request.args.get('language')
    search = request.args.get('search')

    if time_of_eat:
        query = query.filter_by(time_of_eat=time_of_eat)
    if type_of_dish:
        query = query.filter_by(type_of_dish=type_of_dish)
    if language:
        query = query.filter_by(language=language)
    if search:
        query = query.filter(
            Recipe.title.ilike(f'%{search}%') | 
            Recipe.description.ilike(f'%{search}%')
        )

    recipes = query.all()
    return render_template('home.html', recipes=recipes)

# Recipe Feed API (Mobile)
@recipe_bp.route('/api', methods=['GET'])
def api_home():
    query = Recipe.query.order_by(Recipe.created_at.desc())

    # Filters
    time_of_eat = request.args.get('time_of_eat')
    type_of_dish = request.args.get('type_of_dish')
    language = request.args.get('language')
    search = request.args.get('search')

    if time_of_eat:
        query = query.filter_by(time_of_eat=time_of_eat)
    if type_of_dish:
        query = query.filter_by(type_of_dish=type_of_dish)
    if language:
        query = query.filter_by(language=language)
    if search:
        query = query.filter(
            Recipe.title.ilike(f'%{search}%') | 
            Recipe.description.ilike(f'%{search}%')
        )

    recipes = query.all()

    return jsonify([
        {
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'ingredients': r.ingredients,
            'instructions': r.instructions,
            'time_of_eat': r.time_of_eat,
            'type_of_dish': r.type_of_dish,
            'language': r.language,
            'user_id': r.user_id,
            'image_url': url_for('static', filename=f'uploads/{r.image}', _external=True) if r.image else None,
            'created_at': r.created_at.isoformat()
        }
        for r in recipes
    ])

# Web: View single recipe
@recipe_bp.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('view_recipe.html', recipe=recipe)

# API: View single recipe for mobile
@recipe_bp.route('/api/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe_api(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify({
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'time_of_eat': recipe.time_of_eat,
        'type_of_dish': recipe.type_of_dish,
        'language': recipe.language,
        'user_id': recipe.user_id,
        'image_url': url_for('static', filename=f'uploads/{recipe.image}', _external=True) if recipe.image else None,
        'created_at': recipe.created_at.isoformat()
    })
