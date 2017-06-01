import pickle
import numpy as np
from flask import Flask, request
import urllib
import urllib2
from bs4 import BeautifulSoup


def get_top_song(dob):
    year, month, day = dob
    days = hot100[year][month].keys()
    day_key = days[np.argmin(abs(np.array(days) - day))]
    return hot100[year][month][day_key]


def get_top_video(song, artist):
    textToSearch = ' '.join([song, artist])
    query = urllib.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    youtube_url = soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]['href']
    return youtube_url.split("v=")[1]


def make_html():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link rel=stylesheet type=text/css href="static/main.css">
        <title>Top Songs</title>
    </head>
    <body>
    {}
    </body>
    </html>"""
    return html



app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/process', methods = ['POST'])
def results():
    y = int(request.form['dob-year'])
    m = int(request.form['dob-month'])
    d = int(request.form['dob-day'])

    top_songs = get_top_song([y,m,d])
    song = top_songs[1][0]
    artist = top_songs[1][1]

    youtube_id = get_top_video(song, artist)

    html = make_html()

    content = """
    <p>On <b>{d}-{m}-{y}</b>, the top song was <b>{song}</b> by <b>{artist}</b>.</br>
    Check it out below!</p>
    <div class="video-container">
        <iframe src="http://www.youtube.com/embed/{id}" allowfullscreen></iframe>
    </div>
    <p><a href="../" class="button">Go back</a></p>
    """.format(d=d, m=m, y=y, song=song, artist=artist, id=youtube_id)

    return html.format(content)


if __name__ == '__main__':
    with open('hot100_dict.p', 'r') as f:
        hot100 = pickle.load(f)

    app.run(host='0.0.0.0', port=5000)
