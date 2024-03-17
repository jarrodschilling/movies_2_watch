from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_reg(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'email': request.form['email'],
        'password': pw_hash
    }

    user_id = User.save_one(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user_in_db  = User.get_one(request.form['email'])

    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name

    return redirect('/dashboard')

@app.route('/user/account')
def user_account():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    current_user = User.get_user_by_id(data)
    movies = Movie.get_users_magazines(data)

    return render_template('account.html', user=current_user, movies=movies)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')