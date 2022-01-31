import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from googlesearch import search
from pytube import YouTube, Playlist
import os
from zipfile import ZipFile
import random
from datetime import date, datetime

auth_manager = SpotifyClientCredentials(
    client_id="xxx",
    client_secret="xxx"
)

sp = spotipy.Spotify(auth_manager=auth_manager)


def downloader(playlist_link):
    # final file should be name
    if "open.spotify.com" in playlist_link or "www.youtube.com/playlist" in playlist_link:
        now = datetime.now()
        txt_file = open("HELLO.txt", "w+")
        txt_file.write("WELCOME TO YOUR DOWNLOADED SONGS INFO FILE\n")
        zip_id = random.randint(100000, 999999)
        Songs = ZipFile(f'{zip_id}.zip', 'w')
        txt_file.write(f"FINAL ZIP FILE ID:-{zip_id}\n")
        user = "spotify"
        search_terms = []
        links = []
        count = 1
        succses = 0
        if "open.spotify.com" in playlist_link:
            playlist = sp.user_playlist(user, playlist_link[34:])
            for item in playlist['tracks']['items']:
                track = item['track']
                track_info = sp.track(track['id'])
                artist = item['track']['artists'][0]['name']
                name = track_info["name"]
                song_to_search = name+" "+artist + " youtube"
                search_terms.append(song_to_search)
            for term in search_terms:
                links_local = []
                for j in search(term, tld="co.in", num=10, stop=10, pause=2):
                    # reduce search range???
                    links_local.append(j)
                links.append(links_local[0])
            for link in links:
                try:
                    yt = YouTube(link)
                    video = yt.streams.filter(only_audio=True).first()
                    out_file = video.download(output_path=".")
                    base, ext = os.path.splitext(out_file)
                    new_file = f"song_{count}.mp3"
                    os.rename(out_file, new_file)
                    Songs.write(new_file)
                    os.remove(new_file)
                    current_time = now.strftime("%H:%M:%S")
                    txt_file.write(
                        f"added song '{search_terms[count-1]}' at '{current_time}'\n")
                    count += 1
                    succses += 1
                except Exception as e:
                    current_timee = now.strftime("%H:%M:%S")
                    txt_file.write(
                        f"failed to add '{search_terms[-1]}' at '{current_timee}'\n")
                    count += 1
        elif "www.youtube.com/playlist" in playlist_link:
            playlist = Playlist(playlist_link)
            i = 1
            for url in playlist.video_urls:
                try:
                    yt = YouTube(url)
                    video = yt.streams.filter(only_audio=True).first()
                    out_file = video.download(output_path=".")
                    base, ext = os.path.splitext(out_file)
                    new_file = f"song_{count}.mp3"
                    os.rename(out_file, new_file)
                    Songs.write(new_file)
                    os.remove(new_file)
                    current_time = now.strftime("%H:%M:%S")
                    txt_file.write(
                        f"added song '{yt._title}' at '{current_time}'\n")
                    count += 1
                    succses += 1
                except Exception as e:
                    current_timee = now.strftime("%H:%M:%S")
                    txt_file.write(
                        f"failed to add '{yt._title}' at '{current_timee}'\n")
                    count += 1
        txt_file.write(f"added {succses}/{count-1}")
        txt_file.close()
        Songs.write('HELLO.txt')
        Songs.close()
        os.remove('HELLO.TXT')
        return os.path.abspath(f"{zip_id}.zip")
    else:
        return "a"
