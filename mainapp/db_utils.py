from mainapp.models import User
from django.db import connection

# add raw sql statements here
# https://docs.djangoproject.com/en/5.0/topics/db/sql/#executing-custom-sql-directly

# From django documenation, converts row data to dict
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dictfetchone(cursor):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))

def get_user_model(email):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE email=%s", [email])
        user = cursor.fetchone()

    if user is not None:
        return User(email=user[0], name=user[1], password=user[3], number_reviews=user[2])
    
    return None

def get_user(email):
    with connection.cursor() as cursor:
        cursor.execute("SELECT email, name, number_reviews FROM user WHERE email=%s", [email])
        user = dictfetchone(cursor)  

    return user


# returns true user does not already exist
def add_user(email, name, password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM user WHERE email = %s", [email])
        if cursor.fetchone()[0] != 0:
            return False
        
        cursor.execute("INSERT INTO user (email, name, number_reviews, password) VALUES (%s, %s, %s, %s)", [email, name, 0, password])

    return True


def get_reviews_by_user(email, limit=25):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM reviews WHERE email=%s LIMIT %s", [email, limit])
        return cursor.fetchall()
    
def get_movies(title=False, min_score=False, limit=25):
    with connection.cursor() as cursor:
        args = []
        query = "SELECT * FROM movie WHERE"
        if title:
            query += " title LIKE %s"
            args.append(title+'%')
        if min_score and title:
            query += " AND"
        if min_score:
            query += " average_review_score>=%s"
            args.append(min_score)

        args.append(limit)

        cursor.execute(query + " LIMIT %s", args)
        return dictfetchall(cursor)
    
# gets movie and all related information
def get_movies_full(title=False, min_score=False, limit=25):
    movies = get_movies(title, min_score)
    with connection.cursor() as cursor:
        pass
    

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM user WHERE email=%s", [email])
    #     return cursor.fetchone()