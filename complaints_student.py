import streamlit as st
from db import get_connection
from gemini_helper import analyze_complaint
import pandas as pd

def complaints_student_page(view_only=False):
    
    # Custom styling
    st.markdown("""
    <style>
    .complaints-student-header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
    }
    
    .complaints-student-subtitle {
        font-size: 16px;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 30px;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stTextArea label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 10px !important;
    }
    
    /* Submit button */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 32px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Table styling */
    [data-testid="stDataFrame"] {
        background: white;
        border-radius: 12px;
        overflow: hidden;
    }
    
    [data-testid="stDataFrame"] thead tr th {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 12px !important;
        border: none !important;
    }
    
    [data-testid="stDataFrame"] tbody tr {
        background: #ffffff !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }
    
    [data-testid="stDataFrame"] tbody tr:hover {
        background: #f8fafc !important;
    }
    
    [data-testid="stDataFrame"] tbody tr td {
        color: #0f172a !important;
        padding: 12px !important;
    }
    
    [data-testid="stDataFrame"] tbody tr:nth-child(even) {
        background: #f8fafc !important;
    }
    
    /* Info card */
    .complaint-info-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 18px 22px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.1);
    }
    
    .complaint-info-text {
        color: #92400e;
        font-size: 14px;
        font-weight: 500;
        margin: 0;
    }
    
    /* AI Processing card */
    .ai-processing-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid #22c55e;
        padding: 18px 22px;
        border-radius: 12px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.1);
    }
    
    .ai-processing-text {
        color: #15803d;
        font-size: 14px;
        font-weight: 600;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- PAGE HEADER ----------
    if view_only:
        st.markdown('<div class="complaints-student-header">📌 My Complaints</div>', unsafe_allow_html=True)
        st.markdown('<div class="complaints-student-subtitle">Track status of your submitted complaints</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="complaints-student-header">📝 Raise a Complaint</div>', unsafe_allow_html=True)
        st.markdown('<div class="complaints-student-subtitle">Describe your issue clearly for faster resolution</div>', unsafe_allow_html=True)

    conn = get_connection()
    cursor = conn.cursor

    # ---------- VIEW COMPLAINTS ----------
    if view_only:
        cursor.execute("""
            SELECT 
                complaint_text AS Complaint,
                category AS Category,
                urgency AS Urgency,
                status AS Status,
                created_at AS Date
            FROM complaints
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (st.session_state.user_id,))

        data = cursor.fetchall()
        conn.close()

        if not data:
            st.info("📋 You have not submitted any complaints yet.")
            return

        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%d %b %Y")

        # Add status badge styling
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <span style="background: #22c55e; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; margin-right: 8px;">✓ RESOLVED</span>
            <span style="background: #3b82f6; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; margin-right: 8px;">⚡ IN PROGRESS</span>
            <span style="background: #64748b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">⏳ NEW</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        return

    # ---------- SUBMIT COMPLAINT ----------
    
    # Info card
    st.markdown("""
    <div class="complaint-info-card">
        <p class="complaint-info-text">
            🤖 <strong>AI-Powered Analysis:</strong> Our system will automatically categorize your complaint and assign urgency level for faster resolution.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    complaint_text = st.text_area(
        "Complaint Description",
        height=180,
        placeholder="Describe your issue in detail...\n\nExample: Wi-Fi is not working properly in Hostel Block B. The connection keeps dropping every 10 minutes."
    )

    if st.button("🚀 Submit Complaint", use_container_width=True):
        if not complaint_text.strip():
            st.error("⚠️ Complaint description cannot be empty")
        else:
            with st.spinner("🤖 AI is analyzing your complaint..."):
                try:
                    ai = analyze_complaint(complaint_text)
                    
                    # Show AI analysis result
                    st.markdown(f"""
                    <div class="ai-processing-card">
                        <p class="ai-processing-text">
                            ✓ AI Analysis Complete:<br>
                            📁 Category: <strong>{ai["category"]}</strong> | 
                            📍 Area: <strong>{ai["area"]}</strong> | 
                            🚨 Urgency: <strong>{ai["urgency"].upper()}</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    cursor.execute("""
                        INSERT INTO complaints
                        (user_id, complaint_text, category, area, urgency, status)
                        VALUES (%s,%s,%s,%s,%s,'new')
                    """, (
                        st.session_state.user_id,
                        complaint_text,
                        ai["category"],
                        ai["area"],
                        ai["urgency"]
                    ))

                    conn.commit()
                    conn.close()

                    st.success("✅ Complaint submitted successfully! You can track its status in 'My Complaints' section.")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error submitting complaint: {str(e)}")
                    conn.close()