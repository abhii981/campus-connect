import streamlit as st
from notices import notices_page
from resources import resources_page
from add_resource import add_resource_page
from add_notice import add_notice_page
from complaints_admin import admin_complaints_page
from feedback_admin import feedback_admin_page
import os
from db import get_connection

def admin_dashboard():

    # 🔐 Role protection
    if st.session_state.get("role") != "admin":
        st.error("Unauthorized access")
        st.stop()

    st.sidebar.title("🧑‍💼 Admin Menu")
    page = st.sidebar.radio(
        "Go to",
        ["Notices","Add Notice", "Resources", "Add Resource/Study Material","Complaints","Feedback"]
    )

    if page == "Notices":
        notices_page()

    elif page == "Resources":
        resources_page()

    elif page == "Add Resource/Study Material":
        add_resource_page()
    
    elif page=="Add Notice":
        add_notice_page()
    
    elif page=="Complaints":
        admin_complaints_page()

    elif page=="Feedback":
        feedback_admin_page()


