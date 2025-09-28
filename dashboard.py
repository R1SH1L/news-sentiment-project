import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime, timedelta
import time
import subprocess
import sys

# Page configuration
st.set_page_config(
    page_title="Real-Time News Sentiment Analysis",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .positive-sentiment {
        color: #2ca02c;
        font-weight: bold;
    }
    .negative-sentiment {
        color: #d62728;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def load_latest_predictions():
    """Load the latest predictions data"""
    pred_file = "data/predictions/latest.csv"
    stats_file = "data/predictions/latest_stats.json"
    
    predictions_df = None
    stats = None
    
    if os.path.exists(pred_file):
        try:
            predictions_df = pd.read_csv(pred_file)
        except Exception as e:
            st.error(f"Error loading predictions: {e}")
    
    if os.path.exists(stats_file):
        try:
            with open(stats_file, 'r') as f:
                stats = json.load(f)
        except Exception as e:
            st.error(f"Error loading stats: {e}")
    
    return predictions_df, stats

def create_sentiment_gauge(positive_pct):
    """Create a gauge chart for sentiment"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = positive_pct,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Positive Sentiment %"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 100], 'color': "lightgreen"}
            ]
        }
    ))
    fig.update_layout(height=300)
    return fig

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">📰 News Sentiment Analysis</h1>', unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.header("Dashboard Controls")
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        with st.sidebar:
            with st.spinner("Refreshing data..."):
                try:
                    # Run fetch and predict
                    subprocess.run([sys.executable, "fetch_news.py"], timeout=30, check=False)
                    subprocess.run([sys.executable, "predict.py"], timeout=30, check=False)
                    st.success("✅ Data refreshed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Refresh failed: {str(e)}")
    
    # API status
    news_api_key = os.getenv('NEWS_API_KEY', '')
    if news_api_key:
        st.sidebar.success("🌐 NewsAPI: Connected")
    else:
        st.sidebar.warning("⚠️ NewsAPI: Not configured")
    
    # Load data
    predictions_df, stats = load_latest_predictions()
    
    if predictions_df is None or predictions_df.empty:
        st.warning("⚠️ No predictions available yet.")
        
        if st.button("🚀 Initialize App"):
            with st.spinner("Setting up the app..."):
                try:
                    subprocess.run([sys.executable, "generate_sample_labels.py"], check=True)
                    subprocess.run([sys.executable, "train_model.py"], check=True)
                    st.success("✅ App initialized! Now use 'Refresh Data' to get news.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Setup failed: {e}")
        
        st.info("""
        **This app needs:**
        1. Training data for the ML model
        2. News headlines from APIs or RSS feeds  
        3. Sentiment predictions
        
        Click 'Initialize App' above, then use 'Refresh Data' in the sidebar.
        """)
        return
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Headlines", len(predictions_df))
    
    with col2:
        positive_count = len(predictions_df[predictions_df['sentiment'] == 'Positive'])
        st.metric("Positive", positive_count)
    
    with col3:
        negative_count = len(predictions_df[predictions_df['sentiment'] == 'Negative'])
        st.metric("Negative", negative_count)
    
    with col4:
        if stats:
            last_update = datetime.strptime(stats['timestamp'], '%Y%m%d_%H%M%S')
            st.metric("Last Update", last_update.strftime('%H:%M'))
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        if stats:
            gauge_fig = create_sentiment_gauge(stats['positive_percentage'])
            st.plotly_chart(gauge_fig, use_container_width=True)
    
    with col2:
        # Pie chart
        sentiment_counts = predictions_df['sentiment'].value_counts()
        fig_pie = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Sentiment Distribution",
            color_discrete_map={'Positive': '#2ca02c', 'Negative': '#d62728'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Recent headlines table
    st.subheader("📋 Recent Headlines")
    
    # Display table with colors
    for i, row in predictions_df.head(10).iterrows():
        sentiment_color = "🟢" if row['sentiment'] == 'Positive' else "🔴"
        st.write(f"{sentiment_color} {row['title']}")
    
    # Download section
    st.subheader("📥 Export Data")
    csv_data = predictions_df.to_csv(index=False)
    st.download_button(
        label="Download Predictions CSV",
        data=csv_data,
        file_name=f"news_sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()