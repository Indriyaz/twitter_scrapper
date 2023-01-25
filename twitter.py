# Importing the MongoClient class from the pymongo library,
# which is used to interact with MongoDB databases.
from pymongo import MongoClient

# Importing the Pandas library,
# which is used to create and manipulate dataframes.
import pandas as pd

# Importing the streamlit library,
# which is used to create the interactive web app.
import streamlit as st

# Importing the datetime module from the Python standard library,
# which is used to generate timestamps.
import datetime as dt

# Importing the TwitterSearchScraper class from the snscrape library,
# which is used to scrape tweets from Twitter.
from snscrape.modules.twitter import TwitterSearchScraper

# MongoDB Connection address.
localhost = ("mongodb://127.0.0.1:27017/"
             "?directConnection=true&serverSelection"
             "TimeoutMS=2000")

# Database name to be selected for upload of collections.
database = "test2"

# Filepath to save files.
filepath = "C:/Users/R2/Downloads/"

# Timestamp in the format of DD-MM-YY HH:MM:SS.
timestamp = dt.datetime.now().strftime("%d-%m-%y %H:%M:%S")

# Created empty list to store the data,
# before converting it to a data frame.
e_list = []

# Input from the user for number of days the tweets to scrape.
no_of_days = (st.text_input("Enter number of days in numbers"))

# Input from the user for the word or hashtag to search.
keyword = st.text_input("Enter the word to search")

# It Concatenates keyword and days,
# as scraper allows query in a predefined format.
search = keyword + f" within_time:{no_of_days}d"

# For naming the file.
file_name = (keyword + timestamp)

# Input from the user for number of tweets to scrape.
no_of_tweets = (st.text_input("Enter the number of tweet count"))

# assigning variable to start the scraping tweets.
scraper = TwitterSearchScraper


# Created the function to start scraping the tweets.
def logic():
    # Created  a variable which helps in counting the no of iterations,
    # and used to stop the loop.
    a = 1
    # Converts the string to integer from (no_of_tweets) to integer,
    # and stores  in the variable.
    int_no_of_tweets = int(no_of_tweets)
    # Creates a loop to search for tweets.
    for tweet in scraper(search).get_items():
        if a <= int_no_of_tweets:
            # It appends the tweets to the empty list (e_list).
            e_list.append([tweet.date, tweet.id, tweet.url, tweet.content,
                           tweet.user, tweet.replyCount,
                           tweet.retweetCount, tweet.lang,
                           tweet.sourceLabel, tweet.likeCount])
            # It increments the variable (a) for every loop.
            a += 1
        else:
            break

# The session_state variables are used to keep track of,
# whether the user has clicked on a button,
# such as the "Submit" button, and to determine whether certain actions,
# such as uploading data to the database or downloading a file,
# should be performed,
# This allows the user to interact with the app in a more intuitive way,
# by allowing them to take different actions depending,
# on the current state of the app.
# Session_state for submit Button.
if "submit" not in st.session_state:
    st.session_state["submit"] = False

# Session_state for upload Button.
if "upload" not in st.session_state:
    st.session_state["upload"] = False

# Session_state for CSV Button.
if "CSV" not in st.session_state:
    st.session_state["CSV"] = False

# Session_state  for JSON Button.
if "JSON" not in st.session_state:
    st.session_state["JSON"] = False

# Session_state  for Counter it helps in Counting,
# how many times a button is pressed.
if "counter" not in st.session_state:
    st.session_state["counter"] = 0

# Creates a button for submit.
if st.button("Submit"):
    st.session_state["submit"] = not st.session_state["submit"]

# Checks if submit button is clicked.
if st.session_state["submit"]:
    logic()
    # creates dataframe with given column names.
    data = pd.DataFrame(e_list, columns=["Date", "id", "url", "content",
                                         "user", "ReplyCount", "RetweetCount",
                                         "language", "source", "likeCount"])
    # It displays the data in streamlit app.
    st.dataframe(data)
    # It creates a button to upload.
    if st.button("Upload data to database"):
        st.session_state["upload"] = not st.session_state["upload"]
    # Checks for upload button is clicked.
    if st.session_state["upload"]:
        # It increments the counter to 1 when upload button is clicked.
        st.session_state["counter"] += 1
        # when is upload button is pressed for first time.
        if st.session_state["counter"] == 1:
            # connects the local hosted MongoDB.
            client = MongoClient(localhost)
            # Selects the database.
            db = client[database]
            # creates a new collection name in database.
            db.create_collection(file_name)
            # Converts the dataframe  into a dictionary format,
            # with the argument "records" specifying that each
            # row of the DataFrame should be a dictionary.
            data_dict = data.to_dict("records")
            # selects the collection in database.
            collection = db[file_name]
            # Inserts the dataframe in selected collections,
            # with multiple records.
            collection.insert_many(data_dict)
            # Displays a message after upload to database.
            st.write("uploaded successfully")
        # when upload is pressed for more than 1 time.
        else:
            # Displays a message.
            st.write("Already uploaded")
    # Creates expandable button list.
    with st.expander("Download"):
        # Checks for csv button is clicked.
        if st.button("CSV"):
            st.session_state["CSV"] = not st.session_state["CSV"]
        # Checks for json button is clicked.
        if st.button("JSON"):
            st.session_state["JSON"] = not st.session_state["JSON"]
    # Changes filename to format which is accepted by os
    file_name_s = (file_name.replace(":", "-"))
    # When csv button is clicked.
    if st.session_state["CSV"]:
        # It writes data to a folder with filename.
        data.to_csv(filepath+file_name_s+".csv",
                    index=False, header=True)
        # It helps in downloading file multiple times
        st.session_state["CSV"] = False
        # Displays message after download.
        st.write("csv downloaded")
    # When json button is clicked.
    if st.session_state["JSON"]:
        # It writes data to a folder with filename.
        data.to_json(filepath+file_name_s+".json")
        # It helps in downloading file multiple times
        st.session_state["JSON"] = False
        # Displays message after download.
        st.write("json downloaded")
