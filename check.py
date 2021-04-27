import spotify
import ytmusic

yt_client = ytmusic.YouTubeMusic()
spotify_client = spotify.Spotify()


def check_for_duplicates(yt_music_songs: list[dict]):
    seen = []
    dupes = []
    for song in yt_music_songs:
        title = song['title']
        if title in seen:
            dupes.append(f"{title} - {song['artist']}")
        else:
            seen.append(title)

    if len(dupes) == 0:
        print("No duplicates found")
    else:
        print(f"{len(dupes)} duplicates found:")
        for song in dupes:
            print(song)


def check_for_missing_songs(yt_music_songs: list[dict], spotify_songs: list[dict]):
    spotify_songs_lower = [song['title'].lower() for song in spotify_songs]
    missing_songs = []
    for song in yt_music_songs:
        if song['title'].lower() not in spotify_songs_lower:
            missing_songs.append(f"{song['title']} - {song['artist']}")

    if len(missing_songs) == 0:
        print("No missing songs found")
    else:
        print(f"{len(missing_songs)} missing songs found:")
        for song in missing_songs:
            print(song)


def get_library_csv(library: list[dict], service: str):
    i = 0
    csv = f"{service} song,{service} artist,\n"
    while i < len(library):
        title = library[i]['title'].replace(",", "")
        artist = library[i]['artist'].replace(",", "")
        csv = csv + f"{title},{artist},\n"
        i = i + 1

    with (open(f"library-{service}.csv", "w")) as csv_file:
        csv_file.write(csv)


def get_spotify_songs():
    i = 0
    spotify_songs = []
    library = spotify_client.get_library(i)
    total = library['total']
    while i <= total:
        batch = spotify_client.get_library(i)['items']
        for song in batch:
            spotify_songs.append({'title': song['track']['name'], 'artist': song['track']['artists'][0]['name']})
        i = i + 20
    return spotify_songs


def get_youtube_music_songs():
    return yt_client.get_liked_songs()


yt_songs = get_youtube_music_songs()
s_songs = get_spotify_songs()
check_for_duplicates(yt_songs)
print("\n")
check_for_missing_songs(yt_songs, s_songs)
# get_library_csv(yt_songs, "YT")
# get_library_csv(s_songs, "Spotify")
