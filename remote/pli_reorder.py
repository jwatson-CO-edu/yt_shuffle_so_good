# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.update
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import googleapiclient.discovery

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "YOUR_API_KEY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.playlistItems().update(
        part="snippet",
        body={
          "id": "YOUR_PLAYLIST_ITEM_ID",
          "snippet": {
            "playlistId": "YOUR_PLAYLIST_ID",
            "position": 1,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": "YOUR_VIDEO_ID"
            }
          }
        }
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()