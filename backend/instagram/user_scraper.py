import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        self.light_post = 3
        self.light_usecom = 10
        self.deep_post = 15
        self.deep_usecom = 15

    def login_to_instagram(self, username, password):
        """Log in to Instagram using the provided username and password."""
        login_url = 'https://www.instagram.com/accounts/login/'
        self.driver.get(login_url)
        time.sleep(5)  # Allow time for page to load

        try:
            # Locate and input username and password fields
            username_input = self.driver.find_element(By.NAME, 'username')
            password_input = self.driver.find_element(By.NAME, 'password')

            # Fill in the username and password
            username_input.send_keys(username)
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.NAME, 'password')))
            password_input.send_keys(password)

            # Submit the login form
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
        profile_url = f'https://www.instagram.com/{value_username}/'
        self.driver.get(profile_url)
        time.sleep(5)

        # Select posts and limit based on the mode
        posts = self.driver.find_elements(By.CSS_SELECTOR, 'div.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.xfllauq.xo2y696.x11i5rnm.x2pgyrj')[:num_posts]
        user_data = {
            "username": value_username,
            "posts": []
        }

        # Loop through posts and extract data
        for idx, post in enumerate(posts):
            try:
                # Click on the post
                post.click()
                time.sleep(3)  # Wait for the post to load

                # Extract the caption
                try:
                    caption_element = self.driver.find_element(By.CSS_SELECTOR, 'h1._ap3a._aaco._aacu._aacx._aad7._aade')
                    caption = caption_element.text
                except:
                    caption = "No caption"

                # Extract comments and usernames
                comments = []
                comment_elements = self.driver.find_elements(By.CSS_SELECTOR, 'span._ap3a._aaco._aacu._aacx._aad7._aade')[:num_comments]
                username_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.x1i10hfl.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w')[:num_comments]

                for i in range(len(comment_elements)-1):
                    try:
                        # Extract the username and href (profile link)
                        profile_link = username_elements[i+1].get_attribute('href')  # Get href attribute for profile link
                        profile_username = urlparse(profile_link).path.strip('/')  # Extract username from the URL
                        comment_text = comment_elements[i].text

                        comments.append({
                            "username": profile_username,
                            "profile_link": profile_link,
                            "comment": comment_text
                        })
                    except Exception as e:
                        comments.append({
                            "username": "Unknown",
                            "profile_link": "Unknown",
                            "comment": "Unknown"
                        })

                # Collect the post data in the new format
                post_data = {
                    "post": f"Post {idx+1}",
                    "username":username_elements[0].text,
                    "profile_link":username_elements[0].get_attribute('href'),
                    "caption": caption,
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
        with open('instagram_user_posts.json', 'w', encoding='utf-8') as json_file:
            json.dump(user_data, json_file, indent=4, ensure_ascii=False)

        # Print the extracted data
        print("Extracted Posts Data: ", user_data)

    def close_session(self):
        """Close the browser session."""
        self.driver.quit()

# Example usage (uncomment and customize as needed)
if __name__ == '__main__':
    user_scrapper = UserScrapper()
    user_scrapper.login_to_instagram(os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))
    user_scrapper.scrape_user('aurangzeb_alamgir.ra', 'light')
    user_scrapper.close_session()
