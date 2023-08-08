# Logging in with diffrent user still gives the same list of liked songs - NEDDS TO BE FIXED



from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Configuring the app for flask
app = Flask(__name__)

app.secret_key = "GrillMoreGruls99"
app.config['SESSION_COOKIE_NAME'] = 'Sheikh Cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    iteration = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=iteration * 50)['items']
        user = sp.current_user()
        user_id = user['id']
        iteration += 1
        all_songs += items
        if (len(items) < 50):
            break
    all_names = []
    for song in all_songs:
        track = song['track']
        name = track['name']
        all_names.append(name)
    return user_id

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
           client_id="ee138498b83f4ee49967cbf8f0de62b9",
           client_secret="e3ad04585f1248b196fcb72cd90ffc81",
           redirect_uri=url_for('redirectPage', _external=True), #url_for is used so that we do not have to hard code the website url
           scope="user-library-read")