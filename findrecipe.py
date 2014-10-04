def findRecipe(keywords):
	apiKey = dvxI9e588cOKNvbOzd24EXsVRW9Y2OW8
	recipe_keyword = []
	recipe_name = ''
	recipe_keyword = keywords.split(' ')

	for word in recipe_keyword:
		recipe_name += word
		recipe_name += '_'

	url = "http://api.bigoven.com/recipes?pg=1&rpp=25&title_kw="
                  + recipe_name 
                  + "&api_key="+apiKey

    return url 