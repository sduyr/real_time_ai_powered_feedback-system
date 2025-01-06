# import streamlit as st
# from components.input_form import input_form
# from components.feedback_display import display_feedback
# from utils.api_handler import get_analysis_from_api

# # Load logo
# st.image("assets/logo.png", width=150)
# st.title("Real-Time AI Feedback System")

# # Input form
# user_feedback = input_form()

# # Process feedback
# if st.button("Analyze Feedback"):
#     if user_feedback:
#         response = get_analysis_from_api(user_feedback)
#         display_feedback(response)
#     else:
#         st.warning("Please enter some feedback.")

import streamlit as st
from components.input_form import input_form
from components.feedback_display import display_feedback
from utils.api_handler import get_analysis_from_api 
from utils.api_handler import get_reviews_analysis_from_api

# Load logo
st.image("assets/logo.png", width=150)
st.title("Real-Time AI Feedback System")

# Tabbed interface for feedback analysis and product review analysis
tab1, tab2 = st.tabs(["Analyze Feedback", "Scrape and Analyze Reviews"])

# Tab 1: Analyze user-provided feedback
with tab1:
    user_feedback = input_form()  # User input form for feedback
    if st.button("Analyze Feedback"):
        if user_feedback:
            response = get_analysis_from_api(user_feedback)
            display_feedback(response)
        else:
            st.warning("Please enter some feedback.")

# Tab 2: Scrape and analyze product reviews
with tab2:
    st.subheader("Scrape and Analyze Product Reviews")
    product_id = st.text_input("Enter Product ID:")
    if st.button("Scrape and Analyze"):
        if product_id:
            response = get_reviews_analysis_from_api(product_id)
            if "error" in response:
                st.error(response["error"])
            else:
                st.write(f"**Product ID:** {response['product_id']}")
                st.write(f"**Number of Reviews Analyzed:** {response['review_count']}")
                st.success("### AI Analysis Result:")
                # st.write(response["response"])
                st.write(response)

        else:
            st.warning("Please enter a valid Product ID.")

