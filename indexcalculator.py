from textstat.textstat import textstat

import pandas as pd 
import matplotlib.pyplot as plt
from numpy.random import normal
import codecs
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class Tweet:
    def __init__(self,flesch,coleman,gunning,read,text):
        self.flesch=flesch
        self.coleman=coleman
        self.gunning=gunning
        self.readability=read
        self.text=text


    
field=['ID','# of RTs','HashTags','Tweet IDs','Time','Replier Id Strs','Retweeted Tweet User ID','Tweet Text','URLs in Tweet Text','Users','User Types','Parse Tree Edit Distance_strictPOSMatch','Parse Tree Edit Distance']
# just for reference

df = pd.read_csv('tweets2.csv', skipinitialspace=True, usecols=field)
#print(df)
tweet_holder=[]
co=0
for index, row in df.iterrows():


    str_holder=str(row['Tweet Text']).encode('utf-8').decode('utf-8')
    #print(str_holder)
    flesch=textstat.flesch_reading_ease(str_holder)
    coleman=textstat.coleman_liau_index(str_holder) 
    gunning=textstat.gunning_fog(str_holder)
    read=textstat.automated_readability_index(str_holder)

    #creating tweet
    tweet1=Tweet(flesch,coleman,gunning,read,str_holder)
    tweet_holder.append(tweet1)
    #print(tweet1)

    print(str(co) + " " +tweet1.text)
    print(tweet1.coleman)
    co=co+1





flesch_holder=[]

for tweet in tweet_holder:
    flesch_holder.append(tweet.coleman)

tweet_h_2=[x for y, x in sorted(zip(flesch_holder, tweet_holder))]


#print(tweet_h_2)



bins=[0,5,10,15,20,25,30]


file=codecs.open("readability.txt","w","utf-8")

#pd.concat([df1, df4], axis=1, join='inner')
columns = ['Flesch reading ease','Gunning fog index', 'Automated readability index','ColemanLiau index']
df_ = pd.DataFrame(columns=columns)


for index,tweet in enumerate(tweet_holder):
    df_.loc[index]=[tweet.flesch,tweet.gunning,tweet.readability,tweet.coleman]
    

#print(df_)

result = pd.concat([df, df_], axis=1)
#print(result)

result.to_csv("2updated_100_sample_tweet.csv", encoding='utf-8')
co2=0
for idx, val in enumerate(bins):

    try:
        file.write("****************************************************\n")
        file.write(str(val)+"-"+str(bins[idx + 1]) + "\n")


        for tweet in tweet_h_2:
            if(tweet.readability<=bins[idx+1] and tweet.coleman>val):
                print(str(co2) +" " +str(tweet.coleman )+" "+ tweet.text)
                #print(tweet.coleman,tweet.text)
                file.write(str(tweet.readability) + " "+ tweet.text+"\n")
                co2=co2+1

    except Exception as e:
        print(e)
        print("done.")
        file.close()
    

