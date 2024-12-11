import streamlit as st


def menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("chat.py", label="Chat")
    st.sidebar.page_link("pages/calendar.py", label="Calendar")
