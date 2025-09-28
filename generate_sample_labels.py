import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_minimal_training_data():
    """Create minimal training data for model initialization"""
    os.makedirs("data/labeled", exist_ok=True)
    
    # Minimal realistic training examples
    training_data = [
        # Positive examples
        {"title": "Stock market reaches new highs on strong earnings", "label": "Positive"},
        {"title": "New medical breakthrough shows promising results", "label": "Positive"}, 
        {"title": "Technology innovation creates job opportunities", "label": "Positive"},
        {"title": "Community comes together to help local families", "label": "Positive"},
        {"title": "Research shows progress in renewable energy", "label": "Positive"},
        {"title": "Economic growth continues for third quarter", "label": "Positive"},
        {"title": "Education program shows improved student outcomes", "label": "Positive"},
        {"title": "Healthcare initiative expands access to care", "label": "Positive"},
        {"title": "Infrastructure investment supports local development", "label": "Positive"},
        {"title": "Environmental protection efforts show results", "label": "Positive"},
        
        # Negative examples  
        {"title": "Data breach exposes customer information", "label": "Negative"},
        {"title": "Company announces significant layoffs", "label": "Negative"},
        {"title": "Natural disaster causes widespread damage", "label": "Negative"},
        {"title": "Economic uncertainty affects market confidence", "label": "Negative"},
        {"title": "Cyber attack disrupts essential services", "label": "Negative"},
        {"title": "Healthcare costs continue rising rapidly", "label": "Negative"},
        {"title": "Supply chain issues impact consumers", "label": "Negative"},
        {"title": "Climate change effects worsen conditions", "label": "Negative"},
        {"title": "Infrastructure failure creates safety concerns", "label": "Negative"},
        {"title": "Budget cuts reduce public services", "label": "Negative"}
    ]
    
    df = pd.DataFrame(training_data)
    
    # Save to CSV
    out_path = "data/labeled/headlines_labeled.csv"
    df.to_csv(out_path, index=False)
    
    # Print statistics
    label_counts = df['label'].value_counts()
    logger.info(f"✅ Training dataset created with {len(df)} samples:")
    logger.info(f"   - Positive: {label_counts.get('Positive', 0)}")
    logger.info(f"   - Negative: {label_counts.get('Negative', 0)}")
    logger.info(f"   - Saved to: {out_path}")
    
    return df

def main():
    """Main function to generate training data"""
    try:
        create_minimal_training_data()
        logger.info("✅ Training dataset created successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to create dataset: {e}")
        raise

if __name__ == "__main__":
    main()
