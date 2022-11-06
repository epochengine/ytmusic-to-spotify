import spotify
import time
import ytmusic
import os.path

from collections.abc import Callable


class MigrationRunner:

    def __init__(self, yt_music_client, spotify_client):
        self.yt_music_client = yt_music_client
        self.spotify_client = spotify_client

    def migrate_library(self):
        migrate_function = self.spotify_client.add_to_library
        self.migrate_songs(self.yt_music_client.get_liked_songs_playlist_id(), None, migrate_function)

    def migrate_playlist(self, playlist_name: str, spotify_playlist_id: str = None):
        yt_playlist_id = self.yt_music_client.get_playlist(playlist_name)
        if not spotify_playlist_id:
            spotify_playlist_id = self.spotify_client.create_playlist(playlist_name)
        migrate_function = self.spotify_client.add_to_playlist
        self.migrate_songs(yt_playlist_id, spotify_playlist_id, migrate_function)

    def migrate_songs(
            self,
            yt_playlist_id,
            spotify_playlist_id,
            migrate_function: Callable = None,
            timeout_seconds: float = 5,
            batch_size: int = 10):
        if not migrate_function:
            migrate_function = self.spotify_client.add_to_playlist
        playlist_songs = self.yt_music_client.get_playlist_songs(yt_playlist_id)
        total = len(playlist_songs)

        i = 0
        while i < total:
            start = i
            last_batch = i + batch_size >= total
            i = min(i + batch_size, total)

            batch = playlist_songs[start:i]
            self.process_batch(batch, migrate_function, spotify_playlist_id)
            print(f"Progress: {i}/{total}")
            if not last_batch:
                time.sleep(timeout_seconds)

    def process_batch(self, songs_batch: list[dict], migrate_function: Callable, playlist_id: str):
        track_ids = []
        for song in songs_batch:
            spotify_tracks = self.spotify_client.search(song['title'], song['artist'], song['album'])
            results = spotify_tracks['tracks']['items']
            if len(results) > 0:
                choice = results[0]
                track_ids.append(choice['id'])
                # if debug
                song_name = 'Unknown song'
                if 'name' in choice:
                    song_name = choice['name']
                song_artist = 'No artist'
                if 'artists' in choice and len(choice['artists']) > 0:
                    song_artist = choice['artists'][0]['name']
                song_album = 'unknown album'
                if 'album' in choice:
                    song_album = choice['album']['name']
                print(f"Selecting {song_name} - {song_artist} (from {song_album}) "
                      f"for search {song['title']} - {song['artist']} (from {song['album']})")

            else:
                artist_info = ''
                if song['artist']:
                    artist_info = ' - ' + song['artist']
                print("No match found for " + song['title'] + artist_info)

        migrate_function(playlist_id, track_ids)


def main():
    check_file('config.ini')
    check_file('headers_auth.json')
    runner = MigrationRunner(ytmusic.YouTubeMusic(), spotify.Spotify())
    # runner.migrate_library()
    # runner.migrate_playlist('')


def check_file(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError('Missing ' + filename)


if __name__ == '__main__':
    main()
