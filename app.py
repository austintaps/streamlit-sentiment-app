import streamlit as st
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re 
import seaborn as sns



consumerKey = "c6GmhupterzhIxLgYjxtTDmNw"
consumerSecret = "CdIE2dBXCKQAAXpuIIA3nb6noxvkode0qDHG5TqXF5AIgM2dMp"
accessToken ="1088432068403572738-cAX8fc7geKhKefmE0NjHu8mBo5xWBs"
accessTokenSecret ="H0UYpZZBgun9EuFpWIMUtO2flWMygLh4JScrKBjSmVciT"


#Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey,consumerSecret)
authenticate.set_access_token(accessToken, accessTokenSecret) 
    
# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)

#plt.style.use('fivethirtyeight')

st.title("Twitter Sentiment Visualisation app")
def app():


	st.title("Tweet Analyzer 🔥")


	activities=["Tweet Analyzer","Generate Twitter Data"]

	choice = st.sidebar.selectbox("Select Your Activity",activities)

	

	if choice=="Tweet Analyzer":

		st.subheader("Analyze the tweets of your favourite Personalities")

		st.subheader("This tool performs the following tasks :")

		st.write("1. Fetches the 1000 most recent tweets from the given twitter handel")
		st.write("3. Performs Sentiment Analysis a displays it in form of a Bar Graph")


		


		raw_text = st.text_area("Enter the political keyword you want")



		st.markdown("<--------     Also Do checkout the another cool tool from the sidebar")

		Analyzer_choice = st.selectbox("Select the Activities",  ["Show Recent Tweets","Visualize the Sentiment Analysis"])


		if st.button("Analyze"):

			
			if Analyzer_choice == "Show Recent Tweets":

				st.success("Fetching last 1000 Tweets")

				
				def Show_Recent_Tweets(raw_text):

					# Extract 1000 tweets from the twitter user
					posts = api.user_timeline(screen_name=raw_text, count = 1000, lang ="en", tweet_mode="extended")

					
					def get_tweets():

						l=[]
						i=1
						for tweet in posts[:100]:
							l.append(tweet.full_text)
							i= i+1
						return l

					recent_tweets=get_tweets()		
					return recent_tweets

				recent_tweets= Show_Recent_Tweets(raw_text)

				st.write(recent_tweets)



			



			else:



				
				def Plot_Analysis():

					st.success("Generating Visualisation for Sentiment Analysis")

					


					posts = api.user_timeline(screen_name=raw_text, count = 1000, lang ="en", tweet_mode="extended")

					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


					
					# Create a function to clean the tweets
					def cleanTxt(text):
					 text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
					 text = re.sub('#', '', text) # Removing '#' hash tag
					 text = re.sub('RT[\s]+', '', text) # Removing RT
					 text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
					 
					 return text


					# Clean the tweets
					df['Tweets'] = df['Tweets'].apply(cleanTxt)


					def getSubjectivity(text):
					   return TextBlob(text).sentiment.subjectivity

					# Create a function to get the polarity
					def getPolarity(text):
					   return  TextBlob(text).sentiment.polarity


					# Create two new columns 'Subjectivity' & 'Polarity'
					df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
					df['Polarity'] = df['Tweets'].apply(getPolarity)


					def getAnalysis(score):
					  if score < 0:
					    return 'Positive'
					  elif score == 0:
					    return 'Neutral'
					  else:
					    return 'Negative'
					    
					df['Analysis'] = df['Polarity'].apply(getAnalysis)


					return df



				df= Plot_Analysis()



				st.write(sns.countplot(x=df["Analysis"],data=df))


				st.pyplot(use_container_width=True)

				

	

	else:

		st.subheader("This tool fetches the last 100 tweets from the twitter handel & Performs the following tasks")

		st.write("1. Converts it into a DataFrame")
		st.write("2. Cleans the text")
		st.write("3. Analyzes Subjectivity of tweets and adds an additional column for it")
		st.write("4. Analyzes Polarity of tweets and adds an additional column for it")
		st.write("5. Analyzes Sentiments of tweets and adds an additional column for it")






		user_name = st.text_area("*Enter the exact twitter handle of the Personality (without @)*")

		st.markdown("<--------     Also Do checkout the another cool tool from the sidebar")

		def get_data(user_name):

			posts = api.user_timeline(screen_name=user_name, count = 1000, lang ="en", tweet_mode="extended")

			df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

			def cleanTxt(text):
				text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
				text = re.sub('#', '', text) # Removing '#' hash tag
				text = re.sub('RT[\s]+', '', text) # Removing RT
				text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
				return text

			# Clean the tweets
			df['Tweets'] = df['Tweets'].apply(cleanTxt)


			def getSubjectivity(text):
				return TextBlob(text).sentiment.subjectivity

						# Create a function to get the polarity
			def getPolarity(text):
				return  TextBlob(text).sentiment.polarity


						# Create two new columns 'Subjectivity' & 'Polarity'
			df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
			df['Polarity'] = df['Tweets'].apply(getPolarity)

			def getAnalysis(score):
				if score < 0:
					return 'Negative'

				elif score == 0:
					return 'Neutral'


				else:
					return 'Positive'

		
						    
			df['Analysis'] = df['Polarity'].apply(getAnalysis)
			return df

		if st.button("Show Data"):

			st.success("Fetching Last 100 Tweets")

			df=get_data(user_name)

			st.write(df)



	st.subheader(' ------------------------Created By :  Tapiwa A Kaemba-------------------- :sunglasses:')
	st.subheader(' ------------------------Created By : Jamie D kazungu sunglasses:')
	st.subheader(' ------------------------Created By :  Felix M Nezirayi-------------------- :sunglasses:')


			

				
if __name__ == "__main__":
	app()
