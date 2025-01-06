import streamlit as st

def input_form():
    st.subheader("Provide Your Feedback")
    feedback = st.text_area("Enter your feedback here:", placeholder="Example: 'The delivery was slow but the product is great.'")
    return feedback

