import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
from PIL import Image
from dateutil import parser
import numpy as np
from datetime import datetime
from wordcloud import WordCloud
from collections import Counter
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.dates as mdates


# Load DataFrames, ignoring the index column if it's present
@st.cache
def load_data():
    try:
        hotel_info = pd.read_csv('hotel_profiles.csv')  # Adjust index_col as needed
        data_final = pd.read_csv('data_final.csv')
        return hotel_info, data_final
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

hotel_info, data_final = load_data()

# Sort hotel_info DataFrame by 'num' column in ascending order
hotel_info_sorted = hotel_info.sort_values(by='num')

# Function to print hotel information
def print_hotel_info(hotel_id):
    info = hotel_info_sorted[hotel_info_sorted['Hotel ID'] == hotel_id]
    if not info.empty:
        hotel_name = info['Hotel Name'].values[0]
        hotel_address = info['Hotel Address'].values[0]
        hotel_rank = info['Hotel Rank'].values[0]
        st.write(f"**Hotel Name:** {hotel_name}")
        st.write(f"**Hotel Address:** {hotel_address}")
        st.write(f"**Hotel Rank:** {hotel_rank}")
    else:
        st.write(f"No hotel found with ID '{hotel_id}'")

vietnamese_df = pd.read_csv('backup_vn.csv')

# Sidebar for navigation
with st.sidebar:
    selected = st.selectbox(
        "Select Page",
        ["Business Understanding", "Data Understanding & Data Preparation", "Customer Feedback Classification", "Modeling & Evaluations", "Statistics Providing Insight"]
    )


# Page content based on selection
if selected == "Business Understanding":
    st.title("Sentiment Analysis Dashboard")
    st.header("Business Understanding")
    st.write("""
    This application provides insights from sentiment analysis conducted on customer feedback. 
    The goal is to understand customer sentiments to enhance overall satisfaction and improve services.
    By analyzing customer feedback, we aim to identify key areas for improvement and drive business growth.
    """)
    # Display an image
    st.image("Business Understanding.png", caption="Business Understanding", use_column_width=True)


elif selected == "Data Understanding & Data Preparation":
    st.header("Data Understanding & Data Preparation")
    # Data Understanding
    st.write("""
    ### Data understanding: 
    - Bộ dữ liệu thu thập được gồm 80314 dòng
    """)
    # Insert an image
    st.image("Data_Understanding.png", caption="Data Understanding", use_column_width=True)
    # Data Preparation
    st.write("""
    ### Data preparation:
    #### - Xử lý dữ liệu trùng
    #### - Nhận diện ngôn ngữ: Dịch các ngôn ngữ khác sang tiếng Việt
    #### - Chuẩn hoá dữ liệu Tiếng Việt
    #### - Bộ dữ liệu sẵn sàng sử dụng gồm 23236 dòng
    """)
    # Display head and tail of the DataFrame
    st.write("### Data Sample")
    # Display head
    st.write("**Head of the DataFrame:**")
    st.write(vietnamese_df.head())
    # Display tail
    st.write("**Tail of the DataFrame:**")
    st.write(vietnamese_df.tail())


elif selected == "Customer Feedback Classification":
    st.header("Phân loại phản hồi của khách hàng")
    st.write("### Sentiment Analysis Results")
    st.write("Placeholder for sentiment analysis results")
    st.write("### Word Clouds")
    st.write("Placeholder for word clouds")

# Modeling & Evaluations Page
elif selected == "Modeling & Evaluations":
    st.header("Modeling & Evaluations")

    # Load the pre-trained model and vectorizer
    st.write("Loading the pre-trained logistic regression model and vectorizer...")
    model = joblib.load('logistic_regression_model.pkl')
    vectorizer = joblib.load('count_vectorizer.pkl')

    # Load your test data
    st.write("Loading the test data...")
    test_data = pd.read_csv('test_data.csv')

    # Handle NaN values by filling them with an empty string
    st.write("Cleaning the test data...")
    test_data['Review_new'].fillna('', inplace=True)
    
    # Prepare test data for prediction
    X_test = test_data['Review_new']
    y_test = test_data['Sentiment']
    
    # Transform test data
    st.write("Transforming the test data using the loaded vectorizer...")
    test_X = vectorizer.transform(X_test).toarray()
    
    # Predict on test data
    st.write("Predicting on the test data...")
    preds = model.predict(test_X)

    # Accuracy Score
    accuracy = accuracy_score(y_test, preds)
    st.subheader("Accuracy Score")
    st.write(f"Accuracy Score: {accuracy:.4f}")
    
    # Classification Report
    st.subheader("Classification Report")
    report = classification_report(y_test, preds, digits=4)
    st.text(report)
    
    # Confusion Matrix
    st.subheader("Confusion Matrix")
    cm = confusion_matrix(y_test, preds)
    
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.set_title('Confusion Matrix')
    st.pyplot(fig)

    # Model Summary
    st.write("""
        The logistic regression model and vectorizer were trained and saved in a different environment. 
        This section loads the model and vectorizer, transforms the test data accordingly, and evaluates the model's performance. 
        The classification report and confusion matrix provide insights into the model's effectiveness.
    """)

####### Ending Modeling and Evaluations

elif selected == "Statistics Providing Insight":
    st.header("Thống kê cung cấp insight")
    # Display Top 10 Hotels
    st.subheader("Top 10 Hotels")
    top_hotels = hotel_info_sorted.head(10)
    st.write(top_hotels[['num', 'Hotel ID', 'Hotel Name', 'Hotel Rank', 'Hotel Address', 'Total Score']])
    # User input for Hotel ID
    # Header 1
    st.subheader("I. TỔNG QUAN: ")
    hotel_id = st.text_input("Enter Hotel ID:")
    if hotel_id:
        print_hotel_info(hotel_id)
        # Filter data_final for the selected hotel_id
        hotel_data = data_final[data_final['Hotel ID'] == hotel_id]
        # Head 2
        st.write("##### Sample Reviews")
        st.write(hotel_data[['Title', 'Body', 'Sentiment']].head())
        # Display some basic statistics or information about the filtered data
        if not hotel_data.empty:
            # Total number of reviews
            total_reviews = hotel_data['Sentiment'].count()
            # Head 2
            st.write(f"##### 1. Tổng số đánh giá của khách sạn là: {total_reviews}")
            # Sentiment counts
            sentiment_counts = hotel_data['Sentiment'].value_counts()
            # Head 2
            st.write("##### 2. Phân loại đánh giá của khách hàng:")
            # Create a table for sentiment counts
            st.write(sentiment_counts.to_frame().reset_index().rename(columns={'index': 'Sentiment', 'Sentiment': 'Count'}))
            # Draw a bar chart with different colors for each sentiment
            # Head 2
            st.write("##### 3. Sentiment Distribution")
            st.bar_chart(sentiment_counts, use_container_width=True)
            # New Section: Score Distribution
            st.write("##### Thông tin về điểm số đánh giá")
            # Calculate and display median score
            median_score = hotel_data['Score'].mean()
            st.write(f"**Median Score:** {median_score}")
            # Plot Score Distribution
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.histplot(hotel_data['Score'], bins=10, kde=True, color='skyblue', ax=ax)
            ax.set_title(f'Score Distribution for Hotel {hotel_id}')
            ax.set_xlabel('Score')
            ax.set_ylabel('Frequency')
            # Save the plot to a BytesIO object and display it with Streamlit
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img = Image.open(buf)
            st.image(img)
        else:
            st.write(f"No review data found for Hotel ID '{hotel_id}'")

    def extract_nights(stay_details):
        # Look for patterns like "X đêm"
        words = stay_details.split()
        for i, word in enumerate(words):
            if word.isdigit() and i < len(words) - 1 and words[i + 1] == 'đêm':
                return int(word)
        return None
    def extract_month_year(stay_details):
        # Look for patterns like "Tháng X năm YYYY"
        try:
            date = parser.parse(stay_details, fuzzy=True)
            return date.strftime('%B %Y')
        except:
            return None
    hotel_data['Nights Stayed'] = hotel_data['Stay Details'].apply(extract_nights)
    hotel_data['Month Year'] = hotel_data['Stay Details'].apply(extract_month_year)
    def convert_to_datetime(month_year_str):
        try:
            return datetime.strptime(month_year_str, '%B %Y')
        except ValueError:
            return None
    hotel_data['Date'] = hotel_data['Month Year'].apply(convert_to_datetime)
    # Additional Insights
    st.write("##### Tổng quan thời gian lưu trú:")
    st.write("- Số đêm lưu trú: 'Nights Stayed'")
    st.write("- Lượng khách lưu trú tăng/giảm giữa các tháng trong năm và qua các năm : 'Distribution of Stays by Month and Year'")
    # Distribution of Nights Stayed
    st.write("###### Số đêm lưu trú: 'Nights Stayed'")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(hotel_data['Nights Stayed'].dropna(), bins=10, kde=True, color='skyblue', ax=ax)
    ax.set_title('Distribution of Nights Stayed')
    ax.set_xlabel('Number of Nights')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
    # Distribution of Stays by Month and Year
    st.write("###### Lượng khách lưu trú tăng/giảm giữa các tháng trong năm và qua các năm : 'Distribution of Stays by Month and Year'")
    hotel_data.sort_values(by='Date', inplace=True)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.countplot(x='Date', data=hotel_data, palette='viridis', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_title('Distribution of Stays by Month and Year')
    ax.set_xlabel('Month and Year')
    ax.set_ylabel('Count')
    plt.tight_layout()
    st.pyplot(fig)

    # Head 2
    st.write("##### Đánh giá theo các mùa trong năm: Sentiment Distribution Throughout the Year")
    # Extract month and year from the 'Date' column
    hotel_data['Month'] = hotel_data['Date'].dt.to_period('M')
    hotel_data['Month'] = hotel_data['Month'].astype(str)  # Convert to string for easier plotting
    # Group by 'Month' and 'Sentiment', and count occurrences
    monthly_sentiment_counts = hotel_data.groupby(['Month', 'Sentiment']).size().reset_index(name='Count')
    # Plot
    plt.figure(figsize=(14, 8))
    # Create a line plot to show sentiment distribution throughout the year
    sns.lineplot(data=monthly_sentiment_counts, x='Month', y='Count', hue='Sentiment', marker='o')
    # Customize plot
    plt.title('Sentiment Distribution Throughout the Year')
    plt.xlabel('Month')
    plt.ylabel('Number of Reviews')
    plt.xticks(rotation=45)
    plt.legend(title='Sentiment')
    plt.tight_layout()
    # Show plot
    st.pyplot(plt)

    # Head 2: Score Distribution Through Month-Year by boxplot
    st.write("##### Xu hướng điểm số theo thời gian: Score Distribution Through Month-Year by boxplot")
    # Add a 'Month Year' column for better granularity
    hotel_data['Month Year'] = hotel_data['Date'].dt.to_period('M')
    # Create a box plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Month Year', y='Score', palette='Set2', data=hotel_data)
    plt.xticks(rotation=45)
    plt.title('Score Distribution Through Month-Year by boxplot')
    plt.xlabel('Month-Year')
    plt.ylabel('Score')
    plt.grid(True)
    st.pyplot(plt)

    # Head 2: Wordcloud for Customer Feedback
    st.write("#### Wordcloud phản hồi của khách hàng:")
    st.write("##### Phản hồi tích cực")
    positive_reviews = hotel_data.loc[hotel_data['Sentiment'] == 'Tích cực', 'Review_new'].values
    negative_reviews = hotel_data.loc[hotel_data['Sentiment'] == 'Tiêu cực', 'Review_new'].values
    def generate_wordcloud(reviews, title):
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=50).generate(' '.join(reviews))
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(title, fontsize=14)
        plt.axis('off')
        st.pyplot(plt)
    def calculate_word_statistics(wordcloud_text):
        words = ' '.join(wordcloud_text).split()
        word_frequency = Counter(words)
        total_words = len(words)
        unique_words = len(word_frequency)
        most_common_words = word_frequency.most_common(10)
        return word_frequency, total_words, unique_words, most_common_words
    # Show positive reviews word cloud
    generate_wordcloud(positive_reviews, 'Word Cloud for Positive Reviews')
    # Show negative word statistics
    st.write("###### Top 10 Most Common POSITIVE  Words'")
    positive_word_frequency, positive_total_words, positive_unique_words, positive_most_common = calculate_word_statistics(positive_reviews)
    df_positive_most_common = pd.DataFrame(positive_most_common, columns=['Word', 'Count'])
    st.write(df_positive_most_common)
    # Filter negative reviews to exclude positive words
    positive_reviews_set = set(' '.join(positive_reviews).split())
    def filter_words(review):
        return ' '.join([word for word in review.split() if word not in positive_reviews_set])
    negative_reviews_filtered = list(map(filter_words, negative_reviews))
    # Show negative reviews word cloud
    st.write("##### Phản hồi 'Tiêu cực'")
    generate_wordcloud(negative_reviews_filtered, 'Word Cloud for Negative Reviews')
    # Show negative word statistics
    st.write("###### Top 10 Most Common NEGATIVE Words'")
    negative_word_frequency, negative_total_words, negative_unique_words, negative_most_common = calculate_word_statistics(negative_reviews_filtered)
    df_negative_most_common = pd.DataFrame(negative_most_common, columns=['Word', 'Count'])
    st.write(df_negative_most_common)

######
    # Header 1: Nationality Analysis
    st.subheader("II. PHÂN TÍCH QUỐC TỊCH")

    # Head 2: Nationality Distribution
    st.write("##### Phân bổ quốc tịch của du khách")
    nationality_counts = hotel_data['Nationality'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    nationality_counts.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title(f'Nationality Distribution for Hotel {hotel_id}')
    ax.set_xlabel('Nationality')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # Head 2: Median Scores by Nationality
    st.write("##### Điểm số đánh giá trung bình theo quốc tịch")
    median_scores_by_nationality = hotel_data.groupby('Nationality')['Score'].median().reset_index()
    median_scores_by_nationality = median_scores_by_nationality.sort_values(by='Score', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Nationality', y='Score', data=median_scores_by_nationality, palette='viridis', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_xlabel('Nationality')
    ax.set_ylabel('Median Score')
    ax.set_title('Median Scores by Nationality')
    plt.tight_layout()
    st.pyplot(fig)

    # Head 2: Summary Statistics
    st.write("##### Bảng tổng hợp thống kê")
    summary_stats = hotel_data.groupby('Nationality').agg({
        'Nights Stayed': ['median'],
        'Sentiment': lambda x: x.value_counts().to_dict()
    }).reset_index()
    st.write(summary_stats)


######
    # Header 1:
    st.subheader("III. PHÂN TÍCH LOẠI PHÒNG")

    # Create a mapping dictionary
    room_types = hotel_data['Room Type'].unique()
    mapping_dict = {room_type: f'Type {i+1}' for i, room_type in enumerate(room_types)}
    # Replace Room Type with generic labels
    hotel_data['Room Type_new'] = hotel_data['Room Type'].map(mapping_dict)

    # Head 2: with #####
    st.write("##### Danh sách các loại phòng")
    unique_room_types = hotel_data[['Room Type', 'Room Type_new']].drop_duplicates().sort_values(by='Room Type_new')
    st.write(unique_room_types)

    # Head 2: with #####
    st.write("##### Phân bổ loại phòng được sử dụng giữa các tháng trong năm và qua các năm: Room Type Distribution Throughout the Year")
    # Extract month and year from the 'Date' column
    hotel_data['Month'] = hotel_data['Date'].dt.to_period('M')
    # Aggregate data
    monthly_room_type_counts = hotel_data.groupby(['Month', 'Room Type_new']).size().reset_index(name='Count')
    # Plot
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(data=monthly_room_type_counts, x='Month', y='Count', hue='Room Type_new', palette='tab20')
    # Adjust legend
    plt.legend(title='Room Type_new', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    # Set plot title and labels
    plt.title('Room Type Distribution Throughout the Year')
    plt.xlabel('Month')
    plt.ylabel('Number of Rooms')
    plt.xticks(rotation=45)
    # Adjust layout
    plt.tight_layout()
    st.pyplot(plt)

    # Head 2: with #####
    st.write("##### Phân bổ đánh giá của từng loại phòng theo thời gian: Sentiment Trends for Room Type")


    # Create a DataFrame that counts sentiments per date and room type
    sentiment_counts = hotel_data.groupby(['Date', 'Room Type', 'Sentiment']).size().reset_index(name='Count')

    # Pivot table to get the format suitable for plotting
    sentiment_pivot = sentiment_counts.pivot_table(index=['Date', 'Room Type'],
                                                columns='Sentiment',
                                                values='Count',
                                                fill_value=0).reset_index()

    # Melt the DataFrame for easier plotting
    sentiment_melted = sentiment_pivot.melt(id_vars=['Date', 'Room Type'],
                                            value_vars=['Tích cực', 'Tiêu cực', 'Trung tính'],
                                            var_name='Sentiment',
                                            value_name='Count')

    # Get unique room types
    room_types = sentiment_melted['Room Type'].unique()
    n_room_types = len(room_types)
    # Calculate number of rows needed for the plots
    n_cols = 3
    n_rows = (n_room_types + n_cols - 1) // n_cols  # Ceiling division to handle any remainder

    # Set up the plotting area
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(18, 4 * n_rows))

    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    # Define the start and end date for the x-axis limits
    start_date = pd.to_datetime('2022-01-01')
    end_date = sentiment_melted['Date'].max()

    # Plot data for each room type
    for ax, room_type in zip(axes, room_types):
        room_data = sentiment_melted[sentiment_melted['Room Type'] == room_type]
        sns.lineplot(data=room_data, x='Date', y='Count', hue='Sentiment', ax=ax, marker='o')
        ax.set_title(f'Sentiment Trends for Room Type: {room_type}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Count of Sentiments')
        ax.legend(title='Sentiment')

        # Set date format and locator
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Adjust interval as needed

        # Set x-axis limits
        ax.set_xlim(start_date, end_date)

        # Rotate and align x-axis labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Set x-axis labels for all subplots to ensure consistency
    for ax in axes:
        ax.set_xlabel('Date')

    # Hide any unused subplots
    for ax in axes[len(room_types):]:
        ax.axis('off')

    plt.tight_layout()
    st.pyplot(plt)

######
    # Header 1
    st.subheader("IV. PHÂN TÍCH NHÓM KHÁCH")

    # Head 2: with #####
    st.write("##### Phân bổ nhóm khách giữa các tháng và qua các năm: Group Name Distribution Throughout the Year")

    # Extract month and year from the 'Date' column
    hotel_data['Month'] = hotel_data['Date'].dt.to_period('M')

    # Aggregate data
    monthly_group_name_counts = hotel_data.groupby(['Month', 'Group Name']).size().reset_index(name='Count')

    # Plot
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(data=monthly_group_name_counts, x='Month', y='Count', hue='Group Name', palette='tab20')

    # Adjust legend
    plt.legend(title='Group Name', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # Set plot title and labels
    plt.title('Group Name Distribution Throughout the Year')
    plt.xlabel('Month')
    plt.ylabel('Number of Rooms')
    plt.xticks(rotation=45)

    # Adjust layout
    plt.tight_layout()
    st.pyplot(plt)

    # Head 2: with #####
    st.write("##### Phân bổ đánh giá theo từng nhóm khách theo thời gian: Sentiment Trends for Group")

    # Create a DataFrame that counts sentiments per date and group
    sentiment_counts = hotel_data.groupby(['Date', 'Group Name', 'Sentiment']).size().reset_index(name='Count')

    # Pivot table to get the format suitable for plotting
    sentiment_pivot = sentiment_counts.pivot_table(index=['Date', 'Group Name'],
                                                columns='Sentiment',
                                                values='Count',
                                                fill_value=0).reset_index()

    # Melt the DataFrame for easier plotting
    sentiment_melted = sentiment_pivot.melt(id_vars=['Date', 'Group Name'],
                                            value_vars=['Tích cực', 'Tiêu cực', 'Trung tính'],
                                            var_name='Sentiment',
                                            value_name='Count')

    # Get unique group names
    groups = sentiment_melted['Group Name'].unique()
    n_groups = len(groups)

    # Calculate number of rows needed for the plots
    n_cols = 3
    n_rows = (n_groups + n_cols - 1) // n_cols  # Ceiling division to handle any remainder

    # Set up the plotting area
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(18, 4 * n_rows))

    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    # Define the start and end date for the x-axis limits
    start_date = pd.to_datetime('2022-01-01')
    end_date = sentiment_melted['Date'].max()

    # Plot data for each group
    for ax, group in zip(axes, groups):
        group_data = sentiment_melted[sentiment_melted['Group Name'] == group]
        sns.lineplot(data=group_data, x='Date', y='Count', hue='Sentiment', ax=ax, marker='o')
        ax.set_title(f'Sentiment Trends for Group: {group}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Count of Sentiments')
        ax.legend(title='Sentiment')

        # Set date format and locator
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Adjust interval as needed

        # Set x-axis limits
        ax.set_xlim(start_date, end_date)

        # Rotate and align x-axis labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Hide any unused subplots
    for ax in axes[len(groups):]:
        ax.axis('off')

    plt.tight_layout()
    st.pyplot(plt)

##### Ending Visualization

