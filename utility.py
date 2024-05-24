import streamlit as st
import pymysql as ms
from streamlit import session_state
import time
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
# from streamlit_lottie import st_lottie 

def launch_connection():
    # db = ms.connect(host='sql12.freemysqlhosting.net',user='sql12708755',passwd='e5SyF2djWm',database='sql12708755')
    db = ms.connect(host='localhost',user='id22211140_root',passwd='online_croma@P123',database='id22211140_online_croma')
    
    return db

def display_header():
    """Displays a header with cart, wishlist, and logout buttons, considering login status."""

    st.header(st.image("../croma_logo.png"))  # Replace with your app title

    # Display buttons only if user is logged in
    if st.session_state.get("is_logged_in", False):
        col1, col2, col3 = st.columns(3)  # Add a third column

        with col1:
            if st.session_state.get("cart_count", 0) > 0:
                st.button(f" Cart ({st.session_state['cart_count']})")  # Use f-string for dynamic cart count
            else:
                st.button(" Cart")

        with col2:
            if st.session_state.get("wishlist_count", 0) > 0:
                st.button(f"❤️ Wishlist ({st.session_state['wishlist_count']})")
            else:
                st.button("❤️ Wishlist")

        with col3:
            # Logout button with emoji (replace with appropriate emoji code)
            if st.button(" Logout"):
                # Implement logout logic here (e.g., clear session state, redirect to login)
                st.session_state["is_logged_in"] = False  # Placeholder logout logic
                st.success("You have been logged out.")

    else:
        st.error("Please log in to access cart and wishlist features.")
