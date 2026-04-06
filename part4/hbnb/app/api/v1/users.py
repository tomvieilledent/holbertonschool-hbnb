"""User API endpoints."""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

# Model pour CREATE (POST)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='Admin flag')
})

# Model pour UPDATE (PUT) - champs optionnels
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='Admin flag')
})


@api.route('/')
class UserList(Resource):
    """Collection endpoints for users."""

    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        user_data = api.payload
        current_user = get_jwt()

        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Validate required fields
        required_fields = {'first_name', 'last_name', 'email', 'password'}
        if not user_data or not required_fields.issubset(user_data):
            return {'message': 'Invalid input data'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'message': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except (TypeError, ValueError) as exc:
            return {'message': str(exc)}, 400
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Retrieve the list of users"""
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            }
            for u in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """Item endpoints for a single user."""

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        data = api.payload or {}
        current_user_id = get_jwt_identity()
        current_user_claims = get_jwt()
        is_admin = current_user_claims.get('is_admin', False)

        if not is_admin and str(user_id) != str(current_user_id):
            return {'message': 'Unauthorized action.'}, 403

        if not is_admin:
            forbidden_fields = {'email', 'password', 'is_admin'}
            if any(field in data for field in forbidden_fields):
                return {'message': 'You cannot modify email or password.'}, 400

        try:
            user = facade.update_user(user_id, data)
        except ValueError as exc:
            if str(exc) == 'User not found':
                return {'message': 'User not found'}, 404
            return {'message': str(exc)}, 400
        except TypeError as exc:
            return {'message': str(exc)}, 400

        if not user:
            return {'message': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
