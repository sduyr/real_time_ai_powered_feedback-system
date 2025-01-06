import streamlit as st

def display_feedback(response):
    """
    Display feedback analysis results in Streamlit.
    """
    st.subheader("AI Analysis Result")
    if "error" in response:
        st.error(f"Error: {response['error']}")
    else:
        st.success("### Analysis:")
        st.write(response.get("response", "No analysis available."))
