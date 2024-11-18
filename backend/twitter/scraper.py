import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class UserScrapper:
    def __init__(self):
        # Initialize WebDriver (using Chrome)
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")  # Optional: run browser in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Define scraping limits for light and deep modes
        self.light_post = 7
        self.light_usecom = 2
        self.deep_post = 15
        self.deep_usecom = 15

    def login_to_twitter(self, username, password):
        """Log in to Twitter using the provided username and password."""
        login_url = 'https://x.com/login'
        self.driver.get(login_url)
        
        try:
            # Wait for the username field and enter the username
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'text'))
            )
            username_input = self.driver.find_element(By.NAME, 'text')
            username_input.send_keys(username)
            username_input.send_keys(Keys.RETURN)

            # Wait for the password field and enter the password
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            password_input = self.driver.find_element(By.NAME, 'password')
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)

            time.sleep(5)  # Wait for login to complete
        except Exception as e:
            print(f"Login failed: {e}")
            self.driver.quit()

    def scroll_down(self):
        """Scroll down the page to load more tweets."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new tweets to load

    def scrape_user(self, value_username, mode):
        """Scrape user data based on the mode ('light' or 'deep')."""
        # Set the limits based on the mode
        if mode == 'light':
            num_posts = self.light_post
        elif mode == 'deep':
            num_posts = self.deep_post

        profile_url = f'https://x.com/{value_username}'
        self.driver.get(profile_url)

        try:
            # Wait for the tweets to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@data-testid="tweet"]'))
            )

            posts = []
            while len(posts) < num_posts:
                # Find all visible tweets
                current_posts = self.driver.find_elements(By.XPATH, '//*[@data-testid="tweetText"]')
                posts.extend(current_posts)

                # Scroll down to load more tweets if not enough are loaded
                if len(posts) < num_posts:
                    self.scroll_down()
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@data-testid="tweetText"]')))
            # Limit to the number of posts requested
            posts = posts[:num_posts]

            # Print the text of each tweet
            for i, post in enumerate(posts):
                tweet_text = post.text
                print(f"Post {i + 1}: {tweet_text}\n")

        except Exception as e:
            print(f"Error scraping user profile: {e}")

    def close_session(self):
        """Close the browser session."""
        self.driver.quit()


if __name__ == '__main__':
    user_scrapper = UserScrapper()
    user_scrapper.login_to_twitter(os.getenv('TWITTER_USERNAME'), os.getenv('TWITTER_PASSWORD'))
    user_scrapper.scrape_user('elonmusk', 'light')  # Change 'light' to 'deep' for deep mode
    user_scrapper.close_session()
