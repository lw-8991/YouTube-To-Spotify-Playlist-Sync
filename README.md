# YouTube-to-Spotify Playlist Sync

YouTube-to-Spotify Playlist Sync is a Python script that helps you synchronize your YouTube playlist with a corresponding Spotify playlist. It fetches the videos from your YouTube playlist, searches for their corresponding tracks on Spotify, and adds them to your Spotify playlist.

## Requirements

Before using the script, you'll need the following:

- [YouTube API Key](https://developers.google.com/youtube/registering_an_application) (to access the YouTube API)
- [Spotify API Credentials](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app) (to access the Spotify API)
- Python 3.x

## Installation

1. Clone this repository to your local machine.

2. Install the required Python libraries using pip:

```bash
pip install google-api-python-client spotipy
Obtain the YouTube API key and Spotify API credentials and replace the placeholders in the script (YOUR_YOUTUBE_API_KEY, YOUR_SPOTIFY_CLIENT_ID, YOUR_SPOTIFY_CLIENT_SECRET, YOUR_SPOTIFY_REDIRECT_URI, YOUR_SPOTIFY_PLAYLIST_ID).
Usage
Prepare your YouTube and Spotify playlist IDs and ensure your video ID file (video_ids.txt) is created or exists in the repository directory.

Run the script:

bash
Copy code
python playlist_sync.py
The script will fetch the videos from your YouTube playlist and search for corresponding tracks on Spotify. If a suitable track is found, it will be added to your Spotify playlist. If not, the video will be skipped.

The script will keep track of added videos using the video_ids.txt file, preventing duplicates in the future runs.

Customization
You can customize the script to ignore certain Spotify results by adding or modifying entries in the BLACKLIST list. This helps to filter out unwanted tracks based on keywords.

Disclaimer
This script is intended for personal use and may have limitations due to changes in the YouTube and Spotify APIs. Use it responsibly and respect the terms of service of the respective platforms.
