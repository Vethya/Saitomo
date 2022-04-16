import re

# https://stackoverflow.com/questions/3717115/regular-expression-for-youtube-links
SPOTIFY_REGEX = re.compile("^https:\/\/open.spotify.com\/track\/([a-zA-Z0-9]+)(.*)$")
# https://stackoverflow.com/questions/50876850/spotify-urls-regex
YOUTUBE_REGEX = re.compile("(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)(\w+)")

def music_url_type(link):
    if SPOTIFY_REGEX.search(link):
        return "spotify"

    elif YOUTUBE_REGEX.search(link):
        return "youtube"
        
    else:
        return "invalid"