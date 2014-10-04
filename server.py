import os
from flask import Flask, render_template, request
from urllib2 import urlopen
from xml.dom import minidom
from random import choice

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def main_page():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def recipe_post():
    text = request.form['input']
    processed_text = text.upper()
    return processed_text