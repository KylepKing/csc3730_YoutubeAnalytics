
# csc3730_YoutubeAnalytics
This is a repository for a Machine Learning Project in which we scrape data from the Youtube API and run analysis on the data for the different trending video categories of Youtube.
We call the Api to get the top 200 trending vidoes for the day then grab their channel id's. With that we call the api again to get the 20 most recently posted vidoes of those channels that had a trending video. We then store all of that in a JSON file which stores a list of dictionaries. We average a range of 3800-4000 videos in our dataset per run of this project. 


# Setup
1.Pull from this repo
2.Create in the root a .env file and add the API_KEY=google key variable. The Api key is in a txt file called API_KEY_INFO.txt
3. pip install all packages used (pandas, dotenv, seaborn, google-api-python-client) ex: pip install google-api-python-client
4. save and run code.

