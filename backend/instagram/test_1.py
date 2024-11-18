import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Instagram login function
def login_to_instagram(username, password):
    login_url = 'https://www.instagram.com/accounts/login/'
    driver.get(login_url)
    
    time.sleep(5)  # Allow time for page to load
    
    # Locate and input username and password fields
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    
    username_input.send_keys(username)
    time.sleep(2)
    password_input.send_keys(password)
    
    # Submit the login form
    password_input.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Wait for login to complete

# Take input from the user for the Instagram credentials and target username
instagram_username = input("Enter your Instagram username: ")
instagram_password = input("Enter your Instagram password: ")
target_username = input("Enter the Instagram username you want to search: ")

# Initialize WebDriver (using Chrome)
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")  # Optional: run browser in the background

driver = webdriver.Chrome(options=chrome_options)

# Call the login function
login_to_instagram(instagram_username, instagram_password)

# Now go to the target profile
profile_url = f'https://www.instagram.com/{target_username}/'
driver.get(profile_url)

# Give the page time to load
time.sleep(5)

# Scroll down to load more posts (if needed)
# driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
# time.sleep(3)

# Get post elements (for the top 10 posts)
posts = driver.find_elements(By.CSS_SELECTOR, 'div.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x2pgyrj.x56m6dy.x1ntc13c.xn45foy.x9i3mqj')[:3]

# Array to store post data in JSON format
posts_data = []

# Loop through the top 10 posts
for post in posts:
    try:
        # Click on the post
        post.click()
        time.sleep(3)  # Wait for the post to load

        # Extract the caption from the h1 element
        try:
            caption_element = driver.find_element(By.CSS_SELECTOR, 'h1._ap3a._aaco._aacu._aacx._aad7._aade')
            caption = caption_element.text
        except:
            caption = "No caption"

        # Extract the top 15 comments and usernames
        comments = []
        comment_elements = driver.find_elements(By.CSS_SELECTOR, 'span._ap3a._aaco._aacu._aacx._aad7._aade')[:5]
        username_elements = driver.find_elements(By.CSS_SELECTOR, 'a.x1i10hfl.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w')[:5]

        for i in range(len(comment_elements)):
            try:
                # Extract the username and href (profile link)
                username = username_elements[i].text
                profile_link = username_elements[i].get_attribute('href')  # Get href attribute for profile link
                comment_text = comment_elements[i].text
                comments.append({
                    "username": username,
                    "profile_link": profile_link,
                    "comment": comment_text
                })
            except:
                comments.append({
                    "username": "Unknown",
                    "profile_link": "Unknown",
                    "comment": "Unknown"
                })

        # Create a dictionary for the post data
        post_data = {
            "caption": caption,
            "comments": comments
        }
        
        # Add the post data to the array
        posts_data.append(post_data)
        
        # Return to the main profile page
        driver.back()
        time.sleep(2)
        
    except Exception as e:
        print(f"Error extracting post: {e}")

# Save the data in JSON format
with open('instagram_posts.json', 'w') as json_file:
    json.dump(posts_data, json_file, indent=4)

# Print the extracted data
print("Extracted Posts Data: ", posts_data)

# Close the browser session
driver.quit()