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