import pandas as pd
from pandas.tseries.offsets import MonthEnd
import matplotlib.pyplot as plt
import  matplotlib.dates as mdates
import  matplotlib.dates as mdates


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

    monthly_counts = df.groupby(pd.Grouper(key='date', freq='ME')).size()

    
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