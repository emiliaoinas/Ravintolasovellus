from app import app
from flask import render_template, request, redirect
from sqlalchemy.sql import text
import restaurants, reviews, users, maps
from db import db

@app.route("/")
def index():
    admin_status = users.is_admin()
    map = maps.create_map()
    return render_template("index.html", map = map, admin_status = admin_status)
    
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
        error_message = "Salasana tai käyttäjänimi on väärin"
        return render_template("login.html", error = error_message)

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
        if username == "" or password == "" or bool(username.strip()) == False or bool(password.strip()) == False:
            return render_template("register.html", error="Käyttäjänimi tai salasana ei voi olla tyhjä tai koostua pelkistä välilyönneistä")
        sql = text("SELECT 1 FROM users WHERE username = :username")
        result = db.session.execute(sql, {"username": username}).fetchone()
        if result:
            return render_template("register.html", error="Käyttäjänimi on jo käytössä")
        if users.register(username, password):
            return redirect("/")
            
@app.route("/admin_application", methods=["GET", "POST"])
def admin_application():
    if request.method == "GET":
        return render_template("admin_application.html")
    if request.method == "POST":
        application = request.form["application"]
        terms_accepted = "terms" in request.form
        if not terms_accepted:
            return render_template("admin_application.html", error = "Voidaksesi hakea ylläpitäjäksi, sinun on hyväksyttävä ehdot")
        if len(application.strip().split()) < 5:
            return render_template("admin_application.html", error = "Hakemuksesi on liian lyhyt, minimivaatimus on 5 sanaa")
        if users.is_admin:
            return render_template("admin_application.html", error = "Olet jo ylläpitäjä")
        success = users.admin_application(application)
        if success:
            return redirect("/")
        else:
            return render_template("admin_application.html", error="Hakemuksen lähettäminen epäonnistui. Yritä uudelleen.")

@app.route("/sorted_restaurants")
def show_restaurants():
    restaurant_list = restaurants.sorted_restaurants()
    return render_template('sorted_restaurants.html', listed_restaurants = restaurant_list)

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
    sql = text("SELECT id, restaurant_id, rating, comment, sent_at FROM reviews WHERE restaurant_id=:restaurant_id")
    result = db.session.execute(sql, {"restaurant_id": id})
    reviews = result.fetchall()
    return render_template("restaurant.html", restaurant=restaurant, reviews=reviews, restaurant_id = id, admin_status = admin_status)

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

@app.route("/delete_review", methods=["POST"])
def delete_review():
    review_id = request.form["review_id"]
    reviews.delete_review(review_id)
    return redirect("/")

@app.route("/delete_restaurant", methods=["POST"])
def delete_restaurant():
    restaurant_id = request.form["restaurant_id"]
    restaurants.delete_restaurant(restaurant_id)
    return redirect("/")
