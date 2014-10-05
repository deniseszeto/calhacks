import os
from flask import Flask, render_template, request, redirect, url_for
from findrecipe import findRecipe
from nearestStore import nearestStore
import walmartList
import createCart

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
                               ingred=ingredients, ingredstr=repr(ingredients), recipe=instructions, address=address, needtobuy="", walmart="")
    else:
        return render_template('index.html', input="", recipename="", ingred=set(), ingredstr="", recipe="", address="", needtobuy="", walmart="")

@app.route('/list', methods = ["POST", "GET"])
def list():
    if request.method == "POST":
        shoppinglist = request.form["shoppinglist"]
        inputx, recipenamex, ingredx, ingredstrx, recipex, addressx = request.form["inputx"], request.form["recipenamex"], request.form["ingredx"], request.form["ingredstrx"], request.form["recipex"], request.form["addressx"], 
        print(inputx)
        ingredx = eval(ingredstrx)
        slsplit = shoppinglist.split();
        try:
            if request.form["walmart"] == 'Walmart':
                walmart = walmartList.createCart(slsplit);
                return render_template('index.html', input=inputx, recipename=recipenamex, ingred=ingredx, ingredstr=ingredx, recipe=recipex, address=addressx, needtobuy=shoppinglist, walmart=walmart, amazon="")
        except:
            try:
                if request.form["amazon"] == 'Amazon':
                    amazon = createCart.createCart(slsplit);
                    return render_template('index.html', input=inputx, recipename=recipenamex, ingred=ingredx, ingredstr=ingredx,recipe=recipex, address=addressx, needtobuy=shoppinglist, walmart="", amazon=amazon)
            except:
                pass
    else:
        return redirect(request.url[:-4])



if __name__ == '__main__':
    app.debug = True
    app.run(port=5555)