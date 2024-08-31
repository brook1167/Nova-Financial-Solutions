# Nova-Financial-Solutions-Data-Analysis

## Business Objective

Nova Financial Solutions aims to enhance its predictive analytics capabilities to significantly boost its financial forecasting accuracy and operational efficiency through advanced data analysis. In this project, the primary task is to conduct a rigorous analysis of the financial news dataset. The focus of the analysis is two-fold:

### Sentiment Analysis:

Perform sentiment analysis on the ‘headline’ text to quantify the tone and sentiment expressed in financial news. This will involve using natural language processing (NLP) techniques to derive sentiment scores, which can be associated with the respective 'Stock Symbol' to understand the emotional context surrounding stock-related news.

### Correlation Analysis:

Establish statistical correlations between the sentiment derived from news articles and the corresponding stock price movements. This involves tracking stock price changes around the date the article was published and analyzing the impact of news sentiment on stock performance. This analysis considers the publication date and potentially the time the article was published if such data can be inferred or is available.

The recommendations leverage insights from this sentiment analysis to suggest investment strategies. These strategies utilize the relationship between news sentiment and stock price fluctuations to predict future movements. The final report provide clear, actionable insights based on the analysis, offering innovative strategies to use news sentiment as a predictive tool for stock market trends.

## Dataset Overview

Financial News and Stock Price Integration Dataset FNSPID (Financial News and Stock Price Integration Dataset), is a comprehensive financial dataset designed to enhance stock market predictions by combining quantitative and qualitative data.

The structure of the data is as follows

#### headline

Article release headline, the title of the news article, which often
includes key financial actions like stocks hitting highs, price target changes, or
company earnings.

#### url

The direct link to the full news article.


#### publisher

Author/creator of article.


#### date

The publication date and time, including timezone information(UTC-4
timezone).

#### stock

Stock ticker symbol (unique series of letters assigned to a publicly traded
company). For example (AAPL: Apple)



## Getting Started

Follow the instructions below to set up and run the project on your local machine.

        Prerequisites
        Ensure you have the following installed on your system:
        
        Python 3.x
        pip
        virtualenv
        

    1. Clone the repository

        Clone the project repository to your local machine using the following command:
    
        git clone https://github.com/brook1167/Nova-Financial-Solutions

    2. Install dependencies
    
       Navigate to the project directory and create a virtual environment using virtualenv:
    
       cd Nova-Financial-Solutions
       
       virtualenv venv

    
    3. Activate the virtual environment
        
        on Windows
            .\venv\Scripts\activate
            
        on Mac/Linus
            source venv/bin/activate
            
    4. Install dependencies
    
        With the virtual environment activated, install all the required packages from the         requirements.txt file:
        
        pip install -r requirements.txt
    
    
    5. Run the application
    
    After installing the dependencies, you are all set! Run the application or script as       needed.
    
    
    
