from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import secrets

def register(username, password):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()
    return login(username, password)

def login(username, password):
    session["csrf_token"] = secrets.token_hex(16)
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
        return True
    else:
        return False
        
def logout():
    del session["user_id"]
        
def user_id():
    return session.get("user_id", 0)

def admin_application(application):
    user_id = session.get("user_id")
    sql = text("INSERT INTO admins (user_id, application, start_time) VALUES (:user_id, :application, NOW())")
    db.session.execute(sql, {"user_id": user_id, "application": application})
    db.session.commit()
    return True

def is_admin():
    user_id = session.get("user_id")
    sql = text("SELECT 1 FROM admins WHERE user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    return bool(result)
