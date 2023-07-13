from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd 
import emoji
extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    
    num_messages = df.shape[0]
    words = []
    links = []
    for message in df['message']:
        words.extend(message.split())
        links.extend(extract.find_urls(message))
    st1 = "<Media omitted>\n"
    num_media_messages = 0
    num_media_messages = df[df['message']==st1].shape[0]
    # for i in df['message']:
    #     if(i.startswith(st1)):
    #         num_media_messages=num_media_messages+1

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'] .value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    # print(stop_words)   

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    df1 = pd.DataFrame(Counter(words).most_common(20))
    return df1


# def emoji_helper(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     emojis = []
#     for message in df['message']:
#         emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))  

#     return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i]) + "-" + str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline1 = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline1

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()

def most_active_month(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def heat_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)