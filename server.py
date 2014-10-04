import os
from flask import Flask, render_template, request
from urllib2 import urlopen
from xml.dom import minidom
from random import choice

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def maain_page():
   return render_template('index.html')
