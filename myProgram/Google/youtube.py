import os
import google_auth_oauthlib.flow
import googleapiclient.errors
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Replace with your own credentials
CLIENT_SECRETS_FILE = "Credentials/client_secret_328977920138-f584r71j9fse29l4rb09ufrllkghnftb.apps.googleusercontent.com.json"
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Replace with the path to your video file
VIDEO_FILE = "temp.txt_17968.mp4"

# Authorize the API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_console()
youtube = build(API_NAME, API_VERSION, credentials=credentials)

# Upload the video
media = MediaFileUpload(VIDEO_FILE)
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "test file upload from youtube",
            "description": "this a video uploaded from python"
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=media
)
response = request.execute()
print(response)
