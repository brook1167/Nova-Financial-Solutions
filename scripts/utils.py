import pandas as pd
import matplotlib.pyplot as plt



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