import os
from flask import Flask, render_template, request
from findrecipe import findRecipe

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def main_page():
    if request.method == "GET":
        return render_template('index.html', input="", recipename="", ingred=set(), recipe="")
    else:
        inputrecipe = request.form['input']
        name, ingredients, instructions = findRecipe(inputrecipe)
        return render_template('index.html', input=inputrecipe, recipename=name,
                               ingred=ingredients, recipe=instructions)

if __name__ == '__main__':
    #app.debug = True
    app.run(port=5555)