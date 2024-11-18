import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse
import os

class HashTagScrapper:
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
            time.sleep(2)
            password_input.send_keys(password)

            # Submit the login form
            password_input.send_keys(Keys.RETURN)
            time.sleep(5)  # Wait for login to complete
        except Exception as e:
            print(f"Login failed: {e}")
            self.driver.quit()

    def scrape_hashtag(self, value_hashtag, mode):
        """Scrape user data based on the mode ('light' or 'deep')."""
        if mode == 'light':
            num_posts = self.light_post
            num_comments = self.light_usecom
        elif mode == 'deep':
            num_posts = self.deep_post
            num_comments = self.deep_usecom

        # Navigate to the hashtag page
        profile_url = f'https://www.instagram.com/explore/search/keyword/?q=%23{value_hashtag}&hl=en'
        self.driver.get(profile_url)
        time.sleep(5)

        # Select post links (a elements with href attribute)
        posts = self.driver.find_elements(By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x4gyw5p._a6hd')[:1]
        print(len(posts))
        print(posts)
        user_data = {
            "hashtag": value_hashtag,
            "posts": []
        }
        posts[0].click()
        time.sleep(2) #peheli post pe click karega
        idx = 0
        # # Loop through post links and extract data
        for _ in range(num_posts):
            try:
                # Get the href attribute (post URL)
                
                time.sleep(3)  # Wait for the post to load
                print("test 1")
                # Extract the caption
                try:
                    caption_element = self.driver.find_element(By.CSS_SELECTOR, 'h1._ap3a._aaco._aacu._aacx._aad7._aade')
                    caption = caption_element.text
                except:
                    caption = "No caption"

                # Extract comments and usernames
                comments = []
                comment_elements = self.driver.find_elements(By.CSS_SELECTOR, 'span._ap3a._aaco._aacu._aacx._aad7._aade')[:num_comments]
                username_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.x1i10hfl.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.xjyslct.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.x1ypdohk.x1f6kntn.xwhw2v2.xl56j7k.x17ydfre.x2b8uid.xlyipyv.x87ps6o.x14atkfc.xcdnw81.x1i0vuye.xjbqb8w.xm3z3ea.x1x8b98j.x131883w.x16mih1h.x972fbf.xcfux6l.x1qhh985.xm0m39n.xt0psk2.xt7dq6l.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x1n5bzlp.xqnirrm.xj34u2y.x568u83')[:num_comments]
                print("test 2")
                for i in range(len(comment_elements)):
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
                    "profile_link": username_elements[0].get_attribute('href'),
                    "caption": caption,
                    "comments": comments
                }

                # Add post data to the list
                user_data["posts"].append(post_data)

                # Return to the hashtag page
                # self.driver.back()
                
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="Next"]')
                next_button.click()
                print("test 3")
                time.sleep(2)
                idx+=1

            except Exception as e:
                print(f"Error extracting post: {e}")

        # Save the data in JSON format
        with open('instagram_hashtag_posts.json', 'w', encoding='utf-8') as json_file:
            json.dump(user_data, json_file, indent=4, ensure_ascii=False)

        #Print the extracted data
        print("Extracted Posts Data: ", user_data)

    def close_session(self):
        """Close the browser session."""
        self.driver.quit()

# Example usage (uncomment and customize as needed)
if __name__ == '__main__':
    user_scrapper = HashTagScrapper()
    user_scrapper.login_to_instagram(os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))
    user_scrapper.scrape_hashtag('hsluts4mstuds', 'light')
    user_scrapper.close_session()
