import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import emoji
from textblob import TextBlob
import chat
import helper

# Page config
st.set_page_config(page_title="Chat Analyzer", page_icon="💬", layout="wide")

st.title("💬 WhatsApp Chat Analyzer")
st.write("UPDATED VERSION 🚀")

# Sidebar
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    data = uploaded_file.read().decode("utf-8")
    df = chat.chat(data)

    # Users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    option = st.sidebar.selectbox("Menu", ["Analysis", "Fun Insights", "Summary"])

    # ---------------- ANALYSIS ----------------
    if option == "Analysis":
        if st.sidebar.button("Show Analysis"):

            # ----------- CHAT TABLE-----------
            st.subheader("📋 Chat Data Table")

            # create date & time from datetime
            df['date'] = df['date_time'].dt.date
            df['time'] = df['date_time'].dt.time

            search = st.text_input("🔍 Search message")
            limit = st.slider("Select number of messages", 10, 500, 100)

            if search:
                filtered_df = df[df['message'].str.contains(search, case=False, na=False)]
            else:
                filtered_df = df

            st.dataframe(filtered_df[['date', 'time', 'user', 'message']].head(limit))
            # ----------- STATS -----------
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Messages", num_messages)
            col2.metric("Words", words)
            col3.metric("Media", num_media_messages)
            col4.metric("Links", num_links)

            # ----------- TIMELINE -----------
            st.subheader("📈 Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # ----------- HEATMAP -----------
            st.subheader("🔥 Activity Heatmap")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap)
            st.pyplot(fig)

            # ----------- WORDCLOUD -----------
            st.subheader("☁️ Wordcloud")
            df_wc = helper.create_wordcloud(selected_user, df)

            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)

            # ----------- MOST COMMON WORDS -----------
            st.subheader("📊 Most Common Words")
            most_common_df = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            ax.set_xlabel("Frequency")
            st.pyplot(fig)

            # ----------- EMOJI ANALYSIS -----------
            st.subheader("😂 Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)

            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)

            with col2:
                fig, ax = plt.subplots()
                ax.pie(
                    emoji_df[1].head(),
                    labels=emoji_df[0].head(),
                    autopct="%0.2f"
                )
                st.pyplot(fig)

    # ---------------- FUN INSIGHTS ----------------
    elif option == "Fun Insights":
        st.header("😂 Fun Insights")

        avg_length = df.groupby('user')['message'].apply(lambda x: x.str.len().mean())
        st.write("😐 Dry texter:", avg_length.idxmin())

        emoji_count = sum([1 for msg in df['message'] for c in str(msg) if c in emoji.EMOJI_DATA])
        st.write("😂 Total Emojis:", emoji_count)

        score = min(100, len(df) // 10)
        st.write(f"💙 Friendship Score: {score}/100")

    # ---------------- SUMMARY ----------------
    elif option == "Summary":
        st.header("🤖 Chat Summary")

        if st.button("Generate AI Summary"):

            sentiments = df['message'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
            avg_sentiment = sentiments.mean()

            if avg_sentiment > 0:
                mood = "positive 😊"
            elif avg_sentiment < 0:
                mood = "negative 😐"
            else:
                mood = "neutral 😶"

            most_active = df['user'].value_counts().idxmax()

            st.write(
                f"This chat contains {len(df)} messages. "
                f"The most active user is {most_active}. "
                f"The overall mood is {mood}."
            )





