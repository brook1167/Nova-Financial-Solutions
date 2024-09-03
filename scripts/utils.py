import pandas as pd
from pandas.tseries.offsets import MonthEnd
import matplotlib.pyplot as plt
import  matplotlib.dates as mdates
import  matplotlib.dates as mdates
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import talib as ta

def read_csv(file_path):
    return pd.read_csv(file_path)

def check_null_values(df):
    return df.isnull().values.any()

def headline_length(df):
    df['headline_length'] = df['headline'].apply(lambda x: len(x))
    headline_stats = df['headline_length'].describe()
    return headline_stats

def publishers_by_articles(df, top_n):
    print(f'Top {top_n} publishers by articles')
    article_counts = df.groupby('publisher').size()
    sorted_counts = article_counts.sort_values(ascending=False)
    return sorted_counts.head(top_n)

def plot_top_publishers(df, top_n):
    top_publishers = publishers_by_articles(df, top_n)
    plt.figure(figsize=(10, 6))
    top_publishers.plot(kind='bar', color='skyblue')
    plt.title(f'Top {top_n} Publishers by Number of Articles')
    plt.xlabel('Publishers')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def publication_dates(df):
    # Ensure 'date' is in datetime format
    df['date'] = pd.to_datetime(df['date'],format="ISO8601")

    # Group by date and count articles
    daily_counts = df.groupby(df['date'].dt.date).size()
    
    # Find days with highest article counts
    top_days = daily_counts.nlargest(5)
    
    # Analyze weekday distribution
    weekday_counts = df['date'].dt.day_name().value_counts()
    
    # Monthly trend
    df['month_start'] = df['date'].dt.floor('D') + MonthEnd(0) - MonthEnd(1)

    monthly_counts = df.groupby(df['date'].dt.to_period('M').dt.to_timestamp()).size()

    
    return {
        'daily_counts': daily_counts,
        'top_days': top_days,
        'weekday_counts': weekday_counts,
        'monthly_counts': monthly_counts
    }

#Plot the publication trends
def plot_publication_trends(date_analysis):

    fig, axes = plt.subplots(2, 2, figsize=(20, 15))
    
    # Daily trend
    date_analysis['daily_counts'].plot(ax=axes[0, 0])
    axes[0, 0].set_title('Daily Article Count')
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Number of Articles')
    
    # Top days
    date_analysis['top_days'].plot(kind='bar', ax=axes[0, 1])
    axes[0, 1].set_title('Top 5 Days with Most Articles')
    axes[0, 1].set_xlabel('Date')
    axes[0, 1].set_ylabel('Number of Articles')
    
    # Weekday distribution
    date_analysis['weekday_counts'].plot(kind='bar', ax=axes[1, 0])
    axes[1, 0].set_title('Article Distribution by Weekday')
    axes[1, 0].set_xlabel('Weekday')
    axes[1, 0].set_ylabel('Number of Articles')
    
    # Monthly trend
    monthly_counts = date_analysis['monthly_counts']
    monthly_counts.plot(ax=axes[1, 1])
    axes[1, 1].set_title('Monthly Article Count')
    axes[1, 1].set_xlabel('Month')
    axes[1, 1].set_ylabel('Number of Articles')
    
    # Format x-axis to show months
    axes[1, 1].xaxis.set_major_locator(mdates.AutoDateLocator())
    axes[1, 1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(axes[1, 1].xaxis.get_majorticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    return fig

Download necessary NLTK resources
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

# Perform sentiment analysis on the specified text column, defaulting to 'headline'
def perform_sentiment_analysis(df, column='headline'):
    sentiment_analyzer = SentimentIntensityAnalyzer()
    df['sentiment_scores'] = df[column].apply(lambda text: sentiment_analyzer.polarity_scores(text))
    df['sentiment'] = df['sentiment_scores'].apply(lambda scores: 'positive' if scores['compound'] > 0 else ('negative' if scores['compound'] < 0 else 'neutral'))
    return df

def perform_topic_modeling(df, column='headline', topics_count=5, words_count=10):

    # Tokenize and vectorize the text in the specified column
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    doc_term_matrix = vectorizer.fit_transform(df[column])

    # Apply Latent Dirichlet Allocation for topic modeling
    lda_model = LatentDirichletAllocation(n_components=topics_count, random_state=42)
    lda_model.fit(doc_term_matrix)
    
    feature_names = vectorizer.get_feature_names_out()
    extracted_topics = []
    for idx, topic in enumerate(lda_model.components_):
        top_words = [(feature_names[i], topic[i]) for i in topic.argsort()[:-words_count - 1:-1]]
        extracted_topics.append(top_words)
    
    return extracted_topics

# Time Series Analysis

# Examine how article publication times are distributed across different hours of the day
def publication_time_distribution(df):
    df['date'] = pd.to_datetime(df['date'],format="ISO8601")
    df['hour'] = df['date'].dt.hour
    hourly_distribution = df['hour'].value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    hourly_distribution.plot(kind='bar')
    plt.title('Hourly Distribution of Article Publications')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Articles Published')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    
    peak_hour = hourly_distribution.idxmax()
    return f"The highest publication activity occurs at {peak_hour}:00"


# Detect days with significantly higher publication activity
def detect_publication_anomalies(df, threshold=2):
    daily_counts = df.groupby(df['date'].dt.date).size()
    mean_publications = daily_counts.mean()
    std_publications = daily_counts.std()
    
    anomalies = daily_counts[daily_counts > mean_publications + threshold * std_publications]
    return anomalies

def analyze_publication_trends(df, date_column='date'):
    # Convert the date column to datetime
    df['publication_date'] = pd.to_datetime(df[date_column])
    
    # Extract day names for trend analysis
    df['publication_day'] = df['publication_date'].dt.day_name()
    publication_trends = df.groupby('publication_day').size()
    
    # Extract time for time series analysis
    df['publication_time'] = df['publication_date'].dt.time
    
    # Plot publication frequency over time
    df.set_index('publication_date').resample('D').size().plot()
    plt.title('Publication Frequency Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.show()
    
    return publication_trends

def plot_publication_frequency_by_day(df, date_column='date'):
    # Convert the 'date' column to datetime format
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Set the 'date' column as the index
    df.set_index(date_column, inplace=True)
    
    # Group by day of the week
    weekly_publications = df.groupby(df.index.dayofweek).size()
    
    # Set the labels for the x-axis
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Plot the bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(days_of_week, weekly_publications)
    plt.title('Publication Frequency by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Publications')
    plt.show()


def get_top_publisher_domains(df, publisher_column='publisher', top_n=10):
    def extract_domain(email):
        match = re.search(r"@[\w.]+", email)
        if match:
            return match.group()[1:]
        return email

    # Apply the extract_domain function to the specified publisher column
    df["publisher_domain"] = df[publisher_column].apply(extract_domain)

    # Count the occurrences of each publisher domain
    domain_counts = df["publisher_domain"].value_counts()

    # Return the top N publisher domains
    return domain_counts.head(top_n)


def plot_top_publisher_domains(df, publisher_column='publisher', top_n=10):
    def extract_domain(email):
        match = re.search(r"@[\w.]+", email)
        if match:
            return match.group()[1:]
        return email

    # Apply the extract_domain function to the specified publisher column
    df["publisher_domain"] = df[publisher_column].apply(extract_domain)

    # Count the occurrences of each publisher domain
    domain_counts = df["publisher_domain"].value_counts()

    # Get the top N publisher domains
    top_domains = domain_counts.head(top_n)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.bar(top_domains.index, top_domains.values)
    plt.xlabel("Publisher Domain")
    plt.ylabel("Count")
    plt.title(f"Top {top_n} Publisher Domains")
    plt.xticks(rotation=45, ha='right')
    plt.show()


def technical_indicators(df):
    df['SMA_50'] = ta.SMA(df['Close'], timeperiod=50)
    df['RSI'] = ta.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_Signal'], _ = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return df