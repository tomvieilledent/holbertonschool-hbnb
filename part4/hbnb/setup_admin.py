#!/usr/bin/python3
"""Script to create or update the admin user."""

from app import create_app, db
from app.models.user import User
from app.services import facade

# Create app and context
app = create_app()

with app.app_context():
    # Create tables if they don't exist
    db.create_all()

    # Check if admin@admin.com exists
    admin = facade.get_user_by_email('admin@admin.com')

    if admin:
        # Update existing user to be admin
        admin.is_admin = True
        db.session.commit()
        print(f"✓ Admin user updated: {admin.email}")
        print(f"  Name: {admin.first_name} {admin.last_name}")
        print(f"  Admin: {admin.is_admin}")
    else:
        # Create new admin user
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@admin.com',
            'password': 'admin',
            'is_admin': True
        }

        admin = facade.create_user(admin_data)
        print(f"✓ Admin user created successfully!")
        print(f"  Email: {admin.email}")
        print(f"  Name: {admin.first_name} {admin.last_name}")
        print(f"  Admin: {admin.is_admin}")
        print(f"  ID: {admin.id}")
