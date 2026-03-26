-- HBnB initial data seed script (PostgreSQL)
-- Inserts a fixed administrator account and initial amenities.

BEGIN;

INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$31oqrGPWKbPJOMPl8Xj0l.8bW0Pdk/A53OciG3psRyP14gF8zaPOW',
    TRUE
)
ON CONFLICT (email) DO NOTHING;

INSERT INTO amenities (id, name)
VALUES
    ('9d4b2ac6-ac14-41da-9500-ccfd73ac1211', 'WiFi'),
    ('a30aa3c8-d699-411f-a839-3d2b36b949a9', 'Swimming Pool'),
    ('47a0d396-5f27-42dc-a139-6526e4fa7ec7', 'Air Conditioning')
ON CONFLICT (name) DO NOTHING;

COMMIT;
