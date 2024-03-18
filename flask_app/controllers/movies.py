from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.movie import Movie
from flask_app.models.user import User
from flask_app.static.utils.helpers import api_call


@app.route('/dashboard')
def show_all():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'users_id': session['user_id']
    }
    movies = Movie.get_users_movies(data)
    display_movies = []
    for movie in movies:
        store_movie = api_call(movie.title)
        display_movies.append(store_movie)
    return render_template('dashboard.html', movies=movies, display_movies=display_movies)


@app.route('/movies/new')
def new_movie():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new-movie.html')

@app.route('/movies/create', methods=['POST'])
def create_movie():
    if 'user_id' not in session:
        return redirect('/')
    # if not Movie.validate_movie(request.form):
    #     return redirect('/movies/new')

    print(request.form.get('watched'))

    data = {
        'title': request.form['title'],
        'friend': request.form['friend'],
        'date': request.form['date'],
        'watched': request.form.get('watched'),
        'user_id': session['user_id']
    }

    Movie.save_movie(data)
    return redirect('/dashboard')


@app.route('/movies/<int:id>')
def get_one_movie(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    movie = Movie.get_one_movie_by_id(data)
    return render_template('movie.html', movie=movie)


@app.route("/movies/edit/<int:id>")
def update_recipe_page(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    movie = Movie.get_one_movie_by_id(data)
    return render_template('edit.html', movie=movie)


@app.route("/movies/update", methods=['POST'])
def update_recipe():
    print(request.form)
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': request.form['id'],
        'title': request.form['title'],
        'friend': request.form['friend'],
        'date': request.form['date'],
        'watched': request.form.get('watched'),
    }

    recipe_update = Movie.update_movie(data)
    return redirect('/dashboard')

@app.route("/movies/delete/<int:id>")
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    Movie.delete_movie(data)
    return redirect('/user/account')