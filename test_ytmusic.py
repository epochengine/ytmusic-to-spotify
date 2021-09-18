import unittest

from unittest.mock import Mock

from ytmusic import YouTubeMusic


class TestYTMusic(unittest.TestCase):
    def test_liked_songs_mapping(self):
        yt_client = Mock()
        mock_liked_songs = {
            'tracks': [
                {
                    'title': 'Track 1'
                },
                {
                    'title': 'Track 2',
                    'artists': [
                        {
                            'name': 'Artist 2.1'
                        },
                        {
                            'name': 'Artist 2.2'
                        }
                    ]
                },
                {
                    'title': 'Track 3',
                    'artists': [],
                    'album': {
                        'name': 'Album 3'
                    }
                }
            ]
        }
        yt_client.get_liked_songs.return_value = mock_liked_songs

        under_test = YouTubeMusic(yt_client)
        retrieved_songs = under_test.get_liked_songs()
        expected_songs = [
            {'title': 'Track 1', 'artist': None, 'album': None},
            {'title': 'Track 2', 'artist': 'Artist 2.1', 'album': None},
            {'title': 'Track 3', 'artist': None, 'album': 'Album 3'}
        ]

        self.assertEqual(retrieved_songs, expected_songs)

    def test_get_playlist(self):
        yt_client = Mock()
        mock_playlists = [
            {'title': 'The Playlist', 'playlistId': 1234},
            {'title': 'Not The Playlist', 'playlistId': 5678}
        ]
        yt_client.get_library_playlists.return_value = mock_playlists

        under_test = YouTubeMusic(yt_client)
        playlist_id = under_test.get_playlist('The Playlist')

        self.assertEqual(playlist_id, 1234)


if __name__ == '__main__':
    unittest.main()
