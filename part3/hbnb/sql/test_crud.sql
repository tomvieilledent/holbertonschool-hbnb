-- HBnB SQL validation script (PostgreSQL)
-- Verifies table creation, seed data, and CRUD operations.

BEGIN;

-- 1) Validate seeded admin and amenities
SELECT id, email, is_admin
FROM users
WHERE email = 'admin@hbnb.io';

SELECT id, name
FROM amenities
WHERE name IN ('WiFi', 'Swimming Pool', 'Air Conditioning')
ORDER BY name;

-- 2) CREATE test user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '11111111-1111-4111-8111-111111111111',
    'Test',
    'Owner',
    'owner.test@hbnb.io',
    '$2b$12$31oqrGPWKbPJOMPl8Xj0l.8bW0Pdk/A53OciG3psRyP14gF8zaPOW',
    FALSE
)
ON CONFLICT (email) DO NOTHING;

-- 3) CREATE test place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    '22222222-2222-4222-8222-222222222222',
    'SQL Test Place',
    'Created by test_crud.sql',
    99.99,
    48.8566,
    2.3522,
    '11111111-1111-4111-8111-111111111111'
)
ON CONFLICT (id) DO NOTHING;

-- 4) CREATE place-amenity association
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    '22222222-2222-4222-8222-222222222222',
    '9d4b2ac6-ac14-41da-9500-ccfd73ac1211'
)
ON CONFLICT (place_id, amenity_id) DO NOTHING;

-- 5) CREATE review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    '33333333-3333-4333-8333-333333333333',
    'Great place from SQL test',
    5,
    '11111111-1111-4111-8111-111111111111',
    '22222222-2222-4222-8222-222222222222'
)
ON CONFLICT (id) DO NOTHING;

-- 6) READ checks
SELECT p.id, p.title, u.email AS owner_email
FROM places p
JOIN users u ON u.id = p.owner_id
WHERE p.id = '22222222-2222-4222-8222-222222222222';

SELECT r.id, r.rating, r.user_id, r.place_id
FROM reviews r
WHERE r.id = '33333333-3333-4333-8333-333333333333';

-- 7) UPDATE checks
UPDATE places
SET price = 120.00
WHERE id = '22222222-2222-4222-8222-222222222222';

UPDATE reviews
SET rating = 4
WHERE id = '33333333-3333-4333-8333-333333333333';

SELECT id, price
FROM places
WHERE id = '22222222-2222-4222-8222-222222222222';

SELECT id, rating
FROM reviews
WHERE id = '33333333-3333-4333-8333-333333333333';

-- 8) DELETE checks
DELETE FROM reviews
WHERE id = '33333333-3333-4333-8333-333333333333';

DELETE FROM place_amenity
WHERE place_id = '22222222-2222-4222-8222-222222222222'
  AND amenity_id = '9d4b2ac6-ac14-41da-9500-ccfd73ac1211';

DELETE FROM places
WHERE id = '22222222-2222-4222-8222-222222222222';

DELETE FROM users
WHERE id = '11111111-1111-4111-8111-111111111111';

-- 9) Final existence checks (should return 0 rows)
SELECT id FROM reviews WHERE id = '33333333-3333-4333-8333-333333333333';
SELECT id FROM places WHERE id = '22222222-2222-4222-8222-222222222222';
SELECT id FROM users WHERE id = '11111111-1111-4111-8111-111111111111';

COMMIT;
