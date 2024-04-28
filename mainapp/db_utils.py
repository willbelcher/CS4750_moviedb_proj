from mainapp.models import User
from django.db import connection

# add raw sql statements here
# https://docs.djangoproject.com/en/5.0/topics/db/sql/#executing-custom-sql-directly

def get_user(email):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE email=%s", [email])
        user = cursor.fetchone()

    if user is not None:
        return User(email=user[0], name=user[1])
    
    return None


# returns true user does not already exist
def add_user(email, name, password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM user WHERE email=%s", [email])
        if cursor.fetchone() is not None:
            return False
        
        cursor.execute("INSERT INTO user (email, name, number_of_review, password) VALUES (%s, %s, %s, %s)", [email, name, 0, password])

    return True


def get_reviews_by_user(email, limit=25):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM review WHERE email=%s LIMIT %s", [email, limit])
        return cursor.fetchall()
    

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM user WHERE email=%s", [email])
    #     return cursor.fetchone()