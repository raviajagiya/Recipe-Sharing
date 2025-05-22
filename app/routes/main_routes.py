# app/routes/main_routes.py

from flask import Blueprint, render_template, request, jsonify
from app.models import Recipe
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    time_of_eat = request.args.get('time_of_eat')
    type_of_dish = request.args.get('type_of_dish')
    language = request.args.get('language')

    query = Recipe.query

    if time_of_eat:
        query = query.filter_by(time_of_eat=time_of_eat)
    if type_of_dish:
        query = query.filter_by(type_of_dish=type_of_dish)
    if language:
        query = query.filter_by(language=language)

    recipes = query.order_by(Recipe.created_at.desc()).all()

    if request.is_json:
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
                'image_url': url_for('static', filename=r.image) if r.image else None,
                'created_at': r.created_at.isoformat()
            }
            for r in recipes
        ])

    return render_template('home.html', recipes=recipes)
