CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    restaurant_name TEXT,
    opening_hours TEXT,
    restaurant_description TEXT,
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants,
    user_id INTEGER REFERENCES users,
    rating INTEGER,
    comment TEXT,
    sent_at TIMESTAMP
);
