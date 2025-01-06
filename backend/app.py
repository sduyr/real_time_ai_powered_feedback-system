# import openai
# from dotenv import load_dotenv
# import os

# # Load API key from environment variables
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def get_gpt_response(prompt):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # Specify the model
#             messages=[
#                 {"role": "system", "content": "You are an AI feedback analyst. Your task is to analyze user feedback and provide concise, actionable insights. Clearly state the sentiment (positive, negative, or mixed) and summarize the key themes in the feedback."},
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         # Access the content from the response
#         return response.choices[0].message.content.strip()
#     except openai.OpenAIError as e:
#         return f"Error: {e}"

# if __name__ == "__main__":
#     user_input = input("Enter feedback or a question: ")
#     response = get_gpt_response(user_input)
#     print("GPT Response:", response)
import openai
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import logging
import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# import logging
# import time

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load API key from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# def scrape_reviews(product_id):
#     """
#     Scrape Amazon reviews based on the given product ID.
#     """
#     try:
#         logging.info(f"Scraping reviews for Amazon product ID: {product_id}")

#         # Construct the Amazon reviews URL
#         url = f"https://www.amazon.com/product-reviews/{product_id}"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Accept-Language": "en-US,en;q=0.9",
#         }

#         # Make the HTTP GET request
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an error for bad HTTP responses

#         # print the raw HTML content for debugging
#         print(response.text)


#         # Parse the HTML content
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Extract review content
#         reviews = []
#         review_tags = soup.find_all('span', {'data-hook': 'review-body'})
#         reviews = [tag.get_text(strip=True) for tag in review_tags]
#         return reviews
#         # for tag in review_tags:
#         #     reviews.append(tag.get_text(strip=True))

#         # logging.info(f"Scraped {len(reviews)} reviews successfully.")
#         # return reviews

#     # except requests.exceptions.RequestException as e:
#     #     logging.error(f"HTTP request failed: {e}")
#     #     return f"Error scraping reviews: {e}"

#     except Exception as e:
#         logging.error(f"Error scraping reviews: {e}")
#         return f"Error scraping reviews: {e}"

# def scrape_reviews(product_id):
#     """
#     Scrape Amazon reviews for the given product ID by extracting the entire reviews section.
#     """
#     try:
#         logging.info(f"Scraping reviews for product ID: {product_id}")

#         # Construct the Amazon reviews URL
#         url = f"https://www.amazon.com/product-reviews/{product_id}"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Accept-Language": "en-US,en;q=0.9",
#         }

#         # Make the HTTP GET request
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an error for bad HTTP responses

#         # Parse the HTML content
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Find the container holding all reviews
#         reviews_container = soup.find('div', {'id': 'cm_cr-review_list'})
#         if not reviews_container:
#             logging.warning("No reviews container found.")
#             return []

#         # Extract all reviews from the container
#         reviews = []
#         review_blocks = reviews_container.find_all('div', {'data-hook': 'review'})  # Each review block
#         for block in review_blocks:
#             # Extract the review text
#             review_text = block.find('span', {'data-hook': 'review-body'})
#             if review_text:
#                 reviews.append(review_text.get_text(strip=True))

#         if not reviews:
#             logging.warning("No reviews found within the container.")
#         else:
#             logging.info(f"Scraped {len(reviews)} reviews successfully.")

#         return reviews

#     except requests.exceptions.RequestException as e:
#         logging.error(f"HTTP request failed: {e}")
#         return f"Error scraping reviews: {e}"

#     except Exception as e:
#         logging.error(f"Error scraping reviews: {e}")
#         return f"Error scraping reviews: {e}"


# def scrape_reviews(product_id):
#     """
#     Scrape all Amazon reviews for the given product ID across all pages.
#     """
#     try:
#         logging.info(f"Scraping reviews for Amazon product ID: {product_id}")

#         base_url = f"https://www.amazon.com/product-reviews/{product_id}"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Accept-Language": "en-US,en;q=0.9",
#         }

#         reviews = []
#         page_number = 1

#         while True:
#             # Construct the URL for the current page
#             url = f"{base_url}/?pageNumber={page_number}"
#             logging.info(f"Fetching reviews from: {url}")

#             # Make the HTTP GET request
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()  # Raise an error for bad HTTP responses

#             # Log response status
#             logging.debug(f"Response Status Code: {response.status_code}")
#             logging.debug(f"Response URL: {response.url}")

#             # Parse the HTML content
#             soup = BeautifulSoup(response.text, 'html.parser')

#             # Extract review content
#             review_tags = soup.find_all('span', {'data-hook': 'review-body'})
#             if not review_tags:
#                 logging.warning("No reviews found on this page. Stopping pagination.")
#                 break  # Stop if no reviews are found on the page

#             # Add reviews from the current page
#             for tag in review_tags:
#                 reviews.append(tag.get_text(strip=True))

#             logging.info(f"Scraped {len(review_tags)} reviews from page {page_number}.")

#             # Check if there is a "Next" button for pagination
#             next_button = soup.find('li', {'class': 'a-last'})
#             if not next_button or not next_button.find('a'):
#                 logging.info("No more pages found. Stopping pagination.")
#                 break  # Stop if no "Next" button is found

#             # Increment the page number for the next iteration
#             page_number += 1

#         logging.info(f"Total reviews scraped: {len(reviews)}")
#         return reviews

#     except requests.exceptions.RequestException as e:
#         logging.error(f"HTTP request failed: {e}")
#         return f"Error scraping reviews: {e}"

#     except Exception as e:
#         logging.error(f"Error scraping reviews: {e}")
#         return f"Error scraping reviews: {e}"

# def scrape_reviews(product_id):
#     """
#     Scrape all Amazon reviews for the given product ID across all pages.
#     """
#     try:
#         logging.info(f"Scraping reviews for Amazon product ID: {product_id}")

#         # Base URL for the reviews page
#         base_url = f"https://www.amazon.com/product-reviews/{product_id}"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Accept-Language": "en-US,en;q=0.9",
#         }

#         reviews = []
#         page_number = 1

#         while True:
#             # Construct the URL for the current page
#             url = f"{base_url}/?pageNumber={page_number}"
#             logging.info(f"Fetching reviews from: {url}")

#             # Make the HTTP GET request
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()  # Raise an error for bad HTTP responses

#             # Parse the HTML content
#             soup = BeautifulSoup(response.text, 'html.parser')

#             # Find the container that holds all reviews
#             reviews_container = soup.find('div', {'id': 'cm_cr-review_list'})
#             if not reviews_container:
#                 logging.warning("No reviews container found. Stopping scraping.")
#                 break  # Stop if no review container is found

#             # Extract all reviews from the container
#             review_blocks = reviews_container.find_all('div', {'class': "a-row a-spacing-small review-data"})
#             for block in review_blocks:
#                 # Extract the review text
#                 review_text = block.find('span', {'data-hook': "review-body", 'class': "a-size-base review-text review-text-content"})
#                 if review_text:
#                     reviews.append(review_text.get_text(strip=True))

#             logging.info(f"Scraped {len(review_blocks)} reviews from page {page_number}.")

#             # Check if there is a "Next" button for pagination
#             next_button = soup.find('li', {'class': "review aok-relative"})
#             if not next_button or not next_button.find('a'):
#                 logging.info("No more pages found. Stopping pagination.")
#                 break  # Stop if no "Next" button is found

#             # Increment the page number for the next iteration
#             page_number += 1

#             # Add delay to avoid being blocked
#             time.sleep(2)

#         logging.info(f"Total reviews scraped: {len(reviews)}")
#         return reviews

#     except requests.exceptions.RequestException as e:
#         logging.error(f"HTTP request failed: {e}")
#         return f"Error scraping reviews: {e}"

#     except Exception as e:
#         logging.error(f"Error scraping reviews: {e}")
#         return f"Error scraping reviews: {e}"


# def scrape_reviews(product_id):
#     """
#     Scrape all Amazon reviews for the given product ID across all pages.
#     """
#     try:
#         logging.info(f"Scraping reviews for Amazon product ID: {product_id}")

#         # Base URL for the reviews page
#         base_url = f"https://www.amazon.com/product-reviews/{product_id}"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Accept-Language": "en-US,en;q=0.9",
#         }

#         reviews = []
#         page_number = 1

#         while True:
#             # Construct the URL for the current page
#             url = f"{base_url}/?pageNumber={page_number}"
#             logging.info(f"Fetching reviews from: {url}")

#             # Make the HTTP GET request
#             response = requests.get(url, headers=headers)
#             logging.debug(f"Response URL: {response.url}")
#             logging.debug(f"Response Headers: {response.headers}")
#             logging.debug(f"Response Content Preview: {response.text[:500]}")  # Print first 500 characters
#             response.raise_for_status()  # Raise an error for bad HTTP responses

#             # Parse the HTML content
#             soup = BeautifulSoup(response.text, 'html.parser')

#             # Find all review blocks
#             review_blocks = soup.find_all('li', {'class': 'review aok-relative', 'data-hook': 'review'})
#             if not review_blocks:
#                 logging.warning("No reviews found on this page. Stopping scraping.")
#                 break  # Stop if no reviews are found

#             # Extract review text from each review block
#             for block in review_blocks:
#                 review_text = block.find('span', {'class': 'a-size-base review-text review-text-content', 'data-hook': 'review-body'})
#                 if review_text:
#                     reviews.append(review_text.get_text(strip=True))

#             logging.info(f"Scraped {len(review_blocks)} reviews from page {page_number}.")

#             # Check if there is a "Next" button for pagination
#             next_button = soup.find('li', {'class': 'a-last'})
#             if not next_button or not next_button.find('a'):
#                 logging.info("No more pages found. Stopping pagination.")
#                 break  # Stop if no "Next" button is found

#             # Increment the page number for the next iteration
#             page_number += 1

#             # Add delay to avoid being blocked
#             time.sleep(2)

#         logging.info(f"Total reviews scraped: {len(reviews)}")
#         return reviews

#     except requests.exceptions.RequestException as e:
#         logging.error(f"HTTP request failed: {e}")
#         return f"Error scraping reviews: {e}"

#     except Exception as e:
#         logging.error(f"Error scraping reviews: {e}")
#         return f"Error scraping reviews: {e}"

# def scrape_reviews(product_id):
#     """
#     Scrape all Amazon reviews for the given product ID across all pages.
#     """
#     try:
#         logging.info(f"Scraping reviews for Amazon product ID: {product_id}")

#         # Base URL for the reviews page
#         base_url = f"https://www.amazon.com/product-reviews/{product_id}"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Accept-Language": "en-US,en;q=0.9",
#         }

#         reviews = []
#         page_number = 1

#         while True:
#             # Construct the URL for the current page
#             url = f"{base_url}/?pageNumber={page_number}"
#             logging.info(f"Fetching reviews from: {url}")

#             # Make the HTTP GET request
#             response = requests.get(url, headers=headers)
#             logging.debug(f"Response Status Code: {response.status_code}")
#             logging.debug(f"Response Content: {response.text[:500]}")  # Debugging

#             response.raise_for_status()  # Raise an error for bad HTTP responses

#             # Parse the HTML content
#             soup = BeautifulSoup(response.text, 'html.parser')

#             # Find all review blocks
#             review_blocks = soup.find_all('li', {'class': 'review aok-relative', 'data-hook': 'review'})
#             if not review_blocks:
#                 logging.warning("No reviews found on this page. Printing HTML content for debugging.")
#                 logging.debug(soup.prettify()[:1000])  # Print the first 1000 characters of the HTML
#                 break  # Stop if no reviews are found

#             # Extract review text from each review block
#             for block in review_blocks:
#                 # Find the specific <div> containing the review data
#                 review_data_div = block.find('div', {'class': 'a-row a-spacing-small review-data'})
#                 if review_data_div:
#                     # Extract the review text from the nested <span>
#                     review_text = review_data_div.find('span', {
#                         'class': 'a-size-base review-text review-text-content',
#                         'data-hook': 'review-body'
#                     })
#                     if review_text:
#                         reviews.append(review_text.get_text(strip=True))

#             logging.info(f"Scraped {len(review_blocks)} reviews from page {page_number}.")

#             # Check if there is a "Next" button for pagination
#             next_button = soup.find('li', {'class': 'a-last'})
#             if not next_button or not next_button.find('a'):
#                 logging.info("No more pages found. Stopping pagination.")
#                 break  # Stop if no "Next" button is found

#             # Increment the page number for the next iteration
#             page_number += 1

#             # Add delay to avoid being blocked
#             time.sleep(2)

#         logging.info(f"Total reviews scraped: {len(reviews)}")
#         return reviews

#     except requests.exceptions.RequestException as e:
#         logging.error(f"HTTP request failed: {e}")
#         return f"Error scraping reviews: {e}"

#     except Exception as e:
#         logging.error(f"Error scraping reviews: {e}")
#         return f"Error scraping reviews: {e}"

# def scrape_reviews(product_id):
#     """
#     Scrape all reviews from the first page of Amazon reviews for the given product ID.
#     """
#     try:
#         logging.info(f"Scraping reviews for Amazon product ID: {product_id}")

#         # Base URL for the reviews page
#         url = f"https://www.amazon.com/product-reviews/{product_id}"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Accept-Language": "en-US,en;q=0.9",
#         }

#         # Make the HTTP GET request
#         response = requests.get(url, headers=headers)
#         logging.debug(f"Response Status Code: {response.status_code}")
#         logging.debug(f"Response Content Preview: {response.text[:500]}")  # Debugging

#         response.raise_for_status()  # Raise an error for bad HTTP responses

#         # Parse the HTML content
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Locate the container with all reviews
#         reviews_container = soup.find('div', {'id': 'cm_cr-review_list'})
#         if not reviews_container:
#             logging.warning("No reviews container found.")
#             return []

#         # Find all review blocks within the container
#         review_blocks = reviews_container.find_all('li', {'class': 'review aok-relative', 'data-hook': 'review'})
#         if not review_blocks:
#             logging.warning("No reviews found on this page.")
#             return []

#         # Extract review text from each review block
#         reviews = []
#         for block in review_blocks:
#             # Locate the <div> with the review data
#             review_data_div = block.find('div', {'class': 'a-row a-spacing-small review-data'})
#             if review_data_div:
#                 # Locate the nested <span> with the review text
#                 review_text = review_data_div.find('span', {
#                     'class': 'a-size-base review-text review-text-content',
#                     'data-hook': 'review-body'
#                 })
#                 if review_text:
#                     reviews.append(review_text.get_text(strip=True))

#         logging.info(f"Total reviews scraped: {len(reviews)}")
#         return reviews

#     except requests.exceptions.RequestException as e:
#         logging.error(f"HTTP request failed: {e}")
#         return f"Error scraping reviews: {e}"

#     except Exception as e:
#         logging.error(f"Error scraping reviews: {e}")
#         return f"Error scraping reviews: {e}"

# the function working with selenium
# def scrape_reviews(product_id):
#     """
#     Scrape all reviews from the first page of Amazon reviews for the given product ID using Selenium.
#     """
#     try:
#         logging.info(f"Scraping reviews for Amazon product ID: {product_id} using Selenium")

#         # Initialize Selenium WebDriver
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         url = f"https://www.amazon.com/product-reviews/{product_id}"
#         driver.get(url)

#         # Allow time for the page to load
#         time.sleep(3)

#         # Locate the reviews container
#         reviews_container = driver.find_element(By.ID, "cm_cr-review_list")
#         if not reviews_container:
#             logging.warning("No reviews container found.")
#             return []

#         # Locate individual review blocks
#         review_blocks = reviews_container.find_elements(By.CSS_SELECTOR, "li.review.aok-relative[data-hook='review']")
#         if not review_blocks:
#             logging.warning("No reviews found on this page.")
#             return []

#         # Extract review text
#         reviews = []
#         for block in review_blocks:
#             try:
#                 # Locate review text
#                 review_text = block.find_element(By.CSS_SELECTOR, "span.a-size-base.review-text.review-text-content[data-hook='review-body']")
#                 reviews.append(review_text.text.strip())
#             except Exception as e:
#                 logging.warning(f"Failed to extract review text: {e}")
#                 continue

#         logging.info(f"Total reviews scraped: {len(reviews)}")
#         return reviews

#     except Exception as e:
#         logging.error(f"Error scraping reviews with Selenium: {e}")
#         return []

#     finally:
#         driver.quit()



# def scrape_reviews(product_id, username=None, password=None):
#     """
#     Scrape reviews from the first page of Amazon reviews for the given product ID.
#     If login is required, automate the login process.

#     Args:
#         product_id (str): Amazon product ID to scrape reviews for.
#         username (str): Amazon username/email (optional, required for login).
#         password (str): Amazon password (optional, required for login).

#     Returns:
#         list: A list of extracted reviews.
#     """
#     try:
#         logging.info(f"Scraping reviews for Amazon product ID: {product_id}")

#         # Initialize Selenium WebDriver with options
#         options = Options()
#         options.add_argument("start-maximized")
#         options.add_argument(
#             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#         )
#         driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()), options=options
#         )

#         # Open the Amazon product reviews page
#         url = f"https://www.amazon.com/product-reviews/{product_id}"
#         driver.get(url)

#         # Handle login if username and password are provided
#         if username and password:
#             try:
#                 logging.info("Attempting to log in to Amazon...")
#                 username_input = WebDriverWait(driver, 60).until(
#                     EC.presence_of_element_located((By.ID, "ap_email"))
#                 )
#                 password_input = driver.find_element(By.ID, "ap_password")
#                 submit_button = driver.find_element(By.ID, "signInSubmit")

#                 username_input.send_keys(username)
#                 password_input.send_keys(password)
#                 submit_button.click()

#                 # Wait for redirection to the reviews page
#                 WebDriverWait(driver, 60).until(
#                     EC.presence_of_element_located((By.ID, "cm_cr-review_list"))
#                 )
#                 logging.info("Login successful.")
#             except Exception as e:
#                 logging.error(f"Login failed: {e}")

#         # Wait for the reviews container to load
#         try:
#             reviews_container = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.ID, "cm_cr-review_list"))
#             )
#         except Exception as e:
#             logging.error(f"Error waiting for reviews container: {e}")
#             return []

#         # Locate individual review blocks within the container
#         review_blocks = reviews_container.find_elements(
#             By.CSS_SELECTOR, "li.review.aok-relative[data-hook='review']"
#         )
#         if not review_blocks:
#             logging.warning("No reviews found on this page.")
#             return []

#         # Extract review text
#         reviews = []
#         for block in review_blocks:
#             try:
#                 review_text = block.find_element(
#                     By.CSS_SELECTOR,
#                     "span.a-size-base.review-text.review-text-content[data-hook='review-body']",
#                 )
#                 reviews.append(review_text.text.strip())
#             except Exception as e:
#                 logging.warning(f"Failed to extract review text: {e}")
#                 continue

#         logging.info(f"Total reviews scraped: {len(reviews)}")
#         return reviews

#     except Exception as e:
#         logging.error(f"Error during scraping: {e}")
#         return []

#     finally:
#         driver.quit()

def scrape_reviews(product_id):
    """
    Scrape reviews from Amazon with manual login support.
    """
    try:
        # Initialize Selenium WebDriver
        options = Options()
        options.add_argument("start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the Amazon product reviews page
        url = f"https://www.amazon.com/product-reviews/{product_id}"
        driver.get(url)

        # Pause for manual input of username and password
        input("Please log in manually in the browser, then press Enter to continue...")

        # Locate the reviews container after login
        reviews_container = driver.find_element(By.ID, "cm_cr-review_list")
        review_blocks = reviews_container.find_elements(By.CSS_SELECTOR, "li.review.aok-relative[data-hook='review']")

        reviews = []
        for block in review_blocks:
            review_text = block.find_element(By.CSS_SELECTOR, "span.a-size-base.review-text.review-text-content[data-hook='review-body']")
            reviews.append(review_text.text.strip())

        return reviews

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        driver.quit()






def get_gpt_response(prompt):
    """
    Send user feedback to OpenAI GPT model and return actionable analysis.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the model
            messages=[
                {"role": "system", "content": "You are an AI feedback analyst. Your task is to analyze user feedback and provide concise, actionable insights. Clearly state the sentiment (positive, negative, or mixed) and summarize the key themes in the feedback."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract and return the response content
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        return f"Error: {e}"

# Define the API endpoint
# @app.route("/analyze", methods=["POST"])
# def analyze_feedback():
#     """
#     API endpoint to receive user feedback, process it using GPT, and return the response.
#     """
#     try:
#         data = request.get_json()
#         user_input = data.get("text", "")  # Extract 'text' field from JSON payload

#         if not user_input:
#             return jsonify({"error": "No input provided. Please provide valid feedback."}), 400

#         # Get GPT response
#         gpt_response = get_gpt_response(user_input)
#         return jsonify({"response": gpt_response})  # Return the response as JSON

#     except Exception as e:
#         return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
@app.route("/analyze", methods=["POST"])
def analyze_feedback():
    """
    API endpoint to receive user feedback or custom prompts, process them using GPT, and return the response.
    """
    try:
        data = request.get_json()
        user_input = data.get("text", "")  # Extract 'text' field from JSON payload

        if not user_input:
            return jsonify({"error": "No input provided. Please provide valid feedback."}), 400

        # Get GPT response
        gpt_response = get_gpt_response(user_input)
        return jsonify({"response": gpt_response})  # Return the response as JSON

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Define the API endpoint for scraping and analyzing reviews
# @app.route("/scrape_reviews", methods=["POST"])
# def scrape_and_analyze():
#     """
#     API endpoint to scrape product reviews by product ID, analyze them, and return insights.
#     """
#     try:
#         data = request.get_json()
#         product_id = data.get("product_id", "")

#         if not product_id:
#             return jsonify({"error": "No product ID provided. Please provide a valid product ID."}), 400

#         reviews = scrape_reviews(product_id)

#         if not reviews:
#             return jsonify({"error": "No reviews found for the given product ID."}), 404

#         # Combine reviews for GPT analysis
#         combined_reviews = "\n".join(reviews)
#         gpt_response = get_gpt_response(combined_reviews)

#         return jsonify({
#             "product_id": product_id,
#             "review_count": len(reviews),
#             "response": gpt_response
#         })

#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": f"Failed to fetch reviews: {e}"}), 500
#     except Exception as e:
#         return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
@app.route("/scrape_reviews", methods=["POST"])
def scrape_and_analyze():
    """
    API endpoint to scrape Amazon reviews by product ID, analyze each review, and return detailed insights.
    """
    try:
        data = request.get_json()
        product_id = data.get("product_id", "")

        if not product_id:
            logging.error("No product ID provided.")
            return jsonify({"error": "No product ID provided. Please provide a valid product ID."}), 400

        # Scrape reviews for the given product ID
        reviews = scrape_reviews(product_id)

        if isinstance(reviews, str) and reviews.startswith("Error"):
            logging.error(f"Scraping error: {reviews}")
            return jsonify({"error": reviews}), 500

        if not reviews:
            logging.warning("No reviews found.")
            return jsonify({"error": "No reviews found for the given product ID."}), 404

        # Analyze each review
        analyzed_reviews = []
        for review in reviews:
            try:
                analysis = get_gpt_response(review)
                analyzed_reviews.append({
                    "review": review,
                    "analysis": analysis
                })
            except Exception as e:
               logging.error(f"GPT analysis failed for review: {review}")
               analyzed_reviews.append({
                    "review": review,
                    "analysis": f"Error analyzing review: {str(e)}"
                })


        return jsonify({
            "product_id": product_id,
            "review_count": len(reviews),
            "analyzed_reviews": analyzed_reviews
        })

    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500



# Start the Flask server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

