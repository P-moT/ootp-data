from bs4 import BeautifulSoup
from flask_app.models import player, user
from flask import render_template, request, redirect, session, flash
from flask_app import app



@app.route('/')
def home():
    if 'id' in session:
        return render_template('home.html')
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
    return render_template('stats.html', all_players = player.Player.get_all_players())