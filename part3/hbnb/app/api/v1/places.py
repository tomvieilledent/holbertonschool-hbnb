"""Place API endpoints."""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Place operations')


def _serialize_owner(owner):
    """Serialize an owner object for API output."""
    if not owner:
        return None
    return {
        'id': owner.id,
        'first_name': owner.first_name,
        'last_name': owner.last_name,
        'email': owner.email,
    }


def _serialize_amenity(amenity):
    """Serialize an amenity object for API output."""
    return {
        'id': amenity.id,
        'name': amenity.name,
    }


def _serialize_review(review):
    """Serialize a review object for API output."""
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user.id if review.user else None,
    }


# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    """Collection endpoints for places."""

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload
        place_data["owner_id"] = current_user
        try:
            new_place = facade.create_place(place_data)
        except (TypeError, ValueError) as exc:
            return {'message': str(exc)}, 400
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner.id if new_place.owner else None,
            'amenities': [amenity.id for amenity in new_place.amenities],
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [
            {
                'id': u.id,
                'title': u.title,
                'price': u.price,
            }
            for u in places
        ], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """Item endpoints for a single place."""

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': _serialize_owner(place.owner),
            'amenities': [_serialize_amenity(amenity) for amenity in place.amenities],
            'reviews': [_serialize_review(review) for review in place.reviews],
        }, 200

    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload or {}
        current_user_id = get_jwt_identity()
        current_user_claims = get_jwt()
        is_admin = current_user_claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404

        if not is_admin and (not place.owner or str(place.owner.id) != str(current_user_id)):
            return {'message': 'Unauthorized action.'}, 403

        # Owner must come from auth context, never from request payload.
        if data and 'owner_id' in data:
            del data['owner_id']

        try:
            place = facade.update_place(place_id, data)
        except ValueError as exc:
            if str(exc) == 'Place not found':
                return {'message': 'Place not found'}, 404
            return {'message': str(exc)}, 400
        except TypeError as exc:
            return {'message': str(exc)}, 400

        if not place:
            return {'message': 'Place not found'}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id if place.owner else None,
            'amenities': [amenity.id for amenity in place.amenities],
        }, 200

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Forbidden')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404

        current_user_id = get_jwt_identity()
        current_user_claims = get_jwt()
        is_admin = current_user_claims.get('is_admin', False)

        # Admins can delete any place; non-admins can only delete their own
        if not is_admin and (not place.owner or str(place.owner.id) != str(current_user_id)):
            return {'message': 'Unauthorized action.'}, 403

        try:
            facade.delete_place(place_id)
            return {'message': 'Place deleted successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 404


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    """Endpoint to list reviews for a place."""

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            }
            for review in reviews
        ], 200
