import spotify
import time
import ytmusic


class MigrationRunner:

    def __init__(self):
        self.yt_music_client = ytmusic.YouTubeMusic()
        self.spotify_client = spotify.Spotify()

    def migrate_library(self):
        liked_songs = self.yt_music_client.get_liked_songs()
        total = len(liked_songs)

        i = 0
        while i < total:
            start = i
            i = min(i + 10, total)
            batch = liked_songs[start:i]
            self.like_batch(batch)
            print(f"Progress: {i}/{total}")
            time.sleep(5)

    def like_batch(self, liked_songs_batch: list[dict]):
        track_ids = []
        for song in liked_songs_batch:
            spotify_tracks = self.spotify_client.search(song['title'], song['artist'], song['album'])
            results = spotify_tracks['tracks']['items']
            if len(results) > 0:
                track_ids.append(results[0]['id'])
            else:
                print("No match found for " + song['title'] + " - " + song['artist'])

        self.spotify_client.add_to_library(track_ids)

    def migrate_playlist(self, playlist_name: str):
        playlist_id = self.yt_music_client.get_playlist(playlist_name)


def main():
    runner = MigrationRunner()
    runner.migrate_library()


if __name__ == '__main__':
    main()
