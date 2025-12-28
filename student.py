import streamlit as st
from notices import notices_page
from resources import resources_page
from complaints_student import complaints_student_page
from feedback_student import feedback_student_page
from club_utils import is_club_member
from add_club_event import add_club_event_page

def student_dashboard():

    # 🔐 Role protection
    if st.session_state.get("role") != "student":
        st.error("Unauthorized access")
        st.stop()

    st.sidebar.title("🎓 Student Menu")

    menu = [
    "Notices",
    "Resources",
    "Raise Complaint",
    "My Complaints",
    "Feedback"
    ]

    # 👇 ONLY club members see this option
    if is_club_member(st.session_state.user_id):
        menu.append("Add Club Event")

    page = st.sidebar.radio("Go to", menu)


    if page == "Notices":
        notices_page()

    elif page == "Resources":
        resources_page()

    elif page == "Raise Complaint":
        complaints_student_page(view_only=False)

    elif page == "My Complaints":
        complaints_student_page(view_only=True)

    elif page == "Feedback":
        feedback_student_page()
    
    elif page == "Add Club Event":
        add_club_event_page()

