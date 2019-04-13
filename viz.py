import pickle
import numpy as np
import operator
import json
import spotipy
import spotipy.util as util
import sqlite3
import secret
import matplotlib.pyplot as plt
import random

    
    # Log in to spotify
CACHE = '.spotipyoauthcache'
scope   ="""user-read-email
    playlist-read-private
    playlist-modify-private
    playlist-modify-public
    playlist-read-collaborative
    user-modify-playback-state
    user-read-currently-playing
    user-read-playback-state
    user-top-read
    user-read-recently-played
    app-remote-control
    streaming
    user-read-birthdate
    user-read-email
    user-read-private
    user-follow-read
    user-follow-modify
    user-library-modify
    user-library-read"""
spotifyoauth= spotipy.oauth2.SpotifyOAuth(client_id=secret.CLIENT_ID,client_secret=secret.CLIENT_SECRET,redirect_uri=secret.REDIRECT_URI,scope=scope,cache_path=CACHE)
# default to cached token
tokeninfo = spotifyoauth.get_cached_token()
sp = spotipy.Spotify(tokeninfo['access_token'])

print(sp.devices())

def getName(uri):
    try:
        username = i.split(':')[2]
        playlist_id = i.split(':')[4]
        return sp.user_playlist(username, playlist_id)["name"]
    except:
        username = "spotify"
        playlist_id = i.split(':')[2]
        return sp.user_playlist(username, playlist_id)["name"]



    
conn = sqlite3.connect("tracks.db")
c = conn.cursor()
q = """SELECT lookup.name,avg(work.focus) 
FROM lookup 
LEFT JOIN work  USING(uri) 
GROUP BY lookup.name  
UNION ALL 
SELECT lookup.uri,avg(work.focus) 
FROM work 
LEFT JOIN lookup USING(uri) 
WHERE work.focus IS NULL 
GROUP BY lookup.name ORDER  by avg(work.focus) Desc;"""
c.execute(q)
data = c.fetchall()
for i in data:
    print("%-20s %s" % (i[0], i[1]))

def graph(data,title,yl,xl,f):
    x = [ ]
    y = [ ]
    names = []
    for i in data:
        names.append(i[0])
        x.append(i[2])
        y.append(i[1])
    fig, ax = plt.subplots()
    ax.set_facecolor('#303030')
   # fig.patch.set_facecolor('#303030')
    ax.spines['bottom'].set_color('#c6c6c6')
    ax.spines['top'].set_color('#c6c6c6')
    ax.spines['right'].set_color('#c6c6c6')
    ax.spines['left'].set_color('#c6c6c6')
    ax.tick_params(axis='x', colors='#c6c6c6')
    ax.tick_params(axis='y', colors='#c6c6c6')
    ax.yaxis.label.set_color('#c6c6c6')
    ax.xaxis.label.set_color('#c6c6c6')
    ax.title.set_color('#ff4ea3')
    #ax.scatter(x,y)
    label = 1
    colors= "#a020f0"
    plt.scatter(x,y,c=colors)
    plt.title(title)
    plt.ylabel(yl)
    plt.xlabel(xl)
    plt.savefig(f,facecolor='#303030')


q ="""select lookup.name,work.focus,work.time from lookup inner join work on lookup.uri = work.uri  group by lookup.uri order by avg(work.time) desc; """
c.execute(q)
data = c.fetchall()
graph(data,'Rating vs Time','Rating (1-5)','Time (minutes)',"rating.png")


q ="""select lookup.name,avg(work.focus),avg(work.time) from lookup inner join work on lookup.uri = work.uri  group by lookup.uri order by avg(work.time) desc; """
c.execute(q)
data = c.fetchall()
graph(data,'Average Rating vs Average Time','Average Rating (1-5)','Average Time (minutes)',"avg.png")


