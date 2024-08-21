import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "your client id"
CLIENT_SECRET = "your client secret"
USER_NAME = "your username"


date = input("What timezone do you want your playlist to be? (YYYY-MM-DD)")
year = date.split("-")[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
song_names_html = soup.find_all(name="h3", class_="a-font-primary-bold-s", id="title-of-a-story")

song_list = []

for i in range(2, len(song_names_html)):
    song_list.append(song_names_html[i].text.strip())

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=USER_NAME,
    )
)

user_id = sp.current_user()["id"]

song_uris = []

for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


new_playlist = sp.user_playlist_create(user=user_id, name=f"Playlist for {date}", public=False, collaborative=False, description=f"This is the playlist of top 100 songs from {date}")
playlist_id = new_playlist["id"]

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
