import streamlit as st
import os
import base64
from datetime import datetime, timedelta
from db import get_connection

def add_resource_page():
    # Custom styling for this page
    st.markdown("""
    <style>
    .add-resource-header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
    }
    
    .add-resource-subtitle {
        font-size: 18px;
        color: #3b82f6;
        font-weight: 600;
        margin-bottom: 30px;
    }
    
    /* Force all labels to be dark */
    .stTextInput label,
    .stFileUploader label {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    
    /* Force file uploader text to be dark */
    .stFileUploader section,
    .stFileUploader section * {
        color: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="add-resource-page">', unsafe_allow_html=True)
    
    # Use HTML for headers to ensure dark color
    st.markdown('<div class="add-resource-header">📚 Add Study Resource</div>', unsafe_allow_html=True)
    st.markdown('<div class="add-resource-subtitle">Upload PDF\'s or study material for students</div>', unsafe_allow_html=True)

    with st.form("add_resource_form"):
        title = st.text_input("Resource Title")
        subject = st.text_input("Subject")
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        submit = st.form_submit_button("Upload Resource")

        if submit:
            if not title or not subject or not uploaded_file:
                st.error("⚠️ All fields are required")
            else:
                try:
                    file_path = uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute("""
                                INSERT INTO resources(resource_title, resource_subject, file_url, uploaded_by)
                                VALUES(%s, %s, %s, %s)""",
                                (
                                    title,
                                    subject,
                                    file_path,
                                    st.session_state.user_id
                                ))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    st.success("✅ Resource uploaded successfully")
                except Exception as e:
                    st.error(f"❌ Error uploading resource: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)