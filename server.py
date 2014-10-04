import os
from flask import Flask, render_template, request
from urllib2 import urlopen
from xml.dom import minidom
from random import choice

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def at_first():
    if request.method == "POST":
        print "posting"
        time = request.form['time']
        author = request.form['author']
        genre = request.form['genre']
        song_url = findSong(time, author, genre)
        print song_url
        song_url = song_url.encode('ascii','ignore')
        return render_template('index.html', time = time, author = author, genre = genre, song_id = song_url, play = "true")
    else:
        return render_template('index.html', time = "", author = "", genre = "", song_id = "0", play = "false")


def findSong(time, title="", genre="electronic", tolerance=10):
    """
        Returns a song ID of a song that lasts an input time with
        optional query and genre fields to a given tolerance. The
        song is chosen at random from a list of qualifying songs.
        However, if no songs are found within the given tolerance,
        the song closest to input time will be returned.
        
        If an input is invalid, the function uses a default valid
        input instead of the invalid one.

        Time is in minutes, and tolerance is in seconds.
    """
    CLIENT_ID = '93fbdae95f70cd94b70864746295c28f'
    DEFAULT_TIME = 5.0
    DEFAULT_LINK = "http://api.soundcloud.com/tracks/159367793"
    SHORT = 2
    MEDIUM = 10
    LONG = 30
    MINUTES_TO_MILLISECONDS = 60000
    SECONDS_TO_MILLISECONDS = 1000
    
    try:
        time = float(time)
    except:
        time = DEFAULT_TIME
    title = title.replace(" ", "_")
    genre = genre.replace(" ", "_")
    

    url = "http://api.soundcloud.com/tracks?client_id=" + CLIENT_ID

    url += "&filter.duration="
    if time < SHORT:
        url += "short"
    elif time < MEDIUM:
        url += "medium"
    elif time < LONG:
        url += "long"
    else:
        url += "epic"

    # limit=200 maxes out the number of results on the page.
    url += "&genre=" + genre + "&q=" + title + "&limit=200"

    page = urlopen(url)
    xmlDoc = minidom.parse(page)
    durations = xmlDoc.getElementsByTagName('duration')
    uris = []
    for el in xmlDoc.getElementsByTagName('uri'):
        if "tracks" in el.firstChild.nodeValue:
            uris.append(el)
            
    epsilon = float('inf')
    link = DEFAULT_LINK
    timeMs = time * MINUTES_TO_MILLISECONDS
    songList = []
    for i in range(len(durations)):
        diff = abs(timeMs - float(durations[i].firstChild.nodeValue))
        if diff < epsilon:
            epsilon = diff
            link = uris[i].firstChild.nodeValue
            if epsilon < tolerance * SECONDS_TO_MILLISECONDS:
                songList.append(link)
                # return link[33:]
            
    return choice(songList)[33:] if songList else link[33:]
