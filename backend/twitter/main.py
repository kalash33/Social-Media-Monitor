import user_scraper
import time
import hashtag_scraper
import sys
import os

# Take inputs
username_or_hashtag= sys.argv[1]  # User or hashtag
data= sys.argv[5]
degree = sys.argv[2]  
depth = sys.argv[3]  # Depth of scraping
platform = sys.argv[4]  # Hardcoded platform
# List of usernames/hashtags for depth 1
print(username_or_hashtag, degree, depth, platform, data)

# Instantiate the correct scraper class
if username_or_hashtag== "User":
    scraper = user_scraper.UserScrapper()  # User scraper
elif username_or_hashtag== "Hashtag":
    scraper = hashtag_scraper.HashTagScrapper()  # Hashtag scraper

# Log in to Instagram (this will be shared across all scraping sessions)
try:
    scraper.login_to_twitter(os.getenv('TWITTER_USERNAME'), os.getenv('TWITTER_PASSWORD'))  # Use correct credentials
except Exception as e:
    print(f"Login failed: {e}")
    exit()

time.sleep(2)

# Scraping logic
try:
    if depth == 0 or depth == 1:
        # Single user/hashtag scraping
        if username_or_hashtag== "User":
            scraper.scrape_user(data, degree)  # Call user scraping method
        elif username_or_hashtag== "Hashtag":
            scraper.scrape_hashtag(data, degree)  # Call hashtag scraping method

except Exception as e:
    print(f"Scraping failed: {e}")

# Quit the scraper session
scraper.driver.quit()
