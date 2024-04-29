from mainapp.models import User
from django.db import connection

# From django documenation, converts row data to dict
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dictfetchone(cursor):
    res = cursor.fetchone()
    if not res:
        res = []

    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, res))

def get_user_model(email):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE email=%s", [email])
        user = cursor.fetchone()

    if user is not None:
        return User(email=user[0], name=user[1], password=user[3])
    
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
    
def get_movie(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM movie WHERE movie_id=%s", [id])
        movie = cursor.fetchone()

        if movie is not None:
            return movie

    return None

def get_movies(title=False, min_score=False, limit=30):
    with connection.cursor() as cursor:
        args = []
        query = "SELECT * FROM movie"
        if title or min_score:
            query += " WHERE"
        if title:
            query += " title LIKE %s"
            args.append('%' + title + '%')
        if min_score and title:
            query += " AND"
        if min_score:
            query += " average_review_score>=%s"
            args.append(min_score)
        args.append(limit)
        cursor.execute(query + " LIMIT %s", args)
        return dictfetchall(cursor)
    
# gets movie and all related information
def get_movies_full(title=False, min_score=False, get_watched=False, get_watchlist=False, limit=30):
    movies = get_movies(title, min_score)
    with connection.cursor() as cursor:
        for i, movie in enumerate(movies):
            cursor.execute("SELECT genre_name FROM movie_genre WHERE movie_id=%s LIMIT %s", [movie['movie_id'], limit])
            movies[i]['genres'] = ', '.join(x['genre_name'] for x in dictfetchall(cursor))
            cursor.execute("SELECT role, name FROM movie_cast WHERE movie_id=%s LIMIT %s", [movie['movie_id'], limit])
            movies[i]['cast'] = dictfetchall(cursor)
            cursor.execute("SELECT title, composer FROM movie_musicscores WHERE movie_id=%s LIMIT %s", [movie['movie_id'], limit])
            movies[i]['musicscores'] = dictfetchall(cursor)
            cursor.execute("SELECT award_name, year, did_win FROM movie_nominations WHERE movie_id=%s LIMIT %s", [movie['movie_id'], limit])
            movies[i]['awards'] = dictfetchall(cursor)

            if get_watchlist:
                cursor.execute("SELECT * FROM watchlist WHERE movie_id=%s AND email=%s", [movie['movie_id'], get_watchlist])
                movies[i]['watchlist'] = bool(len(dictfetchone(cursor)))
            if get_watched:
                cursor.execute("SELECT * FROM watched WHERE movie_id=%s AND email=%s", [movie['movie_id'], get_watched])
                movies[i]['watched'] = bool(len(dictfetchone(cursor)))

    return movies

def add_movie_to_watchlist(email, movie_id):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO watchlist (email, movie_id) VALUES (%s, %s)", [email, movie_id])

    return

def add_movie_to_watched(email, movie_id):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO watched (email, movie_id) VALUES (%s, %s)", [email, movie_id])

    return

def get_reviews_by_movie(id, limit=25):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM reviews WHERE movie_id =%s LIMIT %s", [id, limit])
    
def get_watchlist(email, limit=25):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM watchlist JOIN movie WHERE email =%s LIMIT %s", [email, limit])
        return cursor.fetchall()
    
def get_watched(email, limit=25):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM watched JOIN movie WHERE email =%s LIMIT %s", [email, limit])
        return cursor.fetchall()