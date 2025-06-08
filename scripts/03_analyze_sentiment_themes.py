import pandas as pd
from transformers import pipeline

df = pd.read_csv('data/cleaned_reviews.csv')


sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
results = sentiment_pipeline(df['review'].tolist())

df['sentiment_label'] = [res['label'] for res in results]
df['sentiment_score'] = [res['score'] for res in results]