from ytmusicapi import YTMusic


class YouTubeMusic:

    liked_songs_playlist_id = 'LM'

    def __init__(self, client=None):
        self.client = client or YTMusic('headers_auth.json')

    def get_liked_songs_playlist_id(self):
        return self.liked_songs_playlist_id

    def get_playlist(self, name: str):
        all_playlists = self.client.get_library_playlists()
        for playlist in all_playlists:
            if playlist['title'] == name:
                return playlist['playlistId']

        return None

    def get_playlist_songs(self, playlist_id: str):
        # This is explicitly allowed by the library to force no limit.
        # noinspection PyTypeChecker
        playlist_songs = self.client.get_playlist(playlist_id, limit=None)
        tracks = playlist_songs['tracks']

        searches = []
        for t in tracks:
            title = t['title']

            album = None
            if 'album' in t and t['album']:
                album = t['album']['name']

            artist = None
            if 'artists' in t and len(t['artists']) > 0:
                artist = t['artists'][0]['name']
            searches.append({'title': title, 'album': album, 'artist': artist})

        return searches
