import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import preprocessor,helper

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    #fetch user name
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis w.r.t", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_messages,num_words,num_media_msg,num_links= helper.fetch_stats(selected_user,df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Total Media")
            st.title(num_media_msg)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #Monthly Timeline
        st.title("Monthly Timeline")
        monthly_timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(monthly_timeline['time'],monthly_timeline['count'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots(figsize=(28,10))
        ax.plot(daily_timeline['just_date'],daily_timeline['count'], color='yellow')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Weekly activity map")
            weekly_activity = helper.weekly_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(weekly_activity.index,weekly_activity.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Monthly activity map")
            monthly_activity = helper.monthly_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(monthly_activity.index,monthly_activity.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Activity Heatmap
        st.title("Activity Heatmap")
        activity_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()

        ax = sns.heatmap(activity_heatmap)
        st.pyplot(fig)

        #most busy users
        if(selected_user=='Overall'):
            st.title("Most Busy Users")
            x,busy_df = helper.most_busy_users(df)
            names = x.index
            counts = x.values
            fig,ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(names,counts,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(busy_df)

        #WordCloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #top 20 most used words
        st.title("Most Common words")
        most_common_words_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_words_df[0],most_common_words_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emoji analysis
        st.title("Emoji's Analysis")
        col1, col2 = st.columns(2)
        emoji_df = helper.most_common_emoji(df)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%1.1f%%")
            st.pyplot(fig)
            
    
