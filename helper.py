import pandas as pd
from wordcloud import WordCloud
from urlextract import URLExtract
extractor = URLExtract()
from collections import Counter
import emoji

def fetch_stats(selected_user,df):
    if(selected_user!="Overall"):
        df = df[df['user']==selected_user]
    
    #total messages
    num_messages = df.shape[0]    
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    #total media share
    num_media_msg = df[df['message']=='<Media omitted>\n'].shape[0]

    #total links shared
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages,len(words),num_media_msg,len(links)

def monthly_timeline(selected_user,df):
    if(selected_user!="Overall"):
        df = df[df['user']==selected_user]

    monthly_timeline=df.groupby(['year','month'])['message'].count()
    monthly_timeline = pd.DataFrame(monthly_timeline).reset_index()

    time=[]
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline.loc[i]['month'] + "-" + str(monthly_timeline.loc[i]['year']))

    monthly_timeline.drop(columns=['month','year'],inplace=True)
    monthly_timeline['time']=time
    monthly_timeline.rename(columns={'message':'count'},inplace=True)
    return monthly_timeline

def daily_timeline(selected_user,df):
    if(selected_user!="Overall"):
        df = df[df['user']==selected_user]

    df['just_date']=df['date'].dt.date
    daily_timeline = df.groupby(['just_date'])['message'].count()
    daily_timeline = pd.DataFrame(daily_timeline).reset_index()
    daily_timeline.rename(columns={'message':'count'},inplace=True)

    return daily_timeline

def weekly_activity(selected_user,df):
    if(selected_user!="Overall"):
        df = df[df['user']==selected_user]

    return df['day_name'].value_counts()

def monthly_activity(selected_user,df):
    if(selected_user!="Overall"):
        df = df[df['user']==selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if(selected_user!="Overall"):
        df = df[df['user']==selected_user]
    pivot_table = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return pivot_table

def most_busy_users(df):
    x = df['user'].value_counts().head()
    busy_df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'percent':'name', 'count':'percent'})
    return x,busy_df

def create_wordcloud(selected_user,df):
    if(selected_user!="Overall"):
        df = df[df['user']==selected_user]

    temp = df[df['user']!='group_notification']
    temp = temp[temp['message']!="<Media omitted>\n"]

    f = open('./stop_words_hinglish.txt','r')
    stop_words = f.read()

    def remove_stop_words(message):
        lst=[]
        for word in message.lower().split():
            if word not in stop_words:
                lst.append(word)
        
        return " ".join(lst)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(df[df['message']!='<Media omitted>\n']['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user,df):
    if(selected_user!="Overall"):
        df = df[df['user']==selected_user]

    temp = df[df['user']!='group_notification']
    temp = temp[temp['message']!="<Media omitted>\n"]

    f = open('./stop_words_hinglish.txt','r')
    stop_words = f.read()

    words = []

    for messages in temp['message']:
        for word in messages.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_words_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words_df

def most_common_emoji(df):
    emojis = []
    for messages in df['message']:
        for word in messages.lower().split():
            if emoji.is_emoji(word):
                emojis.append(word)
    emoji_df = pd.DataFrame(Counter(emojis).most_common(10))
    return emoji_df