import openai
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load API key from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

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

