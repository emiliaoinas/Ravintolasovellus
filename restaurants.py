from db import db
from flask import request
from sqlalchemy.sql import text
import users

# For now everyone can add a restaurant
def add_restaurant():
    restaurant_name = request.form["restaurant_name"]
    opening_hours = request.form["opening_hours"]
    restaurant_description = request.form["restaurant_description"]
    sql = text("INSERT INTO restaurants (restaurant_name, opening_hours, restaurant_description) VALUES (:restaurant_name, :opening_hours, :restaurant_description) RETURNING id")
    db.session.execute(sql, {"restaurant_name": restaurant_name,"opening_hours": opening_hours,"restaurant_description": restaurant_description})
    db.session.commit()
    return True
    
# Below a version of the code for when the way to assign admins is ready
#def add_restaurant():
#    if users.is_admin():
#        restaurant_name = request.form["restaurant_name"]
#        opening_hours = request.form["opening_hours"]
#        restaurant_description = request.form["restaurant_description"]
#        sql = text("INSERT INTO restaurants (restaurant_name, opening_hours, restaurant_description) VALUES (:restaurant_name, :opening_hours, :restaurant_description) RETURNING id")
#        result = db.session.execute(sql, {"restaurant_name": restaurant_name, "opening_hours": opening_hours,"restaurant_description": restaurant_description})
#        db.session.commit()
#        return True

""" A html code for this to be used later: {% if session.get("is_admin") %}
<b><a href="/new">Lisää uusi ravintola</a></b>
{% endif %} """