from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = 'ootp_players'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']

    @staticmethod
    def validate_reg(user):
        valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        query2 = "SELECT * FROM users WHERE username = %(username)s"
        if len(user['first_name']) < 3:
            valid = False
            flash('First name must be 3 or more characters.', 'register')
        if len(user['last_name']) < 3:
            valid = False
            flash('Last name must be 3 or more characters.', 'register')
        if len(user['username']) < 3:
            valid = False
            flash('User name must be 3 or more characters.', 'register')
        if not EMAIL_REGEX.match(user['email']):
            valid = False
            flash('Invalid email address.', 'register')
        if user['password'] != user['confirmpw']:
            valid = False
            print(user['password'])
            print(user['confirmpw'])
            flash('Passwords do not match.', 'register')
        if len(connectToMySQL(db).query_db(query, user)) > 0:
            valid = False
            flash('Email already in use.', 'register')
        if len(connectToMySQL(db).query_db(query2, user)) > 0:
            valid = False
            flash('Username taken.', 'register')
        return valid

    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, username, email, password) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_username(cls, data):
        query = 'SELECT * FROM users WHERE username = %(username)s;'
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        else:
            return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        else:
            return cls(results[0])