from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Movie:
    db = "belt_exam_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['friend']
        self.date = data['date']
        self.watched = data['watched']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.movie_user = None


    @classmethod
    def save_movie(cls, data):
        query = """INSERT INTO movies (title, friend, date, watched)
                VALUES (%(title)s, %(friend)s, %(date)s, %(watched)s, %(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_one_movie_by_id(cls, data):
        query = """SELECT * FROM magazines WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])
    


    

    @classmethod
    def get_users_movies(cls, data):
        query = """SELECT * FROM movies
                WHERE user_id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        movies = []
        if results:
            for row in results:
                a_movie = cls(row)
                movies.append(a_movie)
        return movies

    @classmethod
    def delete_movie(cls, data):
        query = """DELETE FROM movies WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def update_movie(cls, data):
        query = """UPDATE movies SET name = %(title)s, friend = %(friend)s,
                date = %(date)s, watched = %(watched)s 
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def get_by_title(cls, title_data):
        data = {
            'title': title_data
        }
        query = """SELECT * FROM movies WHERE title = %(title)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM movies
                JOIN users ON users.id = movies.user_id;"""
        results = connectToMySQL(cls.db).query_db(query)
        movies = []
        if results:
            for row in results:
                one_movie = cls(row)
                movie_user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                one_movie.movie_user = user.User(movie_user_data)
                movies.append(one_movie)
        return movies
    
    
    @staticmethod
    def validate_movie(data):
        is_valid = True
        if len(data['title']) < 2:
            flash("Title must be at least 2 characters")
            is_valid = False
        if len(data['friend']) < 2:
            flash("Friend must be at least 10 characters")
            is_valid = False
        if Movie.get_by_title(data['title']) != False:
            flash("Title already exists")
            is_valid = False

        return is_valid