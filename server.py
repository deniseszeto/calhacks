import os
from flask import Flask, render_template, request
from findrecipe import findRecipe
from nearestStore import nearestStore

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def main_page():
    if request.method == "POST" and request.form['input'] != "":
        inputrecipe = request.form['input']
        inputlat = request.form['lat']
        inputlong = request.form['long']
        name, ingredients, ctype, instructions = findRecipe(inputrecipe)
        address = nearestStore(ctype,inputlat,inputlong)
        print(address)
        return render_template('index.html', input=inputrecipe, recipename=name,
                               ingred=ingredients, recipe=instructions, address=address)
    else:
        return render_template('index.html', input="", recipename="", ingred=set(), recipe="", address="")

if __name__ == '__main__':
    app.debug = True
    app.run(port=5555)