# The purpose of this script is to vectorize video descriptions/tags using TF-IDF
# After, it will cluster the videos based on these vectors to find similar content groups using K-Means clustering
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

# Function to get list of descriptions from video tags
def extract_descriptions(video_details):
    descriptions = []
    for video in video_details:
        description = (' '.join(video['snippet'].get('tags', '')))+video['snippet'].get('description', '')
        descriptions.append(description)
    return descriptions

# Function to vectorize video descriptions using TF-IDF
def tfidf_vectorize(descriptions):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    return tfidf_matrix, vectorizer

# Function to cluster videos using K-Means
def cluster_videos(tfidf_matrix, num_clusters=10):
    kmeans = KMeans(n_clusters=num_clusters, random_state=1)
    kmeans.fit(tfidf_matrix)
    return kmeans

if __name__ == "__main__":
    # Load data from JSON file
    with open('youtube_data.json', 'r', encoding="utf-8") as f:
        video_details = json.load(f)

    descriptions = extract_descriptions(video_details)
    tfidf_matrix, vectorizer = tfidf_vectorize(descriptions)
    kmeans = cluster_videos(tfidf_matrix)

    # Output cluster assignments
    for i, video in enumerate(video_details):
        print(f"Video ID: {video['id']} - Cluster: {kmeans.labels_[i]}")

    # Plot histogram of cluster sizes
    plt.hist(kmeans.labels_, bins=np.arange(kmeans.n_clusters + 1) - 0.5, edgecolor='black')
    plt.xlabel('Cluster')
    plt.ylabel('Number of Videos')
    plt.title('Video Clusters based on TF-IDF of Descriptions/Tags')
    plt.xticks(range(kmeans.n_clusters))
    plt.show()

    # Compare mean and standard deviation of log(likes) by cluster, plotting/saving boxplots for each cluster
    plt.figure(figsize=(10, 6))
    for cluster_num in range(kmeans.n_clusters):
        cluster_likes = []
        for i, video in enumerate(video_details):
            if kmeans.labels_[i] == cluster_num:
                stats = video.get('statistics', {})
                likes = int(stats.get('likeCount', 0))
                cluster_likes.append(np.log(likes + 1))
        if cluster_likes:
            mean_likes = np.mean(cluster_likes)
            std_likes = np.std(cluster_likes)
            print(f"Cluster {cluster_num}: Mean log(likes) = {mean_likes:.2f}, Std Dev = {std_likes:.2f}")
            plt.boxplot(cluster_likes, positions=[cluster_num], widths=0.6)
        else:
            print(f"Cluster {cluster_num}: No videos")

    plt.xlabel('Cluster')
    plt.ylabel('Log(Likes)')
    plt.title('Distribution of Log(Likes) by Cluster')
    plt.xticks(range(kmeans.n_clusters))
    plt.savefig('log_likes_by_cluster_boxplot.png')
    plt.show()