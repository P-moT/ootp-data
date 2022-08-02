from bs4 import BeautifulSoup
from flask_app.config.mysqlconnetcion import connectToMySQL
from flask import flash, session
db = 'ootp_players'

class Player:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.position = data['position']
        self.rating = data['rating']
        self.card_id = data['card_id']

    @classmethod
    def import_players(cls, doc):
        dict_keys = ['position', 'first_name', 'last_name', 'rating', 'card_id']
        table = doc.find(class_='data sortable')
        # print(table)
        index = 1
        tbody = table.find_all('tr')
        print(tbody)
        for row in tbody:
            def not_null(s):
                return (s != '\n')
            if index == len(tbody):
                break
            dict_values = tbody[index].find_all(string=not_null)
            data = dict(zip(dict_keys, dict_values))
            print(data)
            query = "SELECT * FROM players WHERE card_id = %(card_id)s"
            results = connectToMySQL(db).query_db(query, data)
            if len(results) > 0:
                index += 1
            else:
                query = "INSERT INTO players (first_name, last_name, position, rating, card_id) VALUES (%(first_name)s, %(last_name)s, %(position)s, %(rating)s, %(card_id)s)"
                index += 1
                connectToMySQL(db).query_db(query, data)



