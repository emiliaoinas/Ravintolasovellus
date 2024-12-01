CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT,
);

CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    application TEXT,
    start_time TIMESTAMP
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

CREATE TABLE hidden(
    id SERIAL PRIMARY KEY, 
    review_id INTEGER REFERENCES reviews,
    reason TEXT
);
