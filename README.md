# YouTube to Spotify Playlist Sync

This script allows you to synchronize a YouTube playlist with a Spotify playlist. It uses the YouTube Data API v3 to fetch videos from the specified YouTube playlist and then searches for corresponding tracks on Spotify to add them to the Spotify playlist. Youtube videos IDs are saved to a text file to prevent duplicates and minimise API calls.

## Prerequisites

Before running the application, you'll need to set up the following:

1. Obtain API keys for both YouTube and Spotify:
   - YouTube API Key: [Google Cloud Console](https://console.cloud.google.com)
   - Spotify API Key: [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)

2. Create a Spotify application and set the Redirect URI:
   - Follow the Spotify API documentation to create an application and set the Redirect URI.
   - Make sure to note down the Spotify Client ID, Client Secret, and Redirect URI for configuration.

3. Install the required Python libraries using pip:

```bash
pip install google-api-python-client spotipy
```

4. Replace the placeholders in the `sync.py` file:
- Replace `YOUR_YOUTUBE_API_KEY` with your YouTube API key.
- Replace `YOUR_YOUTUBE_PLAYLIST_ID` with the ID of the YouTube playlist to sync.
- Replace `YOUR_SPOTIFY_CLIENT_ID`, `YOUR_SPOTIFY_CLIENT_SECRET`, and `YOUR_SPOTIFY_REDIRECT_URI` with your Spotify application credentials.
- Replace `YOUR_SPOTIFY_PLAYLIST_ID` with the ID of the Spotify playlist to sync.

## Usage

To run the script:
`python3 sync.py`
It can also easily be automated using Cron to regularly sync playlists

## Customization

- You can add keywords to the `BLACKLIST` list to exclude specific words or phrases from Spotify search result. Tracks containing any of the words in the blacklist will be ignored.

- If you wish to modify the track title formatting, you can do so in the `remove_brackets()` function in `sync.py`. The function removes square brackets, round brackets, and double quotes from the video title.
