import user_scraper
import time
import hashtag_scraper
import sys
import os
# Take inputs
scrape_type = sys.argv[1]  # User or hashtag
data = sys.argv[5]
degree = sys.argv[2]  
depth = (int)(sys.argv[3])  # Depth of scraping
platform = sys.argv[4]  # Hardcoded platform
# List of usernames/hashtags for depth 1
print("scraper type:",scrape_type, "data:",data, "degree:",degree, "depth:",depth, "platform:",platform)

# Instantiate the correct scraper class
if scrape_type == "User":
    scraper = user_scraper.UserScrapper()  # User scraper
elif scrape_type == "Hashtag":
    scraper = hashtag_scraper.HashTagScrapper()  # Hashtag scraper

# Log in to Instagram (this will be shared across all scraping sessions)
try:
    scraper.login_to_instagram(os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))  # Use correct credentials
except Exception as e:
    print(f"Login failed: {e}")
    exit()

time.sleep(2)

# Scraping logic
try:
    if depth == 0 or depth == 1:
        # Single user/hashtag scraping
        if scrape_type == "User":
            scraper.scrape_user(data,degree)  # Call user scraping method
        elif scrape_type == "Hashtag":
            print("Entering the hashtag Scrapper")
            scraper.scrape_hashtag(data, degree)  # Call hashtag scraping method

    # elif depth == 1:
    #     # Multiple users/hashtags scraping
    #     for target in targets:
    #         if scrape_type == "User":
    #             scraper.scrape_user(target, degree)  # Scrape each user
    #         elif scrape_type == "Hashtag":
    #             scraper.scrape_hashtag(target, degree)  # Scrape each hashtag
    #         time.sleep(3)

except Exception as e:
    print(f"Scraping failed: {e}")

# Quit the scraper session
scraper.driver.quit()
