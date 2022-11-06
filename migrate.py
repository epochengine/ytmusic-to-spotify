import spotify
import time
import ytmusic
import os.path


class MigrationRunner:

    def __init__(self, yt_music_client, spotify_client):
        self.yt_music_client = yt_music_client
        self.spotify_client = spotify_client

    def migrate_library(self, timeout_seconds: float = 5, batch_size: int = 10):
        liked_songs = self.yt_music_client.get_liked_songs()
        total = len(liked_songs)

        i = 0
        while i < total:
            start = i
            last_batch = i + batch_size >= total
            i = min(i + batch_size, total)

            batch = liked_songs[start:i]
            self.like_batch(batch)
            print(f"Progress: {i}/{total}")
            if not last_batch:
                time.sleep(timeout_seconds)

    def like_batch(self, liked_songs_batch: list[dict]):
        track_ids = []
        for song in liked_songs_batch:
            spotify_tracks = self.spotify_client.search(song['title'], song['artist'], song['album'])
            results = spotify_tracks['tracks']['items']
            if len(results) > 0:
                track_ids.append(results[0]['id'])
            else:
                artist = song['artist']
                if not artist:
                    artist = 'N/A'
                print("No match found for " + song['title'] + " - " + artist)

        self.spotify_client.add_to_library(track_ids)

    def migrate_playlist(self, playlist_name: str):
        playlist_id = self.yt_music_client.get_playlist(playlist_name)


def main():
    check_file('config.ini')
    check_file('headers_auth.json')
    runner = MigrationRunner(ytmusic.YouTubeMusic(), spotify.Spotify())
    runner.migrate_library()


def check_file(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError('Missing ' + filename)


if __name__ == '__main__':
    main()
