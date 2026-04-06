#!/usr/bin/python3
"""Script to create a test user for testing the authentication system."""

from app import create_app, db
from app.services import facade

# Create app and context
app = create_app()

with app.app_context():
    # Create tables if they don't exist
    db.create_all()

    # Check if user already exists
    existing_user = facade.get_user_by_email('test@hbnb.io')

    if existing_user:
        print(f"✓ User already exists: {existing_user.email}")
    else:
        # Create a new test user
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@hbnb.io',
            'password': 'password123',
            'is_admin': False
        }

        user = facade.create_user(user_data)
        print(f"✓ Test user created successfully!")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.first_name} {user.last_name}")
        print(f"  Admin: {user.is_admin}")
        print(f"  ID: {user.id}")

    # Also create an admin user if it doesn't exist
    admin_user = facade.get_user_by_email('admin@hbnb.io')
    if admin_user:
        print(f"✓ Admin user already exists: {admin_user.email}")
    else:
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'HBnB',
            'email': 'admin@hbnb.io',
            'password': 'admin123',
            'is_admin': True
        }

        admin = facade.create_user(admin_data)
        print(f"✓ Admin user created successfully!")
        print(f"  Email: {admin.email}")
        print(f"  Name: {admin.first_name} {admin.last_name}")
        print(f"  Admin: {admin.is_admin}")
        print(f"  ID: {admin.id}")

    print("\nYou can now login with:")
    print("  Email: test@hbnb.io")
    print("  Password: password123")
