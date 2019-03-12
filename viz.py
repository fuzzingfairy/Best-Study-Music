import pickle
import numpy as np
import operator
import json
import spotipy
import spotipy.util as util
import sqlite3
import secret

focus = pickle.load(open("stats.pickle","rb"))
sorted_x = sorted(focus.items(), key=operator.itemgetter(1))
names = [i[0] for i in sorted_x][::-1]
values =[i[1] for i in sorted_x][::-1]
    
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

playnames = []
for i in names:
    try:
        username = i.split(':')[2]
        playlist_id = i.split(':')[4]
        playnames.append(sp.user_playlist(username, playlist_id)["name"])
    except:
        username = "spotify"
        playlist_id = i.split(':')[2]
        playnames.append(sp.user_playlist(username, playlist_id)["name"])

conn = sqlite3.connect('tracks.db')
c = conn.cursor()
for i in range(len(playnames)):
    print(playnames[i] + " " + str(values[i]) + " names " + str(names[i]))
    c.execute("INSERT INTO lookup VALUES ('" +names[i]+"','"+ playnames[i] +"');")
conn.commit()
conn.close()

def getName(uri):
    try:
        username = i.split(':')[2]
        playlist_id = i.split(':')[4]
        return sp.user_playlist(username, playlist_id)["name"]
    except:
        username = "spotify"
        playlist_id = i.split(':')[2]
        return sp.user_playlist(username, playlist_id)["name"]
