#!/usr/bin/env python3
"""
Simple prediction script for news sentiment analysis
"""

import os
import pandas as pd
import logging
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def simple_predict():
    """Simple rule-based prediction for demo purposes"""
    # Read latest raw headlines
    raw_dir = "data/raw"
    if not os.path.exists(raw_dir) or not os.listdir(raw_dir):
        logger.error("❌ No raw headline CSVs found. Run fetch_news.py first.")
        return
    
    # Find latest CSV file
    csv_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
    if not csv_files:
        logger.error("❌ No CSV files found in raw directory")
        return
    
    latest_file = max([os.path.join(raw_dir, f) for f in csv_files], key=os.path.getctime)
    logger.info(f"📂 Processing: {latest_file}")
    
    # Read data
    df = pd.read_csv(latest_file)
    logger.info(f"Loaded {len(df)} headlines")
    
    # Simple rule-based sentiment analysis (for demo)
    positive_words = [
        'breakthrough', 'success', 'grow', 'increase', 'rise', 'up', 'high', 'good', 
        'great', 'excellent', 'positive', 'win', 'gains', 'boost', 'improve', 
        'celebrate', 'achievement', 'progress', 'recover', 'beneficial', 'hope',
        'innovation', 'advance', 'victory', 'milestone'
    ]
    
    negative_words = [
        'breach', 'attack', 'crisis', 'recession', 'down', 'fall', 'crash', 
        'decline', 'loss', 'negative', 'fail', 'problem', 'issue', 'concern', 
        'threat', 'risk', 'danger', 'disaster', 'emergency', 'violence',
        'unemployment', 'layoffs', 'corruption', 'fraud'
    ]
    
    # Predict sentiment
    predictions = []
    for _, row in df.iterrows():
        title = str(row['title']).lower()
        
        pos_count = sum(1 for word in positive_words if word in title)
        neg_count = sum(1 for word in negative_words if word in title)
        
        if pos_count > neg_count:
            sentiment = "Positive"
            prediction = 1.0
        elif neg_count > pos_count:
            sentiment = "Negative" 
            prediction = 0.0
        else:
            # Default to positive if neutral
            sentiment = "Positive"
            prediction = 1.0
        
        predictions.append({
            'title': row['title'],
            'sentiment': sentiment,
            'prediction': prediction,
            'processed_at': datetime.now().isoformat()
        })
    
    # Create predictions dataframe
    pred_df = pd.DataFrame(predictions)
    
    # Save predictions
    os.makedirs("data/predictions", exist_ok=True)
    
    # Save with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    pred_path = f"data/predictions/predictions_{timestamp}.csv"
    pred_df.to_csv(pred_path, index=False)
    
    # Save as latest for dashboard
    latest_path = "data/predictions/latest.csv"
    pred_df.to_csv(latest_path, index=False)
    
    # Create summary statistics
    total = len(pred_df)
    positive_count = len(pred_df[pred_df['sentiment'] == 'Positive'])
    negative_count = len(pred_df[pred_df['sentiment'] == 'Negative'])
    
    stats = {
        "timestamp": timestamp,
        "total_headlines": total,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "positive_percentage": (positive_count / total * 100) if total > 0 else 0,
        "negative_percentage": (negative_count / total * 100) if total > 0 else 0,
    }
    
    # Save stats
    stats_path = "data/predictions/latest_stats.json"
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    logger.info(f"✅ Processed {total} headlines:")
    logger.info(f"   - Positive: {positive_count} ({positive_count/total*100:.1f}%)")
    logger.info(f"   - Negative: {negative_count} ({negative_count/total*100:.1f}%)")
    logger.info(f"   - Saved to: {pred_path}")
    
    # Show sample predictions
    logger.info("\nSample predictions:")
    for i, row in pred_df.head(10).iterrows():
        sentiment_icon = "😊" if row['sentiment'] == 'Positive' else "😟"
        logger.info(f"   {sentiment_icon} {row['title'][:60]}... -> {row['sentiment']}")

if __name__ == "__main__":
    simple_predict()