from bs4 import BeautifulSoup
from flask_app.models import player
from flask import render_template, request, redirect, session, flash
from flask_app import app


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/process', methods=['POST'])
def process_file():
    file = request.files['stats']
    
    doc = BeautifulSoup(file, 'html.parser')
    player.Player.import_players(doc)
    return redirect('/stats')