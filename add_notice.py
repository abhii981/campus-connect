import streamlit as st
from db import get_connection
from datetime import datetime
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    
    .stSuccess, .stError, .stWarning, .stInfo {
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
    with st.form("add_notice_form", clear_on_submit=True):

        title = st.text_input("Notice Title", placeholder="Enter notice title...")
        description = st.text_area(
            "Notice Description",
            height=120,
            placeholder="Enter notice details here..."
        )

        uploaded_file = st.file_uploader(
            "Attach PDF (optional)",
            type=["pdf"],
            help="Upload a PDF document"
        )

        submit = st.form_submit_button("📤 Publish Notice", use_container_width=True)

        if submit:
            if not title.strip():
                st.error("⚠️ Notice title is required")
                return
            if not description.strip():
                st.error("⚠️ Notice description is required")
                return

            try:
                notice_url = None

                if uploaded_file:
                    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    notice_url = file_path

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO notices
                    (title, description, notice_url, posted_by, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    title.strip(),
                    description.strip(),
                    notice_url,
                    st.session_state.user_id,
                    datetime.now()
                ))

                conn.commit()
                cursor.close()
                conn.close()

                st.success("✅ Notice published successfully!")
                st.balloons()
                st.info("💡 Your notice is now visible in the Notices section")

            except Exception as e:
                st.error(f"❌ Error publishing notice: {str(e)}")

    # ---------- RECENT NOTICES ----------
    st.markdown("---")
    st.markdown("### 📋 Recent Notices")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, created_at, notice_url
            FROM notices
            ORDER BY created_at DESC
            LIMIT 5
        """)

        recent_notices = cursor.fetchall()
        cursor.close()
        conn.close()

        if recent_notices:
            for title_text, created_at, notice_url in recent_notices:
                try:
                    date_str = created_at.strftime("%d %b %Y, %I:%M %p")
                except:
                    date_str = "Unknown date"

                file_icon = "📎" if notice_url else "📄"

                st.markdown(f"""
                <div style="background: #f8fafc; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #3b82f6;">
                    <div style="color: #0f172a; font-weight: 600;">{file_icon} {title_text}</div>
                    <div style="color: #64748b; font-size: 13px; margin-top: 4px;">📅 {date_str}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No notices published yet")

    except Exception as e:
        st.warning(f"Could not load recent notices: {str(e)}")
