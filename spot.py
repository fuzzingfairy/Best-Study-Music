import spotipy
import spotipy.util as util
import random
import time
import thread
from flask import Flask
import flask
import sqlite3
import secret


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



# if not cached login to get token
if not tokeninfo:
    url = spotifyoauth.get_authorize_url()
    print(url)
    url = str(input("\nPlease paste the url you were redirected to below\n"))
    responsecode = spotifyoauth.parse_response_code(url)
    tokeninfo = spotifyoauth.get_access_token(responsecode)
    
print("searchin for new playlists")

sp = spotipy.Spotify(tokeninfo['access_token'])

def getName(uri):
    try:
        username = uri.split(':')[2]
        playlist_id = uri.split(':')[4]
        return sp.user_playlist(username, playlist_id)["name"]
    except:
        username = "spotify"
        playlist_id = uri.split(':')[2]
        return sp.user_playlist(username, playlist_id)["name"]

conn = sqlite3.connect('tracks.db')
c = conn.cursor()
    
for i in sp.search("focus",type='playlist')['playlists']['items']:
    c.execute("select uri from lookup where uri = '" +i['uri'] + "';")
    found = c.fetchone()
    if not found:
        name = getName(i['uri'])
        print("adding playlist " + name)
        c.execute("INSERT INTO LOOKUP VALUES ('"+ i['uri'] + "','" + name + "')")
conn.commit()
conn.close()

app =Flask(__name__)
chosen = ''
@app.route("/start")
def start():
    global chosen,tokeninfo
    tokeninfo = refreshtoken(tokeninfo)
    conn = sqlite3.connect('tracks.db')
    c = conn.cursor()
    c.execute("select uri from lookup")
    uris = c.fetchall()
    chosen = random.choice(uris)[0]
    sp = spotipy.Spotify(tokeninfo['access_token'])
    sp.shuffle(True)
    sp.start_playback(device_id=secret.DEVICE_ID,context_uri=chosen)
    return "started music\n"

@app.route("/stop",methods=['GET','POST'])
def stop():
    global tokeninfo
    tokeninfo = refreshtoken(tokeninfo)
    sp = spotipy.Spotify(tokeninfo['access_token'])
    try:
        sp.pause_playback()
    except:
        print("Couldn't stop spotify")
    if flask.request.method == 'POST':
        t = flask.request.values.get("time")
        if x > 0 :
            x = int(flask.request.values.get("focus"))
            conn = sqlite3.connect('tracks.db')
            c = conn.cursor()
            c.execute("INSERT INTO work VALUES ('" + chosen+ "'," + str(x) + "," + str(t) +")")
            conn.commit()
            conn.close()
    return "stopped music\n"

def refreshtoken(tokeninfo):
    if(spotifyoauth.is_token_expired(tokeninfo)):
        tokeninfo = spotifyoauth.refresh_access_token(tokeninfo['refresh_token'])
    return tokeninfo
    
if __name__ == '__main__':
   app.run()
