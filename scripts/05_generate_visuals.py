# scripts/05_generate_visuals.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

print("Starting visualization script...")

# Define the paths
data_path = 'data/cleaned_reviews.csv'
visuals_path = 'visuals'

# --- Ensure the visuals directory exists ---
# This is a robust way to make sure the folder is there before trying to save files in it.
if not os.path.exists(visuals_path):
    os.makedirs(visuals_path)
    print(f"Created directory: {visuals_path}")

# --- Load the data ---
try:
    df = pd.read_csv(data_path)
    print("Successfully loaded analyzed_reviews.csv")
except FileNotFoundError:
    print(f"Error: The file {data_path} was not found.")
    print("Please make sure you have successfully run the analysis script (03_analyze_sentiment_themes.py) first.")
    exit()

# --- Plot 1: Rating Distribution per Bank ---
print("Generating plot 1: Rating Distribution...")
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='rating', hue='bank', palette='viridis')
plt.title('Figure 1: Distribution of User Ratings by Bank', fontsize=16)
plt.xlabel('Star Rating (1-5)', fontsize=12)
plt.ylabel('Number of Reviews', fontsize=12)
plt.legend(title='Bank')
plt.tight_layout() # Adjusts plot to prevent labels from overlapping

# Save the figure
rating_plot_path = os.path.join(visuals_path, 'rating_distribution.png')
plt.savefig(rating_plot_path)
print(f"Saved plot to: {rating_plot_path}")
plt.close() # Close the plot to free up memory

# --- Plot 2: Sentiment Distribution per Bank ---
print("Generating plot 2: Sentiment Distribution...")
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='sentiment_label', hue='bank', palette='plasma', order=['POSITIVE', 'NEGATIVE']) # Set order for clarity
plt.title('Figure 2: Sentiment of User Reviews by Bank', fontsize=16)
plt.xlabel('Sentiment', fontsize=12)
plt.ylabel('Number of Reviews', fontsize=12)
plt.legend(title='Bank')
plt.tight_layout()

# Save the figure
sentiment_plot_path = os.path.join(visuals_path, 'sentiment_distribution.png')
plt.savefig(sentiment_plot_path)
print(f"Saved plot to: {sentiment_plot_path}")
plt.close()

print("\nVisualization script finished successfully.")