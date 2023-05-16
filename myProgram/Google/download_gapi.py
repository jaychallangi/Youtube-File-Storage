import os
import google.auth
import google_auth_oauthlib
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import urlparse, parse_qs

# Replace with your own credentials
CLIENT_SECRETS_FILE = "Credentials/client_secret_328977920138-f584r71j9fse29l4rb09ufrllkghnftb.apps.googleusercontent.com.json"
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Authorize the API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server()
youtube = build(API_NAME, API_VERSION, credentials=credentials)

# Replace with your video URL or ID
VIDEO_URL = "https://www.youtube.com/watch?v=ladyKuD0f4M"
parsed_url = urlparse(VIDEO_URL)
video_id = parse_qs(parsed_url.query)["v"][0]

try:
    # Get video metadata
    video_request = youtube.videos().list(
        part="id,snippet",
        id=video_id
    )
    video_response = video_request.execute()
    video = video_response["items"][0]

    # Get the download URL
    stream_map_request = youtube.videos().list(
        part="id,snippet,streamingDetails",
        id=video_id
    )
    stream_map_response = stream_map_request.execute()
    stream_map = stream_map_response.get("items", [])[0].get("streamingDetails", {}).get("adaptiveFormats", [])
    stream_url = None
    for stream in stream_map:
        if "url" in stream:
            stream_url = stream["url"]
            break
    if not stream_url:
        raise Exception("Failed to get stream URL")

    # Download the video
    filename = f"{video['snippet']['title']}.mp4"
    os.system(f"wget -O '{filename}' '{stream_url}'")
    print(f"Video downloaded to {filename}")
except HttpError as e:
    print(f"An error occurred: {e}")
