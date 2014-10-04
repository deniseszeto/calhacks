import os
from flask import Flask, render_template, request
import findrecipe

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def main_page():
    return render_template('index.html', input="", recipename="Beerd Eggs")

@app.route('/', methods=['POST'])
def recipe_post():
    inputrecipe = request.form['input']
    name, ingredients, instructions = findRecipe(inputrecipe)
    return render_template('index.html', input=inputrecipe, recipename=name)