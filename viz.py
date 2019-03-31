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



q ="""select lookup.name,avg(work.focus),avg(work.time) from lookup inner join work on lookup.uri = work.uri  group by lookup.uri order by avg(work.time) desc; """
c.execute(q)
data = c.fetchall()
m = ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')
x = [ ]
y = [ ]
names = []
for i in data:
    names.append(i[0])
    x.append(i[2])
    y.append(i[1])
fig, ax = plt.subplots()
#ax.scatter(x,y)
print("DONE")
label = 1
for i, name in enumerate(names):
    ax.scatter(x[i],y[i])
    """
for i, name in enumerate(names):
    label = ax.annotate(name, (x[i], y[i]), ha='center', va='center')
"""
    ax.legend()
plt.title('Average Rating vs Average Time')
plt.ylabel('Average Rating (1-5)')
plt.xlabel('Average Time (minutes)')
plt.show()

