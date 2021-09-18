import configparser
import spotipy

from spotipy.oauth2 import SpotifyOAuth


class Spotify:
    SCOPE = "playlist-read-private playlist-modify-private user-library-modify user-library-read"

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=config['spotify']['clientId'],
            client_secret=config['spotify']['clientSecret'],
            redirect_uri=config['spotify']['redirectUri'],
            scope=self.SCOPE))

    def search(self, title: str, artist: str = None, album: str = None):
        q = title
        if artist:
            q = q + " artist:" + artist
        if album:
            q = q + " album:" + album

        return self.client.search(q)

    def add_to_library(self, track_ids: list[str]):
        self.client.current_user_saved_tracks_add(track_ids)

    def get_library(self, offset: int):
        return self.client.current_user_saved_tracks(limit=20, offset=offset)
