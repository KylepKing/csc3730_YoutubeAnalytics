#This is the main file were we call youtubes api and do the basic calculations
from dotenv import load_dotenv
from pathlib import Path
import os
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

env_path = Path(__file__).parent / '.env'
load_dotenv(env_path) #using this to load the secret variables from the .env file
api_key = os.getenv("API_KEY")

channel_id = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'  # Example channel ID
channel_ids = ['UCC8zWIx8aBQme-x1nX9iZ0A',
                'UCLLw7jmFsvfIVaUFsLs8mlQ',
                'UCiT9RITQ9PW6BhXK0y2jaeg',
                'UCpXBGqwsBkpvcYjsJBQ7LEQ',
                'UC2UXDak6o7rBm23k3Vv5dww'
              ]  # Example list of channel IDs

youtube = build('youtube', 'v3', developerKey=api_key)


## Function to get channel statistics
def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids))
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(Channel_name = response['items'][i]['snippet']['title'],
                Subscribers = response['items'][i]['statistics']['subscriberCount'],
                Views = response['items'][i]['statistics']['viewCount'],
                Total_videos = response['items'][i]['statistics']['videoCount'],
                playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
                )
        all_data.append(data)

    return all_data

channel_statistics = get_channel_stats(youtube, channel_ids)
channel_data = pd.DataFrame(channel_statistics)


playlist_id = channel_data.loc[channel_data['Channel_name']=='Ken Jee', 'playlist_id'].iloc[0]

##Function to get video ids from playlist
def get_video_ids(youtube, playlist_id):
    
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId = playlist_id,
        maxResults = 50)
    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id,
                maxResults = 50,
                pageToken = next_page_token)
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken') 

    return video_ids
    
video_ids = get_video_ids(youtube, playlist_id)


## Function to get video details
def get_video_details(youtube, video_ids):
    all_video_stats = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i+50]))  # Process 50 video IDs at a time
        response = request.execute()

        for video in response['items']:
            video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = video['statistics']['viewCount'],
                               Likes = video['statistics']['likeCount'],
                               Comments = video['statistics']['commentCount']
                               )
            all_video_stats.append(video_stats)
    return all_video_stats
video_details = get_video_details(youtube, video_ids)
video_data = pd.DataFrame(video_details)
video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Comments'] = pd.to_numeric(video_data['Comments'])

top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)

#average published video per month
video_data['Month'] = pd.to_datetime(video_data['Published_date']).dt.strftime('%b')

#gets you the amt of videos published per month
videos_per_month = video_data.groupby('Month', as_index=False).size()
sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories=sort_order, ordered=True) #sorts by month and fixes the index so it uses months as index
videos_per_month = videos_per_month.sort_index()

print("API key:", api_key)
print(channel_data)
print("YouTube Analytics module executed successfully.")
print(video_ids)
print(video_data)
print(videos_per_month)

# Converting data types so they can be used in visualizations
channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])   
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])
print(channel_data.dtypes)

#prints top ten videos of a channel by views
print(top10_videos)



# Visualization using seaborn
sns.set(rc={'figure.figsize':(10,8)})
ax = sns.barplot(x='Channel_name', y='Subscribers', data=channel_data) #example getting bar plot for subscribers
plt.show()
ax = sns.barplot(x='Channel_name', y='Views', data=channel_data) #example getting bar plot for views
plt.show()
ax = sns.barplot(x='Channel_name', y='Total_videos', data=channel_data) #example getting bar plot for total videos
plt.show()


# Visualization for top 10 videos by views
ax1 = sns.barplot(x='Views', y='Title', data=top10_videos)
plt.show()

#visualization for videos published per month
ax2 = sns.barplot(x='Month', y='size', data=videos_per_month)
plt.show()


#if you wanted to load this data frame data into a csv
# video_data.to_csv('Video_Details(Ken Jee).csv')