import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_track_info(url):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    track = sp.track(url)
    name = track["name"]
    artists = track["artists"]

    if len(artists) == 1:
        artist = artists[0]["name"]
    else:
        artist = ", ".join(i["name"] for i in artists)
    
    return {"artist": artist, "name": name}