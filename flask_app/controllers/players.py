from bs4 import BeautifulSoup
from flask_app.models import player, user
from flask import render_template, request, redirect, session, flash
from flask_app import app



@app.route('/')
def home():
    if 'id' in session:
        data = {
            'id' : session['id']
        }
        return render_template('home.html', current_user=user.User.get_by_id(data))
    else:
        return render_template('login.html')

@app.route('/process', methods=['POST'])
def process_file():
    file = request.files['stats']
    
    doc = BeautifulSoup(file, 'html.parser')
    player.Player.import_players(doc)
    return redirect('/stats')

@app.route('/stats')
def stat_page():
    if 'id' in session:
        data = {
            'id': session['id']
        }
        return render_template('stats.html', all_players = player.Player.get_all_players(), watchlist_players=user.User.check_watchlist(data))
    else:
        flash('You must be logged in to view that page.', 'login')
        return redirect('/')