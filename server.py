import os
from flask import Flask, render_template, request
import findrecipe

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def main_page():
    if request.method == "GET":
        return render_template('index.html', input="", recipename="Beer Eggs")
    else:
        inputrecipe = request.form['input']
        print(inputrecipe)
        name, ingredients, instructions = findRecipe(inputrecipe)
        print(name)
        return render_template('index.html', input=inputrecipe, recipename=name)
