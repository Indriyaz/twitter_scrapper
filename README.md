# twitter_scrapper

This is a simple web app that allows users to scrape tweets from Twitter using the snscrape library and upload them to a MongoDB database. The app also allows users to download the scraped tweets in either CSV or JSON format.
```
#Usage:
To use the app, 
simply enter the number of days you want to scrape tweets for, 
the word or hashtag you want to search for, 
and the number of tweets you want to scrape. 
Then click the "Submit" button to start scraping tweets. 
The scraped tweets will be displayed in a dataframe.
You can then click the "upload data to database" button to upload the scraped tweets to a MongoDB database. 
The app will create a new collection in the "test2" database with the name of the keyword and timestamp.
You can also download the scraped tweets in either CSV or JSON format by clicking the "download" button 
and then selecting either "CSV" or "JSON". 
The downloaded files will be saved in the "C:/Users/R2/Downloads/" directory with the name of the keyword and timestamp.
```
```
#Requirements:
python 3.x
streamlit
pymongo
pandas
snscrape
MongoDB
```
```
#Limitations:
The app is currently set up to connect to a MongoDB database running on the localhost on port 27017. 
If you want to connect to a different MongoDB database, you will need to change the "localhost" variable.
The app is set to save collections in database "test2".
If you want to write it different databse ,you will need to change the "database" varaible.
The app is also set up to save downloaded files in the "C:/Users/R2/Downloads/" directory. 
If you want to save the files in a different directory, you will need to change the "filepath" variable.
```
```
#Notes:
The app uses the SessionState
```
