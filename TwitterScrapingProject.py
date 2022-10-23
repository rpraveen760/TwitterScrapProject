import streamlit as st 
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime 
from pymongo import MongoClient

@st.experimental_singleton
def getDatabase() :
    connection_string = "mongodb://localhost:27017/"
    client = MongoClient(connection_string)
    return client['mydatabase']

@st.experimental_memo(ttl=600)
def postdata(record):
    dbname = getDatabase()
    Collection_Name = dbname['twitter']
    print(dbname.twitter.insert_many(record))
 

form = st.form(key="test")
tweet_count = form.number_input("Enter tweet count",min_value=1,step=1)
keyword = form.text_input("Enter the keyword")
start_date = form.date_input("Enter starting date")
end_date = form.date_input("Enter end date")
submit = form.form_submit_button("Submit")

if submit :
        # Creating list to append tweet data to
    tweets_list2 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    #print(keyword)
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword+' since:'+str(start_date)+' until:'+str(end_date)).get_items()):
        if i>tweet_count-1:
            break
        tweets_list2.append([tweet.date, tweet.id,tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.source,tweet.likeCount])
        
    # Creating a dataframe from the tweets list above
    tweets_df2 = pd.DataFrame(tweets_list2, columns=['Date', 'Tweet Id', 'Url', 'Content','User','Reply Count','Retweet Count','Language','Source','Like Count'])
    st.write(tweets_df2)
    download = st.download_button(label = 'Download data as .csv', data = tweets_df2.to_csv().encode('utf-8'), file_name = 'tweet_data.csv',mime='text/csv')
    download2 = st.download_button(label = 'Download data as JSON', data = tweets_df2.to_json(), file_name = 'tweet_data.json',mime='application/json')
    upload = st.button('Upload to Database',on_click=postdata(tweets_df2.to_dict('record')))






