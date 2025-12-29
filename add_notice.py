import streamlit as st
from db import get_connection
from datetime import datetime
import psycopg2

def add_notice_page():

    # ---------- PAGE-SPECIFIC STYLING ----------
    st.markdown("""
    <style>
    .add-notice-header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
    }

    .add-notice-subtitle {
        font-size: 18px;
        color: #3b82f6;
        font-weight: 600;
        margin-bottom: 30px;
    }

    .stTextInput label,
    .stTextArea label,
    .stFileUploader label {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    .stTextInput input,
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }

    .stFileUploader section,
    .stFileUploader section * {
        color: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- HEADER ----------
    st.markdown('<div class="add-notice-header">📢 Add Notice</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="add-notice-subtitle">Create and publish official campus notices</div>',
        unsafe_allow_html=True
    )

    # ---------- FORM ----------
    with st.form("add_notice_form"):

        title = st.text_input("Notice Title")
        description = st.text_area(
            "Notice Description",
            height=120,
            placeholder="Enter notice details here..."
        )

        uploaded_file = st.file_uploader(
            "Attach PDF (optional)",
            type=["pdf"]
        )

        submit = st.form_submit_button("Publish Notice")

        if submit:
            if not title or not description:
                st.error("⚠️ Title and description are required")
                return

            try:
                file_bytes = None
                file_name = None

                if uploaded_file:
                    file_bytes = uploaded_file.read()
                    file_name = uploaded_file.name

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO notices
                    (title, description, file_data, file_name, posted_by, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    title,
                    description,
                    psycopg2.Binary(file_bytes) if file_bytes else None,
                    file_name,
                    st.session_state.user_id,
                    datetime.now()
                ))

                conn.commit()
                cursor.close()
                conn.close()

                st.success("✅ Notice published successfully")

            except Exception as e:
                st.error(f"❌ Error publishing notice: {str(e)}")
