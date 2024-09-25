import os
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
import pandas as pd
import requests
from urllib.parse import urlparse, parse_qs
import pprint

# Load API key from environment variables
load_dotenv(dotenv_path='./config/.env')
api_key = os.getenv("API_KEY")

def get_video_details(youtube, video_id):
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    
    if 'items' in response and len(response['items']) > 0:
        video_title = response['items'][0]['snippet']['title']
        return video_title
    return None

def get_comments(youtube, **kwargs):
    comments = []
    results = youtube.commentThreads().list(**kwargs).execute()
   
    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # Check if there are more comments
        
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = youtube.commentThreads().list(**kwargs).execute()
        else:
            break
 
    return comments

def check_comments_enabled(video_id, api_key):
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        'part': 'statistics',
        'id': video_id,
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return False
    
    video_details = response.json()
    if video_details['items']:
        # Check if comments are enabled based on comment count
        comment_count = int(video_details['items'][0]['statistics'].get('commentCount', 0))
        return comment_count > 0, comment_count
    return False, 0

def main(video_id, api_key):
    # Disable OAuthlib's HTTPs verification when running locally.
    #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=api_key
    )
    
    # Fetch video title
    video_title = get_video_details(youtube, video_id)
    
    # Check if comments are enabled
    comments_enabled, comment_count = check_comments_enabled(video_id, api_key)
    if comments_enabled:
        comments = get_comments(youtube, part="snippet", videoId=video_id, textFormat="plainText")
        print(f"Video Title: {video_title}")
        print(f"Number of comments: {comment_count}")
    else:
        comments = ["The comments are disabled for this video."]
        print("The comments are disabled for this video.")
    
    return video_title, comments

def get_video_comments(video_id):
    video_id = extract_video_id(video_id)
    print(f"Extracted Video ID: {video_id}")
    return main(video_id, api_key)

def extract_video_id(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Check if it's a typical YouTube URL
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
        # Handle URLs like https://www.youtube.com/watch?v=video_id
        if parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        # Handle URLs like https://www.youtube.com/embed/video_id
        if parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        # Handle URLs like https://www.youtube.com/v/video_id
        if parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    # Check if it's a shortened YouTube URL
    elif parsed_url.hostname in ['youtu.be']:
        # Handle URLs like https://youtu.be/video_id
        return parsed_url.path.split('/')[1]
    
    return None

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=YHxj3LvZoLQ"  # Replace with your video URL
    video_title, comments = get_video_comments(video_url)
   
    # Display video title and comments in a DataFrame
    df = pd.DataFrame(comments, columns=["Comment"])
    print(f"Video Title: {video_title}")
    print(df)
