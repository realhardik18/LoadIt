import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from googlesearch import search
from pytube import YouTube
import os

auth_manager = SpotifyClientCredentials(
    client_id="xxx",
    client_secret="xxx"
)
sp = spotipy.Spotify(auth_manager=auth_manager)


def sp_spotify(playlist_link):
    playlist = sp.user_playlist('spotify', playlist_link[34:])
    for item in playlist['tracks']['items']:
        track = item['track']
        track_info = sp.track(track['id'])
        artist = item['track']['artists'][0]['name']
        name = track_info["name"]
        song_to_search = name+" "+artist + " youtube"
        for j in search(song_to_search, tld="co.in", num=1, stop=1, pause=2):
            yt = YouTube(j)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=".")
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)


sp_spotify(
    "https://open.spotify.com/playlist/38u8G3c4TMRwvOt31ih0Eh?si=9554c060d9c84e73")
