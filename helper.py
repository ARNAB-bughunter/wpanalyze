from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

stop_word = ['to', "wasn't", 'can', 'because', 'any', 'itself', 'before', 'into', "you'll", 'after', 'how', 'such', 'himself', 't', 'most', 'has', 'wouldn', 'until', 'his', 'do', 'during', "you've", 'both', 'themselves', 's', 'was', 'few', "isn't", "mustn't", 'him', "couldn't", 'of', 'at', 'i', 'having', 'which', 'she', 'ourselves', 'out', 'your', 'again', 'from', 'ma', "won't", 'so', 'who', 'in', 'mustn', 'm', "doesn't", 'further', 'up', 'her', 'herself', 'all', 'some', 'each', 'just', 'down', 'doesn', 'hasn', 'ain', 'didn', 'were', 'nor', 'd', 'their', 'why', "mightn't", 'here', "didn't", "you'd", 'once', 'now', 'o', 'doing', 'hadn', 'below', 'does', 'my', 'is', 'll', 'whom', 'for', 'he', 'theirs', 'but', 'about', 'very', 'ours', 'when', 'against', "haven't", 'been', 'if', 'not', "should've", 'did', 'had', 'more', 'these', 'isn', "hasn't", 'needn', 'shouldn', 'me', "you're", 'than', 'weren', 'are', 're', 'no', 'have', 'we', 'this', 'own', 'mightn', 'or', 'same', 'yourself', 'an', "don't", 'aren', 'haven', "needn't", 'wasn', 've', 'as', 'a', 'only', "wouldn't", 'the', 'under', 'couldn', 'other', 'yours', 'then', 'it', 'am', 'they', 'where', 'shan', "shouldn't", 'too', 'hers', 'through', 'by', 'yourselves', 'those', "shan't", 'myself', 'above', 'will', 'while', 'should', 'over', 'them', 'y', 'don', 'off', 'there', 'our', 'with', 'what', 'and', "weren't", 'between', 'its', 'be', "she's", "hadn't", 'being', 'that', "aren't", 'won', 'on', 'you', "it's", "that'll","<Media","omitted>"]

def fetch_stats(selected_user,df):
	if selected_user != "Overall":
		df = df[df['user'] == selected_user]

	# fetch number of messages
	num_messages = df.shape[0]

	# fetch number of words
	words = []
	for message in df['only_message']:
		words.extend(message.split())


	# fetch number of media
	num_media_messages = 0
	for i in df['only_message']:
		if "<Media omitted>\n" in i:
			num_media_messages += 1

	# fetch number of link
	num_url_messages = 0
	for i in df['only_message']:
		if "https" in i:
			num_url_messages += 1

	return num_messages,len(words),num_media_messages,num_url_messages

def most_busy_user(df):
	x = df['user'].value_counts().head(10)
	return x

def create_wordcloud(selected_user,df):
	if selected_user != "Overall":
		df = df[df['user'] == selected_user]
	wc = WordCloud(width = 500,height = 500, min_font_size = 10,background_color="black")
	df = df[df['only_message'] != '<Media omitted>\n']
	df_wc = wc.generate(df['only_message'].str.cat(sep=" "))
	return df_wc

def most_common_words(selected_user,df):
	if selected_user != "Overall":
		df = df[df['user'] == selected_user]
	df = df[df['user'] != 'group_notification']
	df = df[df['only_message'] != '<Media omitted>\n']
	words = []
	for message in df['only_message']:
		for i in message.split():
			if i not in stop_word:
				words.append(i.lower())

	temp = Counter(words).most_common(10)
	x = []
	y = []
	for i in temp:
		x.append(i[0])
		y.append(i[1])
	return x,y


def most_common_emojis(selected_user,df):
	if selected_user != "Overall":
		df = df[df['user'] == selected_user]
	emojis = []
	for message in df['only_message']:
		emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
	temp = Counter(emojis).most_common(10)
	x = []
	y = []
	for i in temp:
		x.append(i[0])
		y.append(i[1])
	return x,y

def timeline(selected_user,df):
	if selected_user != "Overall":
		df = df[df['user'] == selected_user]
	timeline = df.groupby(['year','month_num','month']).count()['only_message'].reset_index()
	timeline['time'] = timeline["month"]+ "-" + timeline["year"].map(str)
	return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['only_message'].reset_index()
    return daily_timeline

def week_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    week_timeline = df['day_name'].value_counts()
    return week_timeline


def month_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    month_timeline = df['month'].value_counts()
    return month_timeline


def activity_time(selected_user,df):
	if selected_user != 'Overall':
		df = df[df['user'] == selected_user]
	f = df['period'].value_counts()
	f = dict(f)
	temp = sorted(f.keys(),key = lambda x:int(x[:x.index('-')]))
	final = {}
	for i in temp:
		final[i] = f[i]
	return final
	