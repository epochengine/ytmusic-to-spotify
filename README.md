# ytmusic-to-spotify

A small Python program to migrate a YouTube Music library across to Spotify.

## Setup

### Dependencies

- Python 3.x
- pip
- venv

### (Recommended) create virtual environment

`python3 -m venv venv`

### Install dependencies

`python3 -m pip install -r requirements.txt`

### Spotify auth

Copy `config.ini.example` to a new file called `config.ini`. Replace the placeholders with the values from the
[Spotify developer console](https://developer.spotify.com/dashboard/applications). You will need to add a redirect URI
to your app of `http://localhost:8080` (as set in the template config file).
This allows the included Spotify library [spotipy](https://github.com/plamere/spotipy) to receive the authorization code
from Spotify and complete the OAuth exchange.

### YouTube Music auth

Copy `headers_auth.json.example` to a new file called `headers_auth.json`.
Head to [YouTube Music](https://music.youtube.com) and inspect the headers of any request to that domain
(e.g. `get-search-suggestions`) using your browser's developer tools.
You will need to copy the `Cookie`, `User-Agent` and `X-Goog-AuthUser` header values into the placeholders in the
`headers_auth.json` file.

YouTube Music does not have an official API, so the included library [ytmusicapi](https://github.com/sigma67/ytmusicapi)
mimics a browser accessing the site and uses the 'unofficial' API exposed to the internet that way.

## Running

Calling `python3 migrate.py` will start the migration process. The first time a connection is made to Spotify you will
need to allow the app access to your Spotify account. When access is granted, the browser will attempt to redirect to
your app's `redirect_uri`, which if set properly as above will be handled by spotipy, which will then store a local copy
of an access and refresh token, so this step is not necessary on future executions.

Not all songs will be found, so the program will log to the console if it cannot find any results for a given song
in the YouTube Music library.

The Spotify API has a rate limit, so the migration is done in batches with a pause between to avoid hitting the limit.
This program does not currently handle being rate limited gracefully.

## Post-execution

Unfortunately it is not possible to guarantee perfect matches for each song. This program will use artist/album
information when possible to narrow down the possible search results, but it is recommended to manually look through
the resultant playlist on Spotify's side to ensure there isn't any unexpected in there
(or, e.g. undesired live versions).
You will also need to manually search for and add any songs that weren't found automatically.

## Future work

- TODO: Add work and words around `check.py`.
- TODO: Add migration handling for custom playlists. In particular, refactor the code to make it less nasty (liked songs
passthrough).
- TODO: Logging in a nicer way as a report to make misses more obvious.
- TODO: Mode selector at entrypoint.
