import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials
from fuzzywuzzy import fuzz

def get_auth():
    scope = "playlist-modify-private playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials.client_id, client_secret= credentials.client_secret, redirect_uri=credentials.redirect_url, scope=scope))
    return sp

def is_fuzzy_match(actual, found):
    ind = found.rfind("-")
    if ind != -1:
        found = found[0:ind]
        
    ind = found.find("(")
    if ind != -1:
        found = found[0:ind]

    return fuzz.partial_ratio(actual.lower(), found.lower()) > 80

sp = get_auth()

def get_song_deets(name):
    res = sp.search(name, limit=1, offset=0, type='track', market=None)
    if res['tracks']['items']:
        return res['tracks']['items'][0]['id'], res['tracks']['items'][0]['name']
    else:
        return "x", "x"

def migrate_songs():
    names = list()
    with open('songnames.txt') as f:
        for line in f:
            songName = str(line.strip()[:-4])
            names.append(songName)
    
    names.sort(reverse=True)

    songsToBeAdded = list()

    songsNotAdded = list()
    for songName in names:
        id, spotifySongName  = get_song_deets(songName)
        if id == "x" or not is_fuzzy_match(songName, spotifySongName):
            songsNotAdded.append(songName)
        else:
            songsToBeAdded.append(id)

    print("Number of songs to be added: ", len(songsToBeAdded))
    print("Total songs in the list: ", len(names))

    print("Success Percentage: ", (len(songsToBeAdded)/len(names)) * 100)
    return songsToBeAdded, songsNotAdded
        
def add_songs_not_added_to_file(songsNotAdded):
        with open('songsNotAdded.txt', 'w') as f:
            for song in songsNotAdded:
                f.write(song)
                f.write('\n')

def add_songs_to_be_added_to_file(songsToBeAdded):
        with open('songsToBeAdded.txt', 'w') as f:
            for song in songsToBeAdded:
                f.write(song)
                f.write('\n')

songsToBeAdded, songsNotAdded = migrate_songs()

add_songs_not_added_to_file(songsNotAdded)
add_songs_to_be_added_to_file(songsToBeAdded)
