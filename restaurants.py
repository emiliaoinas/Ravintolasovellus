from db import db
from flask import request
from sqlalchemy.sql import text

def add_restaurant():
    restaurant_name = request.form["restaurant_name"]
    opening_hours = request.form["opening_hours"]
    restaurant_description = request.form["restaurant_description"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]
    sql = text("INSERT INTO restaurants (restaurant_name, opening_hours, restaurant_description, latitude, longitude) VALUES (:restaurant_name, :opening_hours, :restaurant_description, :latitude, :longitude) RETURNING id")
    db.session.execute(sql, {"restaurant_name": restaurant_name,"opening_hours": opening_hours,"restaurant_description": restaurant_description, "latitude": latitude, "longitude": longitude})
    db.session.commit()
    return True
