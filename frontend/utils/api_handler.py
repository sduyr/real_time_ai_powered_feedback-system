# import requests

# def get_analysis_from_api(user_feedback, backend_url="http://127.0.0.1:5000/analyze"):
#     try:
#         response = requests.post(backend_url, json={"text": user_feedback})
#         return response.json()
#     except Exception as e:
#         return {"error": f"Failed to connect to backend: {e}"}

import requests

def get_analysis_from_api(user_feedback, backend_url="http://127.0.0.1:5000/analyze"):
    """
    Send user feedback to the backend API for analysis.
    
    Args:
        user_feedback (str): The feedback text to analyze.
        backend_url (str): The URL of the backend API endpoint for analysis.

    Returns:
        dict: The JSON response from the backend API.
    """
    try:
        response = requests.post(backend_url, json={"text": user_feedback})
        response.raise_for_status()  # Raise an error if the request fails
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to backend: {str(e)}"}

def get_reviews_analysis_from_api(product_id, backend_url="http://127.0.0.1:5000/scrape_reviews"):
    """
    Send product ID to the backend API to scrape and analyze reviews.
    
    Args:
        product_id (str): The ID of the product to scrape reviews for.
        backend_url (str): The URL of the backend API endpoint for scraping and analysis.

    Returns:
        dict: The JSON response from the backend API.
    """
    try:
        response = requests.post(backend_url, json={"product_id": product_id})
        response.raise_for_status()  # Raise an error if the request fails
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to backend: {str(e)}"}

