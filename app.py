from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

app.secret_key = "GrillMoreGruls99"
app.config['SESSION_COOKIE_NAME'] = 'Sheikh Cookie'

@app.route('/')
def index():
    return 'Home page'

@app.route('/getTracks')
def getTracks():
    return"Some songs"