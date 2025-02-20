import pickle
import json
import argparse
import os
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build


CLIENT ='client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']


API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


if __name__ == '__main__':
    try:
        with open('youtube.pkl', 'rb') as yt_pickle:
            youtube = pickle.load(yt_pickle)
    except(OSError, IOError):
        with open('youtube.pkl', 'wb') as yt_pickle:
            youtube = get_authenticated_service()
            pickle.dump(youtube, yt_pickle)

request = youtube.videos().list(
        part="statistics",
        id="PASTE VIDEO ID HERE"
)


response = request.execute()
newDict={}
for item in response['items']:
    newDict.update(item)
response['items']=newDict
Views=str(response['items']['statistics']['viewCount'])

def make_ordinal(n):
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix

ordinalViews=make_ordinal(Views)

request2 = youtube.videos().update(
        part="snippet,status,localizations",
        body={
          "id": "PASTE VIDEO ID HERE",
          "snippet": {
            "categoryId": "Your category ID",
            "description":"Your Description",
            "tags": ['Your tags here'],
            "title": "You are the "+ordinalViews+" person to click on this video!"
          }
        }
    )
response2 = request2.execute()
print(response2)
