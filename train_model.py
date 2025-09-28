import os
import logging
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import col, when

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_spark_session():
    """Create and configure Spark session"""
    return SparkSession.builder \
        .appName("NewsSentimentTraining") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

def load_and_validate_data(data_path):
    """Load and validate the training dataset"""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Labeled dataset not found at {data_path}")
    
    spark = SparkSession.getActiveSession()
    df = spark.read.csv(data_path, header=True, inferSchema=True)
    
    # Validate data
    logger.info(f"Loaded {df.count()} samples from {data_path}")
    
    # Check for required columns
    required_cols = ["title", "label"]
    for col_name in required_cols:
        if col_name not in df.columns:
            raise ValueError(f"Missing required column: {col_name}")
    
    # Remove null values
    df_clean = df.filter(col("title").isNotNull() & col("label").isNotNull())
    null_count = df.count() - df_clean.count()
    if null_count > 0:
        logger.warning(f"Removed {null_count} rows with null values")
    
    # Show data distribution
    logger.info("Label distribution:")
    df_clean.groupBy("label").count().show()
    
    return df_clean

def create_ml_pipeline():
    """Create the ML pipeline with feature engineering"""
    # Text preprocessing
    tokenizer = Tokenizer(inputCol="title", outputCol="words")
    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    
    # Feature extraction
    hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=10000)
    idf = IDF(inputCol="rawFeatures", outputCol="features", minDocFreq=2)
    
    # Label encoding
    label_indexer = StringIndexer(inputCol="label", outputCol="indexedLabel")
    
    # Classifier
    lr = LogisticRegression(
        featuresCol="features", 
        labelCol="indexedLabel",
        maxIter=100,
        regParam=0.01
    )
    
    return Pipeline(stages=[tokenizer, remover, hashingTF, idf, label_indexer, lr])

def train_and_evaluate_model(df):
    """Train the model and evaluate performance"""
    # Split data
    train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)
    
    logger.info(f"Training set: {train_data.count()} samples")
    logger.info(f"Test set: {test_data.count()} samples")
    
    # Create and train pipeline
    pipeline = create_ml_pipeline()
    model = pipeline.fit(train_data)
    
    # Make predictions on test set
    predictions = model.transform(test_data)
    
    # Evaluate model
    evaluator = BinaryClassificationEvaluator(
        labelCol="indexedLabel",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    
    auc = evaluator.evaluate(predictions)
    logger.info(f"Model AUC: {auc:.3f}")
    
    # Show some predictions
    logger.info("Sample predictions:")
    predictions.select("title", "label", "prediction").show(10, truncate=False)
    
    return model

def save_model(model, model_path):
    """Save the trained model"""
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.write().overwrite().save(model_path)
    logger.info(f"✅ Model saved to {model_path}")

def main():
    """Main training function"""
    try:
        # Initialize Spark
        spark = create_spark_session()
        
        # Load and validate data
        data_path = "data/labeled/headlines_labeled.csv"
        df = load_and_validate_data(data_path)
        
        # Train and evaluate model
        model = train_and_evaluate_model(df)
        
        # Save model
        model_path = "models/news_sentiment_model"
        save_model(model, model_path)
        
        logger.info("✅ Training completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        raise
    finally:
        # Clean up
        if SparkSession.getActiveSession():
            SparkSession.getActiveSession().stop()

if __name__ == "__main__":
    main()
