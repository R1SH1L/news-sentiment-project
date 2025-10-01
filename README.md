# News Sentiment Analysis

A real-time news sentiment analysis application with machine learning and interactive dashboard.

## Features

- **Real-time News Fetching**: Gets latest news from NewsAPI and RSS feeds
- **Sentiment Analysis**: Uses PySpark machine learning for sentiment classification
- **Interactive Dashboard**: Built with Streamlit for data visualization
- **Automated Processing**: Continuous analysis and updates

## Installation

1. Clone the repository:
```bash
git clone https://github.com/R1SH1L/news-sentiment-project.git
cd news-sentiment-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up NewsAPI key:
   - Get a free API key from [NewsAPI](https://newsapi.org/)
   - Create a `.env` file and add: `NEWS_API_KEY=your_api_key_here`

## Usage

Run the Streamlit dashboard:
```bash
streamlit run dashboard.py
```

## Deployment to Streamlit Cloud

1. Fork/clone this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file as `dashboard.py`
5. **Important**: Add your NewsAPI key in Streamlit Cloud secrets:
   - Go to your app settings
   - Navigate to "Secrets" section
   - Add: `NEWS_API_KEY = "de914b01d6ce40eba49a4d7f7d21a121"`
6. Deploy and your app will be live!

> **Note**: The app will work with sample data if external news sources are unavailable due to network restrictions.

## Project Structure

- `dashboard.py` - Main Streamlit application
- `fetch_news.py` - News data fetching module
- `train_model.py` - Machine learning model training
- `predict_stream.py` - Real-time prediction engine
- `data/` - Data storage directory
- `models/` - Trained ML models

## How It Works

1. **Data Collection**: Fetches news articles from multiple sources
2. **Preprocessing**: Cleans and prepares text data
3. **Analysis**: Applies trained sentiment classification model
4. **Visualization**: Displays results in interactive dashboard

## Requirements

- Python 3.8+
- Streamlit
- PySpark
- Pandas
- Scikit-learn
- Requests