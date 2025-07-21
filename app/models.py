# app/models.py
from datetime import datetime
from flask_login import UserMixin
from app import db

# Junction table for likes (many-to-many)
user_likes = db.Table(
    'user_likes',
    db.Column('user_id',   db.Integer, db.ForeignKey('user.id'),   primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(150), nullable=False, unique=True)
    email         = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    # Recipes THIS user authored
    recipes = db.relationship(
        'Recipe',
        back_populates='author',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    # Comments THIS user made
    comments = db.relationship(
        'Comment',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    # Recipes THIS user has liked
    liked_recipes = db.relationship(
        'Recipe',
        secondary=user_likes,
        back_populates='likers',
        lazy='dynamic'
    )


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(100), nullable=False)
    description  = db.Column(db.Text,   nullable=False)
    ingredients  = db.Column(db.Text,   nullable=False)
    instructions = db.Column(db.Text,   nullable=False)
    time_of_eat  = db.Column(db.String(50), nullable=False)
    type_of_dish = db.Column(db.String(50), nullable=False)
    language     = db.Column(db.String(50), nullable=False)
    image        = db.Column(db.String(200), nullable=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Who authored this recipe
    author = db.relationship(
        'User',
        back_populates='recipes',
        lazy='joined'
    )

    # Which users have liked this recipe
    likers = db.relationship(
        'User',
        secondary=user_likes,
        back_populates='liked_recipes',
        lazy='selectin'
    )

    # Comments on this recipe
    comments = db.relationship(
        'Comment',
        back_populates='recipe',
        cascade='all, delete-orphan',
        lazy='selectin'
    )


class Comment(db.Model):
    __tablename__ = 'comment'

    id         = db.Column(db.Integer, primary_key=True)
    content    = db.Column(db.Text,    nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'),   nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    # Who wrote this comment
    user = db.relationship(
        'User',
        back_populates='comments',
        lazy='joined'
    )

    # On which recipe
    recipe = db.relationship(
        'Recipe',
        back_populates='comments',
        lazy='joined'
    )
