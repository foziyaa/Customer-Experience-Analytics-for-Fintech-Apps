import pandas as pd
from google_play_scraper import reviews, Sort

apps = {
    'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',
    'Bank of Abyssinia': 'com.boa.boaMobileBanking',
    'Dashen Bank': 'com.dashen.dashensuperapp'
}

all_reviews = []
for bank, app_id in apps.items():
    print(f"Scraping reviews for {bank}...")
   
    result, _ = reviews(
        app_id,
        lang='en',
        country='us',
        sort=Sort.NEWEST,
        count=500
    )
    for rev in result:
        rev['bank'] = bank
        rev['source'] = 'Google Play'
    all_reviews.extend(result)

df = pd.DataFrame(all_reviews)
df.to_csv('data/scraped_reviews_raw.csv', index=False)
print("Scraping complete. Raw data saved to data/scraped_reviews_raw.csv")