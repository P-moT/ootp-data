from flask import Flask
import logging

logging.basicConfig(filename='record.log', level=logging.ERROR)
app = Flask(__name__)
app.secret_key = "1337"

