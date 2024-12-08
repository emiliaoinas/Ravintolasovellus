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
        errors = []
        username = request.form["username"]
        password = request.form["password"]
        if username == "" or password == "" or bool(username.strip()) == False or bool(password.strip()) == False:
            errors.append("Käyttäjänimi tai salasana ei voi olla tyhjä tai koostua pelkistä välilyönneistä")
        sql = text("SELECT 1 FROM users WHERE username = :username")
        result = db.session.execute(sql, {"username": username}).fetchone()
        if result:
            errors.append("Käyttäjänimi on jo käytössä, valitse toinen nimi")
        if len(errors) > 0:
            return render_template("register.html", errors = errors)
        if users.register(username, password):
            return redirect("/")
            
@app.route("/admin_application", methods=["GET", "POST"])
def admin_application():
    if request.method == "GET":
        return render_template("admin_application.html")
    if request.method == "POST":
        errors = []
        application = request.form["application"]
        terms_accepted = "terms" in request.form
        if not terms_accepted:
            errors.append("Voidaksesi hakea ylläpitäjäksi, sinun on hyväksyttävä ehdot")
        if len(application.strip().split()) < 5:
            errors.append("Hakemuksesi on liian lyhyt, minimivaatimus on 5 sanaa")
        if users.is_admin():
            errors.append("Olet jo ylläpitäjä, sinun ei tarvitse hakea uudelleen")
        if len(errors) == 0:
            users.admin_application(application)
            return redirect("/")
        else:
            return render_template("admin_application.html", errors = errors)
            
@app.route("/sorted_restaurants")
def show_restaurants():
    restaurant_list = restaurants.sorted_restaurants()
    return render_template("sorted_restaurants.html", listed_restaurants = restaurant_list)

@app.route("/find_restaurant", methods=["GET", "POST"])
def search_restaurants():
    if request.method == "GET":
        return render_template("find_restaurant.html", results = None, error = None)
    if request.method == "POST":
        errors = []
        keyword = request.form["keyword"]
        if bool(keyword.strip()) == False:
            errors.append("Hakusana ei voi olla tyhjä!")
        if len(keyword.split()) > 1:
            errors.append("Hakusanoja voi olla vain yksi kerralla!")
        if len(errors) > 0:
            return render_template("find_restaurant.html", results = None, errors = errors)
        result = restaurants.find_restaurant(keyword)
        return render_template("find_restaurant.html", results = result, keyword = keyword)

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
    sql = text("SELECT id, restaurant_id, group_name FROM groups WHERE restaurant_id=:restaurant_id")
    result = db.session.execute(sql, {"restaurant_id": id})
    groups = result.fetchall()
    return render_template("restaurant.html", restaurant=restaurant, reviews=reviews, restaurant_id = id, admin_status = admin_status, groups = groups)

@app.route("/submit_review", methods=["POST"])
def submit_review():
    errors = []
    try:
        rating = int(request.form["rating"])
        if rating < 1 or rating > 5:
            errors.append("Arvosanan on oltava 1-5") 
    except ValueError:
        errors.append("Arvosanan on oltava kokonaisluku välillä 1-5.")

    comment = request.form["comment"].strip()
    if not comment:
        errors.append("Kommentti ei voi olla tyhjä tai koostua pelkistä välilyönneistä")
    restaurant_id = request.form["restaurant_id"]
    
    if len(errors) == 0:
        reviews.submit_review(rating, comment, restaurant_id)
        return redirect(f"/restaurant/{restaurant_id}")
    
    else: 
        admin_status = users.is_admin()
        sql = text("SELECT id, restaurant_name, opening_hours, restaurant_description FROM restaurants WHERE id=:id")
        result = db.session.execute(sql, {"id": restaurant_id})
        restaurant = result.fetchone()
        sql = text("SELECT id, restaurant_id, rating, comment, sent_at FROM reviews WHERE restaurant_id=:restaurant_id")
        result = db.session.execute(sql, {"restaurant_id": restaurant_id})
        all_reviews = result.fetchall()
        return render_template("restaurant.html", restaurant = restaurant, reviews = all_reviews, restaurant_id = restaurant_id, admin_status = admin_status, errors = errors)

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

@app.route("/add_group", methods=["POST"])
def add_group():
    errors = []
    restaurant_id = request.form["restaurant_id"]
    group_name = request.form["group_name"]
    if bool(group_name.strip()) == False:
        errors.append("Ryhmän nimi ei voi olla tyhjä!")
    if len(errors) == 0:
        restaurants.add_group(restaurant_id, group_name)
        return redirect("/")
    else:
        admin_status = users.is_admin()
        sql = text("SELECT id, restaurant_name, opening_hours, restaurant_description FROM restaurants WHERE id=:id")
        result = db.session.execute(sql, {"id": restaurant_id})
        restaurant = result.fetchone()
        sql = text("SELECT id, restaurant_id, rating, comment, sent_at FROM reviews WHERE restaurant_id=:restaurant_id")
        result = db.session.execute(sql, {"restaurant_id": restaurant_id})
        all_reviews = result.fetchall()
        return render_template("restaurant.html", restaurant = restaurant, reviews = all_reviews, restaurant_id = restaurant_id, admin_status = admin_status, errors = errors)
