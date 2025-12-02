from googleapiclient.discovery import build
from pathlib import Path
import json
import os
# Load API key from .env file
API_KEY = os.getenv('API_KEY')

youtube = build("youtube", "v3", developerKey=API_KEY)

MAX_VIDEOS_PER_CHANNEL = 20 

# Function to get trending videos from Youtube
def get_trending_videos(max_videos=200, region="US"):
    videos = []
    next_page_token = None

    while len(videos) < max_videos:
        response = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            maxResults=50,
            regionCode=region,
            pageToken=next_page_token
        ).execute()

        videos.extend(response["items"])
        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return videos[:max_videos]


# Function to get uploads playlist ID for a channel
def get_uploads_playlist_id(channel_id):
    response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


# Function to get recent videos from a playlist
def get_recent_videos_from_playlist(playlist_id, max_videos=MAX_VIDEOS_PER_CHANNEL):
    response = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=max_videos
    ).execute()

    return [item["contentDetails"]["videoId"] for item in response["items"]]


# Function to get video details in batches
def get_video_details_batch(video_ids):
    all_video_details = []
    
    # Process in batches of 50
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        
        try:
            response = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(batch)
            ).execute()
            
            all_video_details.extend(response["items"])
            
        except Exception as e:
            print(f"Error fetching batch {i//50 + 1}: {e}")
    
    return all_video_details


# Main execution for data downloading
if __name__ == "__main__":
    print("Fetching top 200 trending videos...")
    trending_videos = get_trending_videos()

    # Extract unique channel IDs
    channel_ids = list({v["snippet"]["channelId"] for v in trending_videos})
    print(f"Found {len(channel_ids)} unique channels in trending list.")

    # Fetch 20 most recent videos from each channel
    all_recent_video_ids = []

    for channel_id in channel_ids:
        try:
            uploads_playlist_id = get_uploads_playlist_id(channel_id)
            recent_videos = get_recent_videos_from_playlist(uploads_playlist_id, MAX_VIDEOS_PER_CHANNEL)
            all_recent_video_ids.extend(recent_videos)

        except Exception as e:
            print(f"Error fetching for channel {channel_id}: {e}")

    print(f"Pulled {len(all_recent_video_ids)} recent videos from trending channels.")

    # Fetch detailed information for all recent videos using batched API calls
    print("Fetching detailed information for recent videos (batched)...")
    recent_video_details = get_video_details_batch(all_recent_video_ids)
    
    # Save only the recent videos list to JSON file
    output_file = "youtube_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(recent_video_details, f, indent=2, ensure_ascii=False)
    
    print(f"\nData saved to {output_file}")
    print(f"Total videos saved: {len(recent_video_details)}")