import spotipy
import spotipy.util as util
import random
import pickle
import time
import thread
from flask import Flask


    # Log in to spotify
CACHE = '.spotipyoauthcache'
CLIENT_ID='XXXXXXX'
CLIENT_SECRET='XXXXXXXX'
REDIRECT_URI='XXXXXXX'
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
spotifyoauth= spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=scope,cache_path=CACHE)
# default to cached token
tokeninfo = spotifyoauth.get_cached_token()

# if not cached login to get token
if not tokeninfo:
    url = spotifyoauth.get_authorize_url()
    print(url)
    url = str(input("\nPlease paste the url you were redirected to below\n"))
    responsecode = spotifyoauth.parse_response_code(url)
    tokeninfo = spotifyoauth.get_access_token(responsecode)

    # tries to load saved data
try:
    focus = pickle.load(open("stats.pickle","rb"))
except:
    # focus playlist to choose from
    focus = {"spotify:user:spotify:playlist:37i9dQZF1DWWQRwui0ExPn":0,
         "spotify:user:spotify:playlist:37i9dQZF1DX4sWSpwq3LiO":0,
         "spotify:user:spotify:playlist:37i9dQZF1DWZeKCadgRdKQ":0,
         "spotify:user:spotify:playlist:37i9dQZF1DX4PP3DA4J0N8":0,
         "spotify:user:spotify:playlist:37i9dQZF1DWWTdxbiocWOL":0,
         "spotify:user:chilledcow:playlist:6eHO8aX6lHu3e6bem8r2rq":0,
         "spotify:user:jigsaw818:playlist:13svul9ibUBdmuVhNkioxN":0,
         "spotify:user:spotify:playlist:37i9dQZF1DWXLeA8Omikj7":0}
    
app = Flask(__name__)
chosen = ''
@app.route("/start")
def start():
    global chosen,tokeninfo
    refreshtoken(tokeninfo)
    print(focus)
    chosen = random.choice(focus.keys())
    sp = spotipy.Spotify(tokeninfo['access_token'])
    sp.start_playback(context_uri=chosen)
    return "started music\n"

@app.route("/stop")
def stop():
    global tokeinfo
    refreshtoken(tokeninfo)
    sp = spotipy.Spotify(tokeninfo['access_token'])
    sp.pause_playback()
    value = focus.get(chosen)
    x = int(input("how productive did you feel (1-5)? "))
    focus.update({chosen:x+value})
    print(focus)
    pickle.dump(focus,open("stats.pickle","wb"))
    return "stopped music\n"

def refreshtoken(tokeninfo):
    if(spotifyoauth.is_token_expired(tokeninfo)):
        spotifyoauth.refresh_access_token(tokeninfo['refresh_token'])
    
if __name__ == '__main__':
   app.run()
