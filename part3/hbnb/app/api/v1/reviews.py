"""Review API endpoints."""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Define the review update model (only text and rating can be updated)
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

# Helper functions for serialization


def _serialize_user(user):
    """Serialize a user object for API output."""
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }


def _serialize_place(place):
    """Serialize a place object for API output."""
    return {
        'id': place.id,
        'title': place.title,
        'latitude': place.latitude,
        'longitude': place.longitude
    }


@api.route('/')
class ReviewList(Resource):
    """Collection endpoints for reviews."""

    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        data = api.payload or {}

        if 'place_id' not in data or 'text' not in data or 'rating' not in data:
            return {'message': 'Invalid input data'}, 400

        place = facade.get_place(data['place_id'])
        if not place:
            return {'message': 'Place not found'}, 404

        if place.owner and str(current_user) == str(place.owner.id):
            return {'message': 'You cannot review your own place.'}, 400

        existing_reviews = facade.get_reviews_by_place(data['place_id'])
        if any(str(r.user.id) == str(current_user) for r in existing_reviews):
            return {'message': 'You have already reviewed this place'}, 400

        user = facade.get_user(current_user)
        if not user:
            return {'message': 'User not found'}, 404

        review_data = {
            'text': data['text'],
            'rating': data['rating'],
            'place': place,
            'user': user
        }

        try:
            review = facade.create_review(review_data)
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            }, 201
        except (TypeError, ValueError) as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            }
            for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    """Item endpoints for a single review."""

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Forbidden')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        current_user = get_jwt_identity()
        if not review.user or str(review.user.id) != str(current_user):
            return {'message': 'Unauthorized action.'}, 403

        data = api.payload or {}

        if 'text' not in data or 'rating' not in data:
            return {'message': 'Invalid input data'}, 400

        # Prepare update data (only text and rating)
        update_data = {
            'text': data['text'],
            'rating': data['rating']
        }

        try:
            facade.update_review(review_id, update_data)
            return {'message': 'Review updated successfully'}, 200
        except (TypeError, ValueError) as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        current_user = get_jwt_identity()

        if not review.user or str(review.user.id) != str(current_user):
            return {'message': 'Unauthorized action.'}, 403

        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 404
