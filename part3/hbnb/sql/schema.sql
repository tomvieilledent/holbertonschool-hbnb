-- HBnB schema creation script (PostgreSQL)
-- Creates tables, constraints, foreign keys, and relationship table.

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY DEFAULT (gen_random_uuid()::text),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY DEFAULT (gen_random_uuid()::text),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    CONSTRAINT fk_places_owner
        FOREIGN KEY (owner_id)
        REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY DEFAULT (gen_random_uuid()::text),
    text TEXT,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    CONSTRAINT fk_reviews_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_reviews_place
        FOREIGN KEY (place_id)
        REFERENCES places(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT uq_reviews_user_place UNIQUE (user_id, place_id)
);

CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY DEFAULT (gen_random_uuid()::text),
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    CONSTRAINT pk_place_amenity PRIMARY KEY (place_id, amenity_id),
    CONSTRAINT fk_place_amenity_place
        FOREIGN KEY (place_id)
        REFERENCES places(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_place_amenity_amenity
        FOREIGN KEY (amenity_id)
        REFERENCES amenities(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

COMMIT;
