import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

ID = "ID HERE"
SECRET = "S HERE"
URL = "https://www.billboard.com/charts/hot-100"
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# Scraping Billboard 100
response = requests.get(url=f"{URL}/{date}")
chart_web = response.text

soup = BeautifulSoup(chart_web, "html.parser")
titles = soup.select("li h3")

song_names = [title.get_text(strip=True) for title in titles]

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ID,
                                               client_secret=SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               username="UN"))

user_id = sp.current_user()["id"]

# Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]

for song in song_names:
    # Search for the song
    results = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)

    try:
        track_uri = results['tracks']['items'][0]['uri']
        song_uris.append(track_uri)

    except IndexError:
        print(f"No track found for '{song}' in Spotify.")

# Creating a new private playlist in Spotify
new_playlist = sp.user_playlist_create(user=user_id,
                                       name=f"{date} Billboard 100",
                                       public=False,
                                       collaborative=False,
                                       description=f"{date}s TOP 100 songs for Nostalgia")

sp.playlist_add_items(playlist_id=new_playlist["id"], items=song_uris)
