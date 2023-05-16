import os
import google.auth
from google.oauth2.credentials import Credentials
import google_auth_oauthlib
from googleapiclient.discovery import build
from pytube import YouTube

# Set up the credentials
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Credentials/client_secret_328977920138-f584r71j9fse29l4rb09ufrllkghnftb.apps.googleusercontent.com.json'
# credentials, project_id = google.auth.default(scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
# youtube = build('youtube', 'v3', credentials=credentials)
CLIENT_SECRETS_FILE = "Credentials/client_secret_328977920138-f584r71j9fse29l4rb09ufrllkghnftb.apps.googleusercontent.com.json"
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Replace with the path to your video file
# VIDEO_FILE = "temp.txt_17968.mp4"

# Authorize the API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_console()
youtube = build(API_NAME, API_VERSION, credentials=credentials)
# Get the video link
video_id = 'VIDEO_ID'
request = youtube.videos().list(
            part='snippet',
            id=video_id
          )
response = request.execute()
video_link = f"https://www.youtube.com/watch?v=ladyKuD0f4M"

# Download the video
yt = YouTube(video_link)
yt.streams.first().download()
