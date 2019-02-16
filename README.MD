# Best Study Music
This is a small flask server that authenticates with spotify and randomly chooses a focus playlist from a predefined set of choices. It is then controllable via get requests. I've added code to make it easy to integrate with orgmode. So that music will start playing when you clock in to an orgmode task and music will stop playing when you clock out. It also records how focused you felt so that you can find playlists that work well for you.

You will need to create a spotify developer account and set the appropiate client_id and client_secret and redirect uri in spot.py.

When the server first runs you'll be prompted to visit address this is so you can allow the server to control your spotify account.
```
https://accounts.spotify.com/authorize?scope=app-remote-control+playlist-modify-private+playlist-modify-public+playlist-read-collaborative+playlist-read-private+streaming+user-follow-modify+user-follow-read+user-library-modify+user-library-read+user-modify-playback-state+user-read-birthdate+user-read-currently-playing+user-read-email+user-read-email+user-read-playback-state+user-read-private+user-read-recently-played+user-top-read&redirect_uri=http%3A%2F%2Fexample.com&response_type=code&client_id=XXXXXXX

Please paste the url you were redirected to below
```
Visit the url in your browser and paste the referral url in double qoutes into the terminal. The server will then cache the credentials so you only need to authenticate once.
```
"https://example.com/?code=AQArWBePQbeGCmAJCSg0X6D5t9mK6PpcPQ8kL65WB_3mUtsjpMc8IZTPbsoKxseYeRROodcebsiRyZ-9JzkWabc6AG9p6czXSuoSZ-M98-s1ACUnqge0P_LHcDfW8tvbnalCDIDR7efM6KCc1GdBaANJg6Je2UWzYQ3hXjEItmNYE71_DRa74TH5HG0amv2ep2uajjwJ1RKVq4NZsdafsdzooaVFZzTe_oMEYg1zfK6JV1wnwDVFGxFUqdBs8tPPWVt7oLT320HYHh496GeUypJNMNuzXzKYgtsjs5UazI1K-X-Eipw7QgnKFjpcD1DE3UhaLIRPssEhztnFUUMMDuj2bv2nNsIeES7UbqDHOWWtb0iFrlGn-ricLJlOIuIzDwLNxt"
```
Add the following code to your .emacs to integrate the service with orgmode. Note the server needs to be running in order to pause and play music
```
(defun playmus()
  (shell-command "curl 127.0.0.1:5000/start"))

(defun stopmus()
  (shell-command "curl 127.0.0.1:5000/stop"))

(add-hook 'org-clock-in-hook #'playmus)
(add-hook 'org-clock-out-hook #'stopmus)
```
When you clock out of an emacs todo you'll be prompted to see how productive you felt.
```
127.0.0.1 - - [16/Feb/2019 02:01:39] "GET /start HTTP/1.1" 200 -
how productive did you feel (1-5)?
2
```
Which will then be saved to the servers saved data. Overtime it will help you get a feel for what music is most helpful to you