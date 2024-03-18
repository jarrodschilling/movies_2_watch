from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.movie import Movie
from flask_app.models.user import User


@app.route('/dashboard')
def show_all():
    if 'user_id' not in session:
        return redirect('/')
    movies = Movie.get_all()
    return render_template('dashboard.html', movies=movies)


@app.route('/movies/new')
def new_movie():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new-movie.html')

@app.route('/movies/create', methods=['POST'])
def create_movie():
    if 'user_id' not in session:
        return redirect('/')
    if not Movie.validate_movie(request.form):
        return redirect('/movies/new')

    data = {
        'title': request.form['title'],
        'description': request.form['description'],
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
    subscribers = User.users_subscribed(data)
    return render_template('movie.html', movie=movie, subscribers=subscribers)


@app.route("/movies/delete/<int:id>")
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    Movie.delete_movie(data)
    return redirect('/user/account')