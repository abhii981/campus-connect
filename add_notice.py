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
    
    /* Success/Error messages - ensure visibility */
    .stSuccess, .stError, .stWarning, .stInfo {
        color: #0f172a !important;
    }
    
    /* Form submit button */
    button[type="submit"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 32px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    button[type="submit"]:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
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
            help="Upload a PDF document (max 16MB)"
        )

        submit = st.form_submit_button("📤 Publish Notice", use_container_width=True)

        if submit:
            if not title.strip():
                st.error("⚠️ Notice title is required")
            elif not description.strip():
                st.error("⚠️ Notice description is required")
            else:
                try:
                    file_bytes = None
                    file_name = None

                    if uploaded_file:
                        file_bytes = uploaded_file.read()
                        file_name = uploaded_file.name
                        
                        # Check file size (16MB limit for PostgreSQL)
                        if len(file_bytes) > 16 * 1024 * 1024:
                            st.error("⚠️ File size exceeds 16MB limit. Please upload a smaller file.")
                            return

                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO notices
                        (title, description, file_data, file_name, posted_by, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        title.strip(),
                        description.strip(),
                        psycopg2.Binary(file_bytes) if file_bytes else None,
                        file_name,
                        st.session_state.user_id,
                        datetime.now()
                    ))

                    conn.commit()
                    cursor.close()
                    conn.close()

                    st.success("✅ Notice published successfully!")
                    st.balloons()
                    
                    # Show a helpful message
                    st.info("💡 Your notice is now visible in the Notices section")

                except Exception as e:
                    st.error(f"❌ Error publishing notice: {str(e)}")
                    import traceback
                    with st.expander("View error details"):
                        st.code(traceback.format_exc())
    
    # ---------- RECENT NOTICES ----------
    st.markdown("---")
    st.markdown("### 📋 Recent Notices")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT title, created_at, file_name
            FROM notices
            ORDER BY created_at DESC
            LIMIT 5
        """)
        
        recent_notices = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if recent_notices:
            for idx, notice in enumerate(recent_notices, 1):
                title_text = notice[0]
                created_at = notice[1]
                has_file = notice[2] is not None
                
                try:
                    if isinstance(created_at, str):
                        date_str = created_at
                    else:
                        date_str = created_at.strftime("%d %b %Y, %I:%M %p")
                except:
                    date_str = "Unknown date"
                
                file_icon = "📎" if has_file else "📄"
                
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