from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import player, user
bcrypt = Bcrypt(app)

@app.route('/new_user', methods=['POST'])
def add_user():
    if not request.form['password']:
        flash('Password field cannot be empty', 'register')
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': pw_hash
    }
    form = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirmpw': request.form['confirmpw']
    }
    
    if not user.User.validate_reg(form):
        return redirect('/')
    else:
        session['id'] = user.User.add_user(data)
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'username': request.form['username']
    }
    this_user = user.User.get_by_username(data)
    if not this_user:
        flash('Invalid Email or Password.', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash('Invalid Email or Password.', 'login')
        return redirect('/')
    session['id'] = this_user.id
    return redirect('/')

@app.route('/user/<int:id>')
def profile(id):
    if 'id' in session:
        data = {
            'id': id
        }
        return render_template('profile.html', this_user = user.User.get_by_id(data), watchlist_players=user.User.get_user_watchlist(data))
    else:
        flash('You must be logged in to view that page.', 'login')
        return redirect('/')

@app.route('/add_to_list/<int:pid>/<int:uid>')
def add_to_list(pid, uid):
    data = {
        'pid': pid,
        'uid': uid
    }
    user.User.add_to_list(data)
    return redirect('/stats')

@app.route('/delete/<int:pid>/<int:uid>')
def delete(pid, uid):
    data = {
        'pid': pid,
        'uid': uid
    }
    user.User.delete_from_list(data)
    return redirect(request.referrer)