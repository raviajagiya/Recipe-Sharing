# app/routes/recipe_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Recipe
import os
from werkzeug.utils import secure_filename
from datetime import datetime

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@recipe_bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_recipe():
    if request.method == 'POST':
        if request.is_json:
            # ---- Mobile/API request ----
            data = request.get_json()
            required_fields = ['title', 'description', 'ingredients', 'instructions', 'time_of_eat', 'type_of_dish', 'language']
            if not all(data.get(field) for field in required_fields):
                return jsonify({'error': 'All fields are required'}), 400

            new_recipe = Recipe(
                title=data['title'],
                description=data['description'],
                ingredients=data['ingredients'],
                instructions=data['instructions'],
                time_of_eat=data['time_of_eat'],
                type_of_dish=data['type_of_dish'],
                language=data['language'],
                user_id=current_user.id,
                created_at=datetime.utcnow()
            )
            db.session.add(new_recipe)
            db.session.commit()

            return jsonify({'message': 'Recipe submitted successfully'}), 201

        else:
            # ---- Web Form request ----
            title = request.form.get('title')
            description = request.form.get('description')
            ingredients = request.form.get('ingredients')
            instructions = request.form.get('instructions')
            time_of_eat = request.form.get('time_of_eat')
            type_of_dish = request.form.get('type_of_dish')
            language = request.form.get('language')
            file = request.files.get('image')

            if not all([title, description, ingredients, instructions, time_of_eat, type_of_dish, language]):
                flash('All fields are required.', 'danger')
                return redirect(request.url)

            filename = None
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)

            new_recipe = Recipe(
                title=title,
                description=description,
                ingredients=ingredients,
                instructions=instructions,
                time_of_eat=time_of_eat,
                type_of_dish=type_of_dish,
                language=language,
                image=filename,
                user_id=current_user.id,
                created_at=datetime.utcnow()
            )

            db.session.add(new_recipe)
            db.session.commit()
            flash('Recipe submitted successfully!', 'success')
            return redirect(url_for('main.home'))

    return render_template('submit_recipe.html')
