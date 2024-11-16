from db import db
from sqlalchemy.sql import text
import users

def submit_review(rating, comment, restaurant_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO reviews (restaurant_id, user_id, rating, comment, sent_at) VALUES (:restaurant_id, :user_id, :rating, :comment, NOW())")
    db.session.execute(sql, {"restaurant_id": restaurant_id, "rating": rating, "comment": comment, "user_id": user_id})
    db.session.commit()
    return True