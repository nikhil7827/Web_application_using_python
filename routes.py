from flask import Blueprint, request, jsonify
from blog_models import db, BlogPost
from sqlalchemy import or_

bp = Blueprint("posts", __name__)

@bp.route("/", methods=["POST"])
def create_post():
    data = request.json
    required_fields = ["title", "content", "category", "tags"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    post = BlogPost(**data)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@bp.route("/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = BlogPost.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.json
    for key in ["title", "content", "category", "tags"]:
        if key in data:
            setattr(post, key, data[key])

    db.session.commit()
    return jsonify(post.to_dict()), 200

@bp.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    if not post:
        return "", 404
    db.session.delete(post)
    db.session.commit()
    return "", 204

@bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = BlogPost.query.get(post_id)
    if not post:
        return "", 404
    return jsonify(post.to_dict()), 200

@bp.route("/", methods=["GET"])
def get_all_posts():
    term = request.args.get("term")
    query = BlogPost.query
    if term:
        query = query.filter(
            or_(
                BlogPost.title.ilike(f"%{term}%"),
                BlogPost.content.ilike(f"%{term}%"),
                BlogPost.category.ilike(f"%{term}%"),
            )
        )
    posts = query.all()
    return jsonify([post.to_dict() for post in posts]), 200
