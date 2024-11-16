from app import app
from flask import render_template, request, redirect
from sqlalchemy.sql import text
import restaurants, reviews, users
from db import db

@app.route("/")
def index():
    sql = text("SELECT id, restaurant_name FROM restaurants")
    result = db.session.execute(sql)
    restaurants = result.fetchall()
    return render_template("index.html", restaurants = restaurants)
    
@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message = "Kirjautuminen ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message = "Rekisteröityminen ei onnistunut")

@app.route("/create", methods=["POST"])
def create():
    restaurants.add_restaurant()
    return redirect("/")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/restaurant/<int:id>")
def restaurant(id):
    sql = text("SELECT id, restaurant_name, opening_hours, restaurant_description FROM restaurants WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    restaurant = result.fetchone()
    sql = text("SELECT restaurant_id, rating, comment FROM reviews WHERE restaurant_id=:restaurant_id")
    result = db.session.execute(sql, {"restaurant_id": id})
    reviews = result.fetchall()
    return render_template("restaurant.html", restaurant=restaurant, reviews=reviews, restaurant_id = id)

@app.route("/submit_review", methods=["POST"])
def submit_review():
    rating = request.form["rating"]
    comment = request.form["comment"]
    restaurant_id = request.form["restaurant_id"]
    submission = reviews.submit_review(rating, comment, restaurant_id)
    if submission:
        return redirect(f"/restaurant/{restaurant_id}")
    else:
        return render_template("error.html", message = "Palautteen lähettäminen ei onnistunut")