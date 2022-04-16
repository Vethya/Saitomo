from youtube_search import YoutubeSearch
import youtube_dl

def search(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    url_suffix = results[0]["url_suffix"]

    return f"https://www.youtube.com/{url_suffix}"

def get_video_info(url):
    ytdl_opts = {}
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        music = ytdl.extract_info(url, download=False)

    return music