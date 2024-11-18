import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse
import os

class UserScrapper:
    def __init__(self):
        # Initialize WebDriver (using Chrome)
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")  # Optional: run browser in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Define scraping limits
        self.light_post = 10
        self.light_usecom = 10
        self.deep_post = 15
        self.deep_usecom = 15

    def login_to_twitter(self, username, password):
        """Log in to Twitter using the provided username and password."""
        login_url = 'https://x.com/login'
        self.driver.get(login_url)
        time.sleep(5)  

        try:
            # Locate username and password fields
            username_input = self.driver.find_element(By.NAME, 'text')
            username_input.send_keys(username)
            username_input.send_keys(Keys.RETURN)
            time.sleep(3)
            
            password_input = self.driver.find_element(By.NAME, 'password')
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)

            time.sleep(5)  # Wait for login to complete
        except Exception as e:
            print(f"Login failed: {e}")
            self.driver.quit()

    def scrape_user(self, value_username, mode):
        """Scrape user data based on the mode ('light' or 'deep')."""
        if mode == 'light':
            num_posts = self.light_post
            num_comments = self.light_usecom
        elif mode == 'deep':
            num_posts = self.deep_post
            num_comments = self.deep_usecom

        # Navigate to the user's profile
        profile_url = f'https://x.com/{value_username}'
        self.driver.get(profile_url)
        time.sleep(5)

        # Extract tweets
        posts = self.driver.find_elements(By.CSS_SELECTOR, 'div.css-146c3p1.r-8akbws.r-krxsd3.r-dnmrzs.r-1udh08x.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-16dba41.r-bnwqim')[:num_posts]
        user_data = {"username":value_username,"posts":[]}  # Initialize user data for the current user

        # Loop through posts and extract data
        for post in posts:
            try:
                # Click on the post to expand (if needed)
                post.click()
                time.sleep(3)  # Wait for the post to load

                # Extract the tweet text (caption equivalent)
                try:
                    # Locate the specific div and span for tweet text using the data-testid and CSS class
                    tweet_text_element = post.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"] span')
                    tweet_text = tweet_text_element.text
                except:
                    tweet_text = "No text found"

                # Extract comments and usernames
                comments = []
                comment_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetText"] span')[:num_comments]
                username_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.css-175oi2r.r-1wbh5a2.r-dnmrzs.r-1ny4l3l.r-1loqt21')[:num_comments]

                for i in range(len(comment_elements)):
                    try:
                        # Extract the username and href (profile link)
                        profile_link = username_elements[i].get_attribute('href')  # Get href attribute for profile link
                        profile_username = urlparse(profile_link).path.strip('/')  # Extract username from the URL
                        comment_text = comment_elements[i].text
                        
                        comments.append({
                            "username": profile_username,
                            "profile_link": profile_link,  # Use the link directly
                            "comment": comment_text
                        })
                    except Exception as e:
                        comments.append({
                            "username": "Unknown",
                            "profile_link": "Unknown",
                            "comment": "Unknown"
                        })

                # Collect the post data
                post_data = {
                    
                    "tweet_text": tweet_text,
                    "comments": comments
                }

                # Add post data to the list
                user_data["posts"].append(post_data)

                # Return to the profile page
                self.driver.back()
                time.sleep(2)

            except Exception as e:
                print(f"Error extracting post: {e}")

        # Save the data in JSON format
        with open('twitter_user_posts.json', 'w', encoding='utf-8') as json_file:
            json.dump(user_data, json_file, indent=4, ensure_ascii=False)

        # Print the extracted data
        print("Extracted Posts Data: ", user_data)

    def close_session(self):
        """Close the browser session."""
        self.driver.quit()


if __name__ == '__main__':
    user_scrapper = UserScrapper()
    user_scrapper.login_to_twitter(os.getenv('TWITTER_USERNAME'), os.getenv('TWITTER_PASSWORD'))
    user_scrapper.scrape_user('kunalkamra88', 'light')
    user_scrapper.close_session()
