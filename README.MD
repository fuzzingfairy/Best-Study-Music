# Quick start
To get started you'll need to install the required libraries I used `pip install -r requirements.txt`. This script relies on features of spotipy that aren't yet on pip. So you will need to install the most recent spotipy by cloning the github repo and installing it locally by typing `pip install .`. Then sign up for a spotify [developer's](https://developer.spotify.com/) account. Add your client id and client secret to secrets.py you'll also be prompted for a redirect uri this is url you want to be redirected to after your authenticated. Optionally add your device_id if there's a specific device you want Spotify to play on.

When you first run the server it will prompt you through Spotify's authentication process. It will then cache your tokens so you won't have to go through it again.

The script will then populate the database with the most popular songs in the Focus genre. To play make a get request to `localhost:5000/start` make sure the spotify client is open so that the server can communicate with it. Enjoy the music!
