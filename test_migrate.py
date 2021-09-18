import unittest

from unittest.mock import Mock, call

from migrate import MigrationRunner


class TestMigrate(unittest.TestCase):

    timeout_seconds = 0.001

    def test_migrate_library(self):
        yt_music_client = Mock()
        mock_liked_songs = [
            {'title': 'Title 1', 'artist': None, 'album': None},
            {'title': 'Title 2', 'artist': 'Artist 2', 'album': 'Album 2'}
        ]
        yt_music_client.get_liked_songs.return_value = mock_liked_songs
        spotify_client = Mock()
        spotify_searches = [
            {'tracks': {'items': [{'id': 12}]}},
            {'tracks': {'items': [{'id': 34}, {'id': 56}]}}
        ]
        spotify_client.search.side_effect = spotify_searches

        under_test = MigrationRunner(yt_music_client, spotify_client)
        under_test.migrate_library(timeout_seconds=self.timeout_seconds, batch_size=1)

        self.assertEqual(spotify_client.add_to_library.call_args_list, [call([12]), call([34])])

    def test_no_result(self):
        yt_music_client = Mock()
        mock_liked_songs = [
            {'title': 'Title 1', 'artist': None, 'album': None},
            {'title': 'Title 2', 'artist': 'Artist 2', 'album': 'Album 2'}
        ]
        yt_music_client.get_liked_songs.return_value = mock_liked_songs
        spotify_client = Mock()
        spotify_searches = {'tracks': {'items': []}}
        spotify_client.search.return_value = spotify_searches

        under_test = MigrationRunner(yt_music_client, spotify_client)
        under_test.migrate_library(timeout_seconds=self.timeout_seconds)

        self.assertEqual(spotify_client.add_to_library.call_args_list, [call([])])


if __name__ == '__main__':
    unittest.main()
