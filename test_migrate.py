import unittest

from unittest.mock import Mock, call

from migrate import MigrationRunner


class TestMigrate(unittest.TestCase):

    def setUp(self) -> None:
        self.yt_music_client = Mock()
        self.spotify_client = Mock()
        mock_playlist_songs = [
            {'title': 'Title 1', 'artist': 'Artist 1', 'album': 'Album 1'}
        ]
        self.yt_music_client.get_playlist_songs.return_value = mock_playlist_songs
        self.spotify_client.search.return_value = {'tracks': {'items': [{'id': 12}, {'id': 34}]}}
        self.under_test = MigrationRunner(self.yt_music_client, self.spotify_client)

    def test_migrate_library(self):
        self.under_test.migrate_library()

        self.assertEqual(self.spotify_client.add_to_library.call_args_list, [call(None, [12])])

    def test_no_result(self):
        spotify_searches = {'tracks': {'items': []}}
        self.spotify_client.search.return_value = spotify_searches

        self.under_test.migrate_library()

        self.assertEqual(self.spotify_client.add_to_library.call_args_list, [call(None, [])])

    def test_migrate_playlist(self):
        self.spotify_client.create_playlist.return_value = 'playlist1234'

        self.under_test.migrate_playlist('My Playlist')

        self.assertEqual(self.spotify_client.add_to_playlist.call_args_list, [call('playlist1234', [12])])

    def test_batching(self):
        mock_playlist_songs = [
            {'title': 'Title 1', 'artist': None, 'album': None},
            {'title': 'Title 2', 'artist': 'Artist 2', 'album': 'Album 2'}
        ]
        self.yt_music_client.get_playlist_songs.return_value = mock_playlist_songs
        spotify_searches = [
            {'tracks': {'items': [{'id': 12}]}},
            {'tracks': {'items': [{'id': 34}, {'id': 56}]}}
        ]
        self.spotify_client.search.side_effect = spotify_searches

        self.under_test.migrate_songs('yt_playlist1234', 'sp_playlist1234', timeout_seconds=0.001, batch_size=1)

        self.assertEqual(self.spotify_client.add_to_playlist.call_args_list,
                         [call('sp_playlist1234', [12]), call('sp_playlist1234', [34])])


if __name__ == '__main__':
    unittest.main()
