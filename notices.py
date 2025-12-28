import streamlit as st
import os
import base64
from datetime import datetime, timedelta
from db import get_connection
import pandas as pd

def notices_page():
    
    # Custom styling
    st.markdown("""
    <style>
    .notices-breadcrumb {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 8px;
    }
    .notices-breadcrumb span {
        color: #3b82f6;
        font-weight: 600;
    }
    
    .notices-header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    
    .notices-subheader {
        font-size: 18px;
        color: #3b82f6;
        font-weight: 600;
        margin-bottom: 30px;
    }
    
    /* Section headers */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
        margin-top: 10px;
    }
    
    .section-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 20px;
    }
    
    .notices-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .notices-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
        border-color: #3b82f6;
    }
    
    .notices-badge {
        font-size: 13px;
        background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
        color: #1e40af;
        padding: 5px 12px;
        border-radius: 16px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        margin-bottom: 12px;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(30, 64, 175, 0.1);
    }
    
    .notices-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 10px;
    }
    
    .notices-desc {
        font-size: 14px;
        color: #475569;
        margin-bottom: 14px;
        line-height: 1.6;
    }
    
    /* View button */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 8px 20px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        color: white !important;
        border: none !important;
        padding: 8px 20px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4) !important;
    }
    
    /* PDF iframe */
    iframe {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-top: 16px;
    }
    
    /* New notice indicator */
    .new-indicator {
        background: #22c55e;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        margin-left: 8px;
        text-transform: uppercase;
    }
    
    /* Club event card */
    .club-event-card {
        background: linear-gradient(135deg, #ffffff 0%, #faf5ff 100%);
        border: 1px solid #e9d5ff;
        border-left: 5px solid #a855f7;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(168, 85, 247, 0.1);
    }

    .club-event-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(168, 85, 247, 0.15);
        border-color: #a855f7;
    }

    .club-event-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }

    .club-event-desc {
        font-size: 14px;
        color: #475569;
        margin-bottom: 10px;
        line-height: 1.6;
    }

    .club-event-meta {
        font-size: 13px;
        color: #6b21a8;
        font-weight: 600;
    }
    
    .club-event-badge {
        font-size: 13px;
        background: linear-gradient(135deg, #f3e8ff 0%, #fae8ff 100%);
        color: #7e22ce;
        padding: 5px 12px;
        border-radius: 16px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        margin-bottom: 10px;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(126, 34, 206, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("<div class='notices-breadcrumb'>Home <span>/ Notices</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='notices-header'>🎓 Campus Connect</div>", unsafe_allow_html=True)
    st.markdown("<div class='notices-subheader'>Official campus notices & academic updates</div>", unsafe_allow_html=True)

    # Add a visual separator/divider
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <div style="display: inline-block; padding: 10px 30px; background: linear-gradient(135deg, #3b82f6 0%, #a855f7 100%); 
                    border-radius: 50px; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);">
            <span style="color: white; font-weight: 700; font-size: 14px; letter-spacing: 1px;">
                📢 OFFICIAL NOTICES &nbsp;&nbsp; | &nbsp;&nbsp; 🎉 CLUB EVENTS
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Two column layout with visual separator
    left_col, separator, right_col = st.columns([10, 0.5, 10], gap="medium")
    
    # ==================== LEFT COLUMN: OFFICIAL NOTICES ====================
    with left_col:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                    padding: 12px 20px; border-radius: 12px 12px 0 0; margin-bottom: -10px;">
            <div class='section-title' style="color: white; margin: 0;">📢 Official Notices</div>
        </div>
        <div style="background: #eff6ff; padding: 8px 20px; border-radius: 0 0 12px 12px; margin-bottom: 20px;">
            <div class='section-subtitle' style="margin: 0; color: #1e40af;">Campus-wide announcements and updates</div>
        </div>
        """, unsafe_allow_html=True)
        
        conn = get_connection()
        cursor = conn.cursor

        cursor.execute("""
            SELECT title, description, notice_url, created_at
            FROM notices
            ORDER BY created_at DESC
        """)
        notices = cursor.fetchall()
        cursor.close()
        conn.close()

        if not notices:
            st.info("📭 No notices available yet.")
        else:
            # Display notice count
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%); 
                        padding: 10px 16px; 
                        border-radius: 10px; 
                        margin-bottom: 18px;
                        border-left: 4px solid #3b82f6;">
                <span style="color: #1e40af; font-weight: 600; font-size: 13px;">
                    📊 Total: <strong>{len(notices)}</strong> notices
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            for idx, n in enumerate(notices):
                with st.container():
                    st.markdown("<div class='notices-card'>", unsafe_allow_html=True)

                    # Check if notice is new (within last 7 days)
                    is_new = False
                    if n["created_at"]:
                        date_str = n['created_at'].strftime('%d %b %Y')
                        days_old = (datetime.now() - n["created_at"]).days
                        is_new = days_old <= 7
                        
                        new_badge = "<span class='new-indicator'>New</span>" if is_new else ""
                        
                        st.markdown(
                            f"<div class='notices-badge'>📅 {date_str}{new_badge}</div>",
                            unsafe_allow_html=True
                        )

                    st.markdown(f"<div class='notices-title'>{n['title']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='notices-desc'>{n['description']}</div>", unsafe_allow_html=True)

                    file_path = n["notice_url"]
                    if file_path and os.path.exists(file_path):
                        if st.button("📄 View Notice", key=f"notice_{idx}", use_container_width=True):
                            with open(file_path, "rb") as f:
                                pdf_bytes = f.read()
                                base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

                            st.markdown(
                                f"""
                                <iframe src="data:application/pdf;base64,{base64_pdf}"
                                width="100%" height="400px" style="border:none;"></iframe>
                                """,
                                unsafe_allow_html=True
                            )
                        
                        # Download button
                        with open(file_path, "rb") as f:
                            st.download_button(
                                "⬇️ Download",
                                data=f.read(),
                                file_name=os.path.basename(file_path),
                                mime="application/pdf",
                                key=f"download_notice_{idx}",
                                use_container_width=True
                            )
                    else:
                        st.warning("⚠️ File not found")

                    st.markdown("</div>", unsafe_allow_html=True)
    
    # ==================== SEPARATOR ====================
    with separator:
        st.markdown("""
        <div style="width: 2px; 
                    background: linear-gradient(to bottom, #3b82f6, #a855f7); 
                    height: 100%; 
                    min-height: 500px; 
                    border-radius: 2px;
                    box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);">
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== RIGHT COLUMN: CLUB EVENTS ====================
    with right_col:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%); 
                    padding: 12px 20px; border-radius: 12px 12px 0 0; margin-bottom: -10px;">
            <div class='section-title' style="color: white; margin: 0;">🎉 Societies & Clubs Events</div>
        </div>
        <div style="background: #faf5ff; padding: 8px 20px; border-radius: 0 0 12px 12px; margin-bottom: 20px;">
            <div class='section-subtitle' style="margin: 0; color: #7e22ce;">Campus activities and events</div>
        </div>
        """, unsafe_allow_html=True)
        
        conn = get_connection()
        
        try:
            events_df = pd.read_sql("""
                SELECT title, description, event_date, venue
                FROM club_events
                ORDER BY event_date ASC
            """, conn)
            conn.close()
        except Exception as e:
            conn.close()
            st.error(f"Error loading events: {str(e)}")
            events_df = pd.DataFrame()

        if events_df.empty:
            st.info("🎭 No club events announced yet.")
        else:
            # Display event count
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f3e8ff 0%, #fae8ff 100%); 
                        padding: 10px 16px; 
                        border-radius: 10px; 
                        margin-bottom: 18px;
                        border-left: 4px solid #a855f7;">
                <span style="color: #7e22ce; font-weight: 600; font-size: 13px;">
                    🎪 Total: <strong>{len(events_df)}</strong> events
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            for _, row in events_df.iterrows():
                # Format date
                try:
                    if isinstance(row['event_date'], str):
                        event_date_formatted = row['event_date']
                    else:
                        event_date_formatted = row['event_date'].strftime('%d %b %Y')
                except:
                    event_date_formatted = str(row['event_date'])
                
                st.markdown(f"""
                <div class="club-event-card">
                    <div class="club-event-badge">🎯 Upcoming Event</div>
                    <div class="club-event-title">{row['title']}</div>
                    <div class="club-event-desc">
                        {row['description']}
                    </div>
                    <div class="club-event-meta">
                        📍 {row['venue']} &nbsp;&nbsp;•&nbsp;&nbsp; 📅 {event_date_formatted}
                    </div>
                </div>
                """, unsafe_allow_html=True)