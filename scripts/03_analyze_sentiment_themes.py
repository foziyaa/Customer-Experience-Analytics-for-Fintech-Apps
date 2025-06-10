# scripts/03_analyze_sentiment_themes.py

import pandas as pd
from transformers import pipeline
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import torch

def perform_analysis():
    """
    Main function to run sentiment and thematic analysis.
    """
    print("--- Starting Analysis Script ---")

    # --- 1. Load Cleaned Data ---
    try:
        df = pd.read_csv('data/cleaned_reviews.csv')
        print(f"Successfully loaded 'cleaned_reviews.csv' with {len(df)} rows.")
    except FileNotFoundError:
        print("Error: 'data/cleaned_reviews.csv' not found. Please run the preprocessing script first.")
        return # Stop execution if file doesn't exist

    # --- 2. Sentiment Analysis ---
    print("\n--- Performing Sentiment Analysis ---")
    # Check for GPU, otherwise use CPU
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Using a smaller, faster model for compatibility. If you have issues, this is a good alternative.
    # model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    
    print(f"Loading sentiment analysis pipeline with model: {model_name}...")
    sentiment_pipeline = pipeline("sentiment-analysis", model=model_name, device=device)
    
    # To avoid long run times, let's analyze a sample first if needed
    # To run on all data, comment out the next line.
    # df = df.head(100).copy()
    
    # Applying the pipeline to the 'review' column
    # The tolist() method is important for performance.
    reviews_list = df['review'].dropna().tolist()
    sentiment_results = sentiment_pipeline(reviews_list, batch_size=8, truncation=True) # Use batching and truncation for robustness
    
    df['sentiment_label'] = [res['label'] for res in sentiment_results]
    df['sentiment_score'] = [res['score'] for res in sentiment_results]
    print("Sentiment analysis complete.")

    # --- 3. Thematic Analysis (Keyword Extraction) ---
    print("\n--- Performing Thematic Analysis ---")
    print("Loading spaCy model for text processing...")
    nlp = spacy.load("en_core_web_sm")

    def preprocess_text(text):
        if not isinstance(text, str):
            return ""
        doc = nlp(text.lower())
        # Lemmatize and remove stopwords, punctuation, and non-alphabetic characters
        return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha])

    df['processed_review'] = df['review'].apply(preprocess_text)
    print("Text preprocessing for thematic analysis complete.")

    # Define themes and associated keywords
    theme_map = {
        'Account & Login': ['login', 'password', 'register', 'signin', 'otp', 'access', 'account', 'verify'],
        'Transactions': ['transfer', 'transaction', 'send', 'money', 'payment', 'fee', 'charge', 'limit'],
        'App Performance': ['slow', 'fast', 'load', 'crash', 'bug', 'error', 'stuck', 'performance', 'update'],
        'User Interface': ['ui', 'interface', 'easy', 'design', 'user-friendly', 'dark', 'mode', 'look', 'layout'],
        'Customer Support': ['support', 'customer', 'service', 'help', 'response', 'contact', 'call'],
        'Feature Request': ['feature', 'add', 'suggest', 'wish', 'fingerprint', 'biometric', 'need']
    }

    def assign_theme(processed_text):
        assigned_themes = set()
        for theme, keywords in theme_map.items():
            if any(keyword in processed_text for keyword in keywords):
                assigned_themes.add(theme)
        return ', '.join(sorted(list(assigned_themes))) if assigned_themes else 'General Feedback'

    df['themes'] = df['processed_review'].apply(assign_theme)
    print("Theme assignment complete.")

    # --- 4. Save the Final Analyzed Data ---
    output_path = 'data/analyzed_reviews.csv'
    df.to_csv(output_path, index=False)
    print(f"\n--- Analysis Complete. Results saved to '{output_path}' ---")

# This is the standard Python way to make a script runnable
if __name__ == '__main__':
    perform_analysis()