import streamlit as st
import preprocessing
import helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
	bytes_data = uploaded_file.getvalue()
	data = bytes_data.decode("utf-8")
	df = preprocessing.preprocess(data)
	# st.dataframe(df)
	user_list = df['user'].unique().tolist()
	user_list.remove('group_notification')
	user_list.sort()
	user_list.insert(0,"Overall")
	selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
	if st.sidebar.button("Show Analysis"):

		num_messages,words,num_media_messages,num_url_messages = helper.fetch_stats(selected_user, df)
		
		col1, col2, col3, col4 = st.columns(4)
		with col1:
			st.header("Total Messages")
			st.title(num_messages)
		with col2:
			st.header("Total Words")
			st.title(words)
		with col3:
			st.header("Media Shared")
			st.title(num_media_messages)
		with col4:
			st.header("Link Shared")
			st.title(num_url_messages)

		# timeline
		st.title("Monthly TimeLine")
		timeline_df = helper.timeline(selected_user, df)
		fig, ax = plt.subplots()
		ax.bar(timeline_df['time'],timeline_df['only_message'])
		plt.xticks(rotation='vertical')
		st.pyplot(fig)

		# daily timeline
		st.title("Daily TimeLine")
		daily_timeline_df = helper.daily_timeline(selected_user, df)
		fig, ax = plt.subplots()
		ax.plot(daily_timeline_df['only_date'],daily_timeline_df['only_message'])
		plt.xticks(rotation='vertical')
		st.pyplot(fig)

		# activity map 
		st.title("Activity Map")
		col5, col6 = st.columns(2)
		with col5:
			week_timeline_df = helper.week_timeline(selected_user, df)
			fig, ax = plt.subplots()
			ax.bar(week_timeline_df.index,week_timeline_df.values)
			plt.xticks(rotation='vertical')
			st.pyplot(fig)
		with col6:
			month_timeline_df = helper.month_timeline(selected_user, df)
			fig, ax = plt.subplots()
			ax.bar(month_timeline_df.index,month_timeline_df.values)
			plt.xticks(rotation='vertical')
			st.pyplot(fig)

		# activity time
		st.title("Activity with Time")
		time_df = helper.activity_time(selected_user, df)
		fig, ax = plt.subplots()
		ax.bar(time_df.keys(),time_df.values())
		plt.xticks(rotation='vertical')
		st.pyplot(fig)








		# finding the busiest user in group
		if selected_user == "Overall":
			st.title("Most Busy User")
			col7, col8 = st.columns(2)
			with col7:
				x = helper.most_busy_user(df)
				fig, ax = plt.subplots()
				ax.bar(x.index,x.values)
				plt.xticks(rotation='vertical')
				st.pyplot(fig)
			with col8:
				x = round((df['user'].value_counts()/df.shape[0])*100,2)
				y = x.values
				mylabels = x.index
				fig, ax = plt.subplots()
				ax.pie(y,labels=mylabels)
				st.pyplot(fig)
		
		# Wordcloud
		st.title("Word Cloud")
		df_wc = helper.create_wordcloud(selected_user, df)
		fig, ax = plt.subplots()
		ax.imshow(df_wc,interpolation="bilinear")
		plt.axis("off")
		st.pyplot(fig)

		# most common word
		st.title("Most Common Words")
		most_common_words_x,most_common_words_y = helper.most_common_words(selected_user, df) 
		fig, ax = plt.subplots()
		ax.pie(most_common_words_y,labels=most_common_words_x,autopct="%0.2f")
		st.pyplot(fig)

		# most common emoji
		st.title("Most Common Emoji")
		most_common_emojis_x,most_common_emojis_y = helper.most_common_emojis(selected_user, df) 
		fig, ax = plt.subplots()
		ax.pie(most_common_emojis_y,labels=most_common_emojis_x,autopct="%0.2f")
		st.pyplot(fig)




