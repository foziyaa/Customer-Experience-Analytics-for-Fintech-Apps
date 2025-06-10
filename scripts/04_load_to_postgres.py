# scripts/04_load_to_postgres.py (Enhanced Debugging Version)

import pandas as pd
import psycopg2

def load_data_to_postgres():
    print("--- Starting Enhanced Debugging Data Loading Script ---")

    # --- 1. Load Data ---
    try:
        df = pd.read_csv('data/analyzed_reviews.csv')
        df['review'] = df['review'].fillna('')
        df['themes'] = df['themes'].fillna('General Feedback')
        print(f"✅ Loaded {len(df)} rows from 'analyzed_reviews.csv'.")
    except Exception as e:
        print(f"❌ Failed to load or process CSV file: {e}")
        return

    # --- 2. Connection ---
    conn_params = {
        "host": "localhost", "port": 7890, "database": "bank_reviews",
        "user": "postgres", "password": "lier4638"
    }
    
    conn = None
    try:
        print("\nConnecting to database...")
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        print("✅ Connection successful!")
        
        # --- 3. Banks Table ---
        unique_banks = df['bank'].unique()
        bank_map = {}
        print("\nPopulating Banks table...")
        for bank_name in unique_banks:
            cur.execute("INSERT INTO Banks (bank_name) VALUES (%s) ON CONFLICT (bank_name) DO NOTHING;", (bank_name,))
            cur.execute("SELECT bank_id FROM Banks WHERE bank_name = %s;", (bank_name,))
            bank_id = cur.fetchone()[0]
            bank_map[bank_name] = bank_id
        print("✅ Banks table populated.")

        # --- 4. Reviews Table ---
        print("\nPopulating Reviews table...")
        df['bank_id'] = df['bank'].map(bank_map)
        
        print("Clearing existing data from Reviews table...")
        cur.execute("TRUNCATE TABLE Reviews RESTART IDENTITY CASCADE;")
        
        reviews_to_insert = [(row.bank_id, row.review, row.rating, row.date, row.sentiment_label, row.sentiment_score, row.themes, row.source) for row in df.itertuples(index=False)]
        
        print(f"Prepared {len(reviews_to_insert)} rows for insertion.")
        
        insert_query = "INSERT INTO Reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, identified_themes, source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        
        print("Executing INSERT statement...")
        cur.executemany(insert_query, reviews_to_insert)
        
        print(f"✅ {cur.rowcount} records reported as inserted.")
        
        # --- 5. Commit ---
        print("Committing transaction...")
        conn.commit()
        print("✅ Transaction committed successfully.")

    except (Exception, psycopg2.Error) as error:
        print("\n" + "#"*60)
        print("###!  AN ERROR OCCURRED DURING THE DATABASE OPERATION  !###")
        print(f"###!  Error Details: {error}")
        print("#"*60 + "\n")
        if conn:
            conn.rollback()
            print("Transaction has been rolled back.")
    
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    load_data_to_postgres()