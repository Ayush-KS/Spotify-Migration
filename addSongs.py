import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials

def get_auth():
    scope = "playlist-modify-private playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials.client_id, client_secret= credentials.client_secret, redirect_uri=credentials.redirect_url, scope=scope))
    return sp

sp = get_auth()

def migrate_songs():
    ids = list()
    with open('songsToBeAdded.txt') as f:
        for line in f:
            songId = line.strip()
            sp.playlist_add_items(credentials.playlist_id, [songId], position=0)
    return ids

ids = migrate_songs()