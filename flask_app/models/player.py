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
        self.G = data['G']
        self.PA = data['PA']
        self.AB = data['AB']
        self.H = data['H']
        self.HR = data['HR']
        self.RBI = data['RBI']
        self.R = data['R']
        self.BB = data['BB']
        self.IBB = data['IBB']
        self.HBP = data['HBP']
        self.SF = data['SF']
        self.SO = data['SO']
        self.GIDP = data['GIDP']
        self.TB = data['TB']
        self.SB = data['SB']
        self.CS = data['CS']

    @classmethod
    def import_players(cls, doc):
        dict_keys = ['position', 'first_name', 'last_name', 'rating', 'card_id', 'G', 'PA', 'AB', 'H', 'HR', 'RBI', 'R', 'BB', 'IBB', 'HBP', 'SF', 'SO', 'GIDP', 'TB', 'SB', 'CS']
        table = doc.find(class_='data sortable')
        # print(table)
        index = 1
        tbody = table.find_all('tr')
        # print(tbody)
        for row in tbody:
            def not_null(s):
                return (s != '\n')
            if index == len(tbody):
                break
            dict_values = tbody[index].find_all(string=not_null)
            data = dict(zip(dict_keys, dict_values))
            # print(data)
            query = "SELECT * FROM players WHERE card_id = %(card_id)s"
            results = connectToMySQL(db).query_db(query, data)
            if len(results) > 0:
                card_id = {
                'card_id': results[0]['card_id']
                }
                query = "SELECT * FROM players WHERE card_id = %(card_id)s"
                results = connectToMySQL(db).query_db(query, card_id)
                new_data = {}
                new_data['G'] = (int(results[0]['G']) + int(data['G']))
                new_data['PA'] = (int(results[0]['PA']) + int(data['PA']))
                new_data['AB'] = (int(results[0]['AB']) + int(data['AB']))
                new_data['H'] = (int(results[0]['H']) + int(data['H']))
                new_data['HR'] = (int(results[0]['HR']) + int(data['HR']))
                new_data['RBI'] = (int(results[0]['RBI']) + int(data['RBI']))
                new_data['R'] = (int(results[0]['R']) + int(data['R']))
                new_data['BB'] = (int(results[0]['BB']) + int(data['BB']))
                new_data['IBB'] = (int(results[0]['IBB']) + int(data['IBB']))
                new_data['HBP'] = (int(results[0]['HBP']) + int(data['HBP']))
                new_data['SF'] = (int(results[0]['SF']) + int(data['SF']))
                new_data['SO'] = (int(results[0]['SO']) + int(data['SO']))
                new_data['GIDP'] = (int(results[0]['GIDP']) + int(data['GIDP']))
                new_data['TB'] = (int(results[0]['TB']) + int(data['TB']))
                new_data['SB'] = (int(results[0]['SB']) + int(data['SB']))
                new_data['CS'] = (int(results[0]['CS']) + int(data['CS']))
                new_data['card_id'] = results[0]['card_id']
                if data['position'] not in results[0]['position']:
                    new_data['position'] = results[0]['position'] + ', ' + data['position']
                else:
                    new_data['position'] = results[0]['position']
                update_query = "UPDATE players SET position = %(position)s, G = %(G)s, PA = %(PA)s, AB = %(AB)s, H = %(H)s, HR = %(HR)s, RBI = %(RBI)s, R = %(R)s, BB = %(BB)s, IBB = %(IBB)s, HBP = %(HBP)s, SF = %(SF)s, SO = %(SO)s, GIDP = %(GIDP)s, TB = %(TB)s, SB = %(SB)s, CS = %(CS)s WHERE card_id = %(card_id)s"
                connectToMySQL(db).query_db(update_query, new_data)
                index += 1
            else:
                query = "INSERT INTO players (first_name, last_name, position, rating, card_id, G, PA, AB, H, HR, RBI, R, BB, IBB, HBP, SF, SO, GIDP, TB, SB, CS) VALUES (%(first_name)s, %(last_name)s, %(position)s, %(rating)s, %(card_id)s, %(G)s, %(PA)s, %(AB)s, %(H)s, %(HR)s, %(RBI)s, %(R)s, %(BB)s, %(IBB)s, %(HBP)s, %(SF)s, %(SO)s, %(GIDP)s, %(TB)s, %(SB)s, %(CS)s)"
                connectToMySQL(db).query_db(query, data)
                index += 1
    @classmethod
    def get_all_players(cls):
        query = "SELECT * FROM players"
        player_list = connectToMySQL(db).query_db(query)
        all_players = []
        for each_player in player_list:
            one_player = cls(each_player)
            all_players.append(one_player)
        return all_players



