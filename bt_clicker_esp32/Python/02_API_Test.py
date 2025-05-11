# python3.11 -m pip install google-api-python-client oauth google-auth-oauthlib --user

import os, sys
print( sys.version )

from time import sleep

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = [
    "https://www.googleapis.com/auth/youtubepartner",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]
reqFreq = 1.0

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name    = "youtube"
api_version         = "v3"
client_secrets_file = "../../keys/client_secrets.json"


def cls():
    """ Clear CLI """
    os.system( 'clear' )
    sleep( 0.01 )
    os.system( 'clear' )


def get_flow_credentials_yt( client_secrets_file, scopes ):
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, 
        scopes
    )
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, 
        api_version, 
        credentials = credentials
    )
    cls()
    return flow, credentials, youtube

flow, credentials, youtube = get_flow_credentials_yt( client_secrets_file, scopes )

# Get video details
video_response = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id=video_id
).execute()

# Check if video exists
if not video_response.get('items'):
    return {"error": f"No video found with ID: {video_id}"}

# Extract relevant information
video_data = video_response['items'][0]
snippet = video_data['snippet']
statistics = video_data['statistics']

# Format the information
video_info = {
    "title": snippet['title'],
    "channel_name": snippet['channelTitle'],
    "channel_id": snippet['channelId'],
    "published_at": snippet['publishedAt'],
    "description": snippet.get('description', '')[:100] + "..." if len(snippet.get('description', '')) > 100 else snippet.get('description', ''),
    "view_count": statistics.get('viewCount', 'N/A'),
    "like_count": statistics.get('likeCount', 'N/A'),
    "comment_count": statistics.get('commentCount', 'N/A'),
    "tags": snippet.get('tags', [])[:5] if 'tags' in snippet else [],
}