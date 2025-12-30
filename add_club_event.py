import streamlit as st
from db import get_connection

def add_club_event_page():

    # Show current user info for debugging
    st.info(f"🔍 Debug: Logged in as User ID: {st.session_state.user_id} | Name: {st.session_state.name}")

    # 🔐 Security check - verify user is in club_users table
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT club_id, role_club 
            FROM club_users 
            WHERE user_id = %s
        """, (st.session_state.user_id,))
        
        result = cursor.fetchone()
        
        if not result:
            cursor.close()
            conn.close()
            
            st.error("🚫 Unauthorized access - This page is only accessible to club members")
            st.warning(f"❗ User ID {st.session_state.user_id} is not registered in any club")
            st.info("💡 Contact admin to add you to a club or use a club member account (User ID 2 or 5)")
            
            # Show who IS in clubs
            conn2 = get_connection()
            cursor2 = conn2.cursor()
            cursor2.execute("SELECT user_id, club_id, role_club FROM club_users")
            club_members = cursor2.fetchall()
            cursor2.close()
            conn2.close()
            
            if club_members:
                st.markdown("**Current club members:**")
                for member in club_members:
                    st.write(f"- User ID: {member[0]}, Club ID: {member[1]}, Role: {member[2]}")
            
            st.stop()
        
        # Store club info
        user_club_id = result[0]
        user_club_role = result[1]
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        st.error(f"❌ Database error: {str(e)}")
        import traceback
        with st.expander("Technical details"):
            st.code(traceback.format_exc())
        st.stop()

    # Custom styling
    st.markdown("""
    <style>
    .club-event-header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
    }
    
    .club-event-subtitle {
        font-size: 16px;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 30px;
    }
    
    /* Form inputs */
    .stTextInput input, .stTextArea textarea, .stDateInput input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        border: 2px solid #e9d5ff !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stDateInput input:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.1) !important;
    }
    
    .stTextInput label, .stTextArea label, .stDateInput label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
    }
    
    /* Submit button */
    .stButton > button {
        background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 32px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #9333ea 0%, #7e22ce 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4) !important;
    }
    
    /* Info card */
    .club-info-card {
        background: linear-gradient(135deg, #f3e8ff 0%, #fae8ff 100%);
        border-left: 4px solid #a855f7;
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 2px 8px rgba(168, 85, 247, 0.1);
    }
    
    .club-info-title {
        color: #6b21a8;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .club-info-text {
        color: #7e22ce;
        font-size: 14px;
        font-weight: 500;
        line-height: 1.6;
    }
    
    /* Form container */
    .form-container {
        background: white;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f3e8ff;
    }
    
    /* Form submit button */
    button[type="submit"] {
        background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 32px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    button[type="submit"]:hover {
        background: linear-gradient(135deg, #9333ea 0%, #7e22ce 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<div class="club-event-header">🎉 Add Club / Society Event</div>', unsafe_allow_html=True)
    st.markdown('<div class="club-event-subtitle">Share your upcoming events with the campus community</div>', unsafe_allow_html=True)

    # Info card
    st.markdown(f"""
    <div class="club-info-card">
        <div class="club-info-title">🎯 Club Member Access</div>
        <div class="club-info-text">
            You are logged in as <strong>{user_club_role}</strong> (Club ID: {user_club_id}). 
            Your event will be visible to all students on the Notices page once published.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Form in a styled container
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    with st.form("add_club_event_form", clear_on_submit=True):
        st.markdown(
            "<h3 style='color:#0f172a; font-weight:700;'>📝 Event Details</h3>",
            unsafe_allow_html=True
        )

        title = st.text_input(
            "Event Title",
            placeholder="e.g., Annual Cultural Fest 2025"
        )
        
        description = st.text_area(
            "Event Description",
            height=150,
            placeholder="Provide a detailed description of your event..."
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            event_date = st.date_input("Event Date")
        
        with col2:
            venue = st.text_input(
                "Venue",
                placeholder="e.g., Main Auditorium"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("🚀 Publish Event", use_container_width=True)

        if submit:
            if not title.strip() or not description.strip() or not venue.strip():
                st.error("⚠️ All fields are required")
            else:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()

                    # Insert with USER_ID as created_by (as requested)
                    cursor.execute("""
                        INSERT INTO club_events
                        (title, description, event_date, venue, created_by)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        title.strip(),
                        description.strip(),
                        event_date,
                        venue.strip(),
                        st.session_state.user_id  # Using user_id as you requested
                    ))

                    conn.commit()
                    cursor.close()
                    conn.close()

                    st.success("🎉 Event published successfully!")
                    st.balloons()
                    st.info(f"Event created by User ID: {st.session_state.user_id}")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    import traceback
                    with st.expander("Debug"):
                        st.code(traceback.format_exc())
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")

    st.markdown("""
<div style="background:#ffffff; border:1px solid #e9d5ff; border-radius:16px; padding:24px; box-shadow:0 4px 20px rgba(0,0,0,0.06);">
<h3 style="color:#0f172a; font-weight:800; margin-bottom:20px;">💡 Tips for Creating Great Event Posts</h3>
<div style="display:flex; gap:24px; flex-wrap:wrap;">

<div style="flex:1; min-width:220px;">
<h4 style="color:#6b21a8; font-weight:700;">📝 Be Descriptive</h4>
<ul style="color:#0f172a; font-size:14px; line-height:1.6;">
<li>Include all key details</li>
<li>Mention special guests</li>
<li>Highlight unique features</li>
</ul>
</div>

<div style="flex:1; min-width:220px;">
<h4 style="color:#6b21a8; font-weight:700;">📅 Plan Ahead</h4>
<ul style="color:#0f172a; font-size:14px; line-height:1.6;">
<li>Post at least 1 week early</li>
<li>Choose convenient timings</li>
<li>Book venues in advance</li>
</ul>
</div>

<div style="flex:1; min-width:220px;">
<h4 style="color:#6b21a8; font-weight:700;">🎯 Engage Students</h4>
<ul style="color:#0f172a; font-size:14px; line-height:1.6;">
<li>Make it exciting</li>
<li>Offer incentives</li>
<li>Create buzz</li>
</ul>
</div>

</div>
</div>
""", unsafe_allow_html=True)