
import pandas as pd

df = pd.read_csv('data/scraped_reviews_raw.csv')

df_clean = df[['content', 'score', 'at', 'bank', 'source']].copy()
df_clean.rename(columns={'content': 'review', 'score': 'rating', 'at': 'date'}, inplace=True)

df_clean.dropna(subset=['review'], inplace=True)

df_clean['date'] = pd.to_datetime(df_clean['date']).dt.strftime('%Y-%m-%d')

df_clean.drop_duplicates(subset=['review', 'date', 'bank'], inplace=True)

df_clean['review'] = df_clean['review'].str.strip()

df_clean.to_csv('data/cleaned_reviews.csv', index=False)
print(f"Preprocessing complete. Cleaned data has {len(df_clean)} rows.")
print("Cleaned data saved to data/cleaned_reviews.csv")