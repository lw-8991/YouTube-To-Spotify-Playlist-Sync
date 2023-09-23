from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import re
import random

#===============================================================================#
#===============================================================================#

# Google API credentials
YOUTUBE_API_KEY = 'YOUTUBE_API_KEY'
YOUTUBE_PLAYLIST_ID = 'YOUTUBE_PLAYLIST_ID'

# Spotify API credentials
SPOTIFY_CLIENT_ID = 'SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'SPOTIFY_CLIENT_SECRET'
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback'
SPOTIFY_PLAYLIST_ID = 'SPOTIFY_PLAYLIST_ID'

# Ignore Spotify results with these words
BLACKLIST = ['karaoke", "originally performed']

# Leave blank for random position
POSITION_TO_ADD = "0"

# Playlist ID file
VIDEO_ID_FILE = "video_ids.txt"

#===============================================================================#
#===============================================================================#


# Authenticate services
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-modify-public",
        open_browser=False
    )
)


# Get YouTube playlist videos
def main(youtube_service, youtube_playlist_id, video_id_file, spotify_playlist_id,blacklist,position_to_add):
    playlist_items = []
    next_page_token = None

    # Create video ID file if it doesn"t exist
    if not os.path.exists(video_id_file):
        with open(video_id_file, "x"):
            print(f"Created {video_id_file}")

    with open(video_id_file, "r") as f:
        file_contents = f.read()

    next_token = True

    while next_token:
        request = youtube_service.playlistItems().list(
            part="snippet",
            playlistId=youtube_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        # Check for duplicates and add to Spotify playlist
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            if video_id in file_contents or item['snippet']['title'] == "Deleted video":
                print(f"{item['snippet']['title']} already exists in {video_id_file} or is unavailable")
                next_token = False
                break
            else:
                playlist_items.append(item)
                add_spotify(item,youtube_service,spotify_playlist_id,blacklist,video_id_file,position_to_add)

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    # Save the video IDs to a text file
    with open(video_id_file, "a") as f:
        for item in playlist_items:
            video_id = item['snippet']['resourceId']['videoId']
            f.write(f"{video_id}\n")

    print(f"All video IDs have been saved to {video_id_file}")


# Add song to Spotify playlist
def add_spotify(item, youtube_service, spotify_playlist_id,blacklist,video_id_file,position_to_add):
    # Format title
    video_title = remove_brackets(item['snippet']['title'])

    # Add artist
    if "-" not in video_title:
        artist_name = get_video_uploader(youtube_service, item['snippet']['resourceId']['videoId'])
        track_query = f"{artist_name} - {video_title}"
        print(f"{track_query} - added artist")
    else:
        track_query = video_title

    # Search for tracks using text
    results = spotify.search(q=track_query, type="track", limit=5)
    tracks = results['tracks']['items']

    if not tracks:
        print(f"No tracks found for video: {video_title}")
    else:
        track_uri = None

        # Find the first track that doesn"t contain words in blacklist"
        for track in tracks:
            if not any(word in track['name'].lower() for word in blacklist):
                track_uri = track['uri']
                break

        if track_uri is None:
            print(f"No suitable tracks found for video: {video_title}")
        else:
            # Check if the track is already in the playlist
            playlist_tracks = spotify.playlist_items(playlist_id=spotify_playlist_id)['items']
            existing_track_uris = [item['track']['uri'] for item in playlist_tracks]

            if track_uri in existing_track_uris:
                print(f"Track already exists in the playlist: {track_query}")
            else:
                # Add the track to the playlist
                if position_to_add == "":   
                    with open(video_id_file, 'r') as f:
                        lines = len(f.readlines())
                    position = random.randint(0,lines)
                else:
                    position = position_to_add
                spotify.playlist_add_items(playlist_id=spotify_playlist_id, items=[track_uri], position=position) 
                print(f"Track added to the playlist {track_query}")


# Get uploader to titles without artist
def get_video_uploader(youtube_service, video_id):
    # Retrieve the video uploader
    video_response = youtube_service.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    # Extract the uploader from the video details
    if "items" in video_response and len(video_response['items']) > 0:
        uploader = video_response['items'][0]['snippet']['channelTitle']
        uploader = uploader.rstrip("- Topic").strip()
        return uploader

    return None


def remove_brackets(video_title):
    # Remove brackets and their contents from the video title
    video_title = re.sub(r"\[[^\]]*\]", "", video_title)  # Remove square brackets and their contents
    video_title = re.sub(r"\([^)]*\)", "", video_title)  # Remove round brackets and their contents
    video_title = re.sub(r"\"[^\']*\"", "", video_title)  # Remove double quotes and their contents
    return video_title.strip()


if __name__ == "__main__":
    main(youtube, YOUTUBE_PLAYLIST_ID, VIDEO_ID_FILE, SPOTIFY_PLAYLIST_ID, BLACKLIST, POSITION_TO_ADD)
