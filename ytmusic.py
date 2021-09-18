from ytmusicapi import YTMusic


class YouTubeMusic:

    def __init__(self, client=None):
        self.client = client or YTMusic('headers_auth.json')

    def get_liked_songs(self):
        liked_songs = self.client.get_liked_songs(limit=1000)
        tracks = liked_songs['tracks']

        searches = []
        for t in tracks:
            title = t['title']

            album = None
            if 'album' in t:
                album = t['album']['name']

            artist = None
            if 'artists' in t and len(t['artists']) > 0:
                artist = t['artists'][0]['name']
            searches.append({'title': title, 'album': album, 'artist': artist})

        return searches

    def get_playlist(self, name: str):
        all_playlists = self.client.get_library_playlists()
        for playlist in all_playlists:
            if playlist['title'] == name:
                return playlist['playlistId']

        return None
