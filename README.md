# News Sentiment Analysis 📰

**Real-time news sentiment analysis with machine learning and interactive dashboard**

🔗 **Live Demo**: [View Dashboard](https://your-app-name.streamlit.app)

## ✨ Features
- 📰 **Real-time News**: Fetches from NewsAPI and RSS feeds
- 🤖 **ML Analysis**: PySpark-powered sentiment classification  
- 📊 **Live Dashboard**: Interactive charts and real-time updates
- 🌐 **Cloud Deployed**: Available 24/7 on Streamlit Cloud

## 🚀 Quick Start

### Local Development
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

### API Setup
Get free NewsAPI key: https://newsapi.org/

**For local:** Add to `.env` file:
```
NEWS_API_KEY=your_api_key_here
```

**For deployment:** Add to Streamlit secrets in your app dashboard

## 📁 Project Structure
- `dashboard.py` - Main Streamlit app
- `fetch_news.py` - News fetching with multiple sources
- `train_model.py` - ML model training
- `predict.py` - Sentiment prediction engine

## 🔧 How It Works
1. **Fetch** - Gets latest news from APIs/RSS
2. **Analyze** - Runs sentiment analysis with trained model
3. **Visualize** - Shows results in real-time dashboard

## 📊 Dashboard Features
- Real-time sentiment metrics and gauges
- Interactive charts and word clouds
- Source breakdown and trend analysis
- Auto-refresh every 30 seconds