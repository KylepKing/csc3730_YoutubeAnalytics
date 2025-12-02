
# Exploratory Data Analysis (EDA) for YouTube Video Dataset
import json
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    # Load data from JSON file
    with open('youtube_data.json', 'r', encoding="utf-8") as f:
        video_details = json.load(f)

    # Extract video likes, views, and comments
    likes = []
    views = []
    comments = []
    for video in video_details:
        stats = video.get('statistics', {})
        likes.append(np.log(int(stats.get('likeCount', 0)) + 1))
        views.append(np.log(int(stats.get('viewCount', 0)) + 1))
        comments.append(np.log(int(stats.get('commentCount', 0)) + 1))
    
    # Plot distributions
    plt.figure(figsize=(8, 5))
    plt.subplot(1, 2, 1)
    plt.hist(likes, bins=50, color='blue', alpha=0.7)
    plt.title('Distribution of Likes')
    plt.xlabel('Number of Likes (log scale)')
    plt.ylabel('Number of Videos')
    
    plt.subplot(1, 2, 2)
    plt.hist(comments, bins=50, color='red', alpha=0.7)
    plt.title('Distribution of Comments')
    plt.xlabel('Number of Comments (log scale)')
    plt.ylabel('Number of Videos')
    
    plt.tight_layout()
    plt.show()

    # Create histogram of number of tags
    num_tags = [np.log(len(video['snippet'].get('tags', [])) + 1) for video in video_details]
    plt.figure(figsize=(6, 4))
    plt.hist(num_tags, bins=30, color='green', alpha=0.7)
    plt.title('Distribution of Number of Tags per Video')
    plt.xlabel('Number of Tags (log scale)')
    plt.ylabel('Number of Videos')
    plt.show()
