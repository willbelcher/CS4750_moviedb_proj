from django.contrib.auth.models import User
from django.db import connection

# add raw sql statements here
# https://docs.djangoproject.com/en/5.0/topics/db/sql/#executing-custom-sql-directly

def get_user(email):
    return User.objects.raw("SELECT * FROM user WHERE email=%s", [email])[0]

def get_reviews_by_user(email, limit=25):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM review WHERE email=%s LIMIT %s", [email, limit])
        return cursor.fetchall()
    

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM user WHERE email=%s", [email])
    #     return cursor.fetchone()