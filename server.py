import pickle
import numpy as np
from flask import Flask, request
import urllib
import urllib2
from bs4 import BeautifulSoup


def get_top_song(dob, hot100):
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
        {experiment}
        <meta charset="UTF-8">
        <link rel=stylesheet type=text/css href="static/main.css">
        <title>Nostalgia -> {song} - {artist}</title>
        <!-- START GOOGLE ANALYTICS -->
        <script>
          (function(i,s,o,g,r,a,m){{i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){{
          (i[r].q=i[r].q||[]).push(arguments)}},i[r].l=1*new Date();a=s.createElement(o),
          m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
          }})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

          ga('create', 'UA-100396571-1', 'auto');
          ga('send', 'pageview');

        </script>
        <!-- END GOOGLE ANALYTICS -->
    </head>
    <body>
    {body}
    </body>
    </html>"""
    return html



app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/preprocess', methods = ['POST'])
def results():

    with open('/home/ubuntu/nostalgia/hot100_dict.p', 'r') as f:
        hot100 = pickle.load(f)

    y = int(request.form['dob-year'])
    m = int(request.form['dob-month'])
    d = int(request.form['dob-day'])

    return resultsv2(y,m,d)


@app.route('/processv2', methods = ['GET'])
def resultsv2(y,m,d):

    with open('/home/ubuntu/nostalgia/hot100_dict.p', 'r') as f:
        hot100 = pickle.load(f)

    top_songs = get_top_song([y,m,d], hot100)
    song = top_songs[1][0]
    artist = top_songs[1][1]

    youtube_id = get_top_video(song, artist)

    html = make_html()

    experiment = """
    <!-- Google Analytics Content Experiment code -->
    <script>function utmx_section(){{}}function utmx(){{}}(function(){{var
    k='152124986-0',d=document,l=d.location,c=d.cookie;
    if(l.search.indexOf('utm_expid='+k)>0)return;
    function f(n){{if(c){{var i=c.indexOf(n+'=');if(i>-1){{var j=c.
    indexOf(';',i);return escape(c.substring(i+n.length+1,j<0?c.
    length:j))}}}}}}var x=f('__utmx'),xx=f('__utmxx'),h=l.hash;d.write(
    '<sc'+'ript src="'+'http'+(l.protocol=='https:'?'s://ssl':
    '://www')+'.google-analytics.com/ga_exp.js?'+'utmxkey='+k+
    '&utmx='+(x?x:'')+'&utmxx='+(xx?xx:'')+'&utmxtime='+new Date().
    valueOf()+(h?'&utmxhash='+escape(h.substr(1)):'')+
    '" type="text/javascript" charset="utf-8"><\/sc'+'ript>')}})();
    </script><script>utmx('url','A/B');</script>
    <!-- End of Google Analytics Content Experiment code -->
    """

    body = """
    <p>On <b>{d}-{m}-{y}</b>, the top song was <b>{song}</b> by <b>{artist}</b>.<br>
    Check it out on <a href="http://www.youtube.com/embed/{id}" target=_blank>Youtube</a>!</p>
    <p><button onclick="javascript:history.back(); ga('send', 'event', 'button', 'back', 'masn697', 10);">Go back</button></p>
    """.format(d=d, m=m, y=y, song=song, artist=artist, id=youtube_id)

    return html.format(experiment=experiment, song=song, artist=artist, body=body)


@app.route('/processv3', methods = ['GET'])
def resultsv3(y,m,d):

    with open('/home/ubuntu/nostalgia/hot100_dict.p', 'r') as f:
        hot100 = pickle.load(f)

    top_songs = get_top_song([y,m,d], hot100)
    song = top_songs[1][0]
    artist = top_songs[1][1]

    youtube_id = get_top_video(song, artist)

    html = make_html()

    experiment = """
    <!-- Google Analytics Content Experiment code -->
    <script>function utmx_section(){{}}function utmx(){{}}(function(){{var
    k='152124986-0',d=document,l=d.location,c=d.cookie;
    if(l.search.indexOf('utm_expid='+k)>0)return;
    function f(n){{if(c){{var i=c.indexOf(n+'=');if(i>-1){{var j=c.
    indexOf(';',i);return escape(c.substring(i+n.length+1,j<0?c.
    length:j))}}}}}}var x=f('__utmx'),xx=f('__utmxx'),h=l.hash;d.write(
    '<sc'+'ript src="'+'http'+(l.protocol=='https:'?'s://ssl':
    '://www')+'.google-analytics.com/ga_exp.js?'+'utmxkey='+k+
    '&utmx='+(x?x:'')+'&utmxx='+(xx?xx:'')+'&utmxtime='+new Date().
    valueOf()+(h?'&utmxhash='+escape(h.substr(1)):'')+
    '" type="text/javascript" charset="utf-8"><\/sc'+'ript>')}})();
    </script><script>utmx('url','A/B');</script>
    <!-- End of Google Analytics Content Experiment code -->
    """

    body = """
    <p>On <b>{d}-{m}-{y}</b>, the top song was <b>{song}</b> by <b>{artist}</b>.<br>
    Check it out on <a top_songs_i </a>!</p>

    <p><button onclick="javascript:history.back(); ga('send', 'event', 'button', 'back', 'masn697', 10);">Go back</button></p>
    """.format(d=d, m=m, y=y, song=song, artist=artist, top_songs_i=top_songs)

    return html.format(experiment=experiment, song=song, artist=artist, body=body)







if __name__ == '__main__':
    app.run()
    #app.run(host='0.0.0.0', port=5000)
