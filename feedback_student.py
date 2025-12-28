import streamlit as st
from db import get_connection

def feedback_student_page():
    
    # Custom styling
    st.markdown("""
    <style>
    .feedback-student-header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
    }
    
    .feedback-student-subtitle {
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
    
    /* Info card */
    .feedback-info-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        padding: 18px 22px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
    }
    
    .feedback-info-text {
        color: #1e40af;
        font-size: 14px;
        font-weight: 500;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="feedback-student-header">💬 Submit Feedback</div>', unsafe_allow_html=True)
    st.markdown('<div class="feedback-student-subtitle">Your feedback helps improve campus services</div>', unsafe_allow_html=True)
    
    # Info card
    st.markdown("""
    <div class="feedback-info-card">
        <p class="feedback-info-text">
            💡 <strong>Tip:</strong> Be specific and constructive in your feedback. This helps us understand and address your concerns better.
        </p>
    </div>
    """, unsafe_allow_html=True)

    feedback = st.text_area(
        "Your Feedback",
        height=180,
        placeholder="Share your experience, suggestions or issues...\n\nExample: The library needs more study spaces during exam season."
    )

    if st.button("📨 Submit Feedback", use_container_width=True):
        if not feedback.strip():
            st.error("⚠️ Feedback cannot be empty")
        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO feedback (user_id, feedback_text)
                    VALUES (%s, %s)
                """, (st.session_state.user_id, feedback))

                conn.commit()
                conn.close()

                st.success("✅ Thank you for your feedback! We appreciate your input.")
                
                # Clear the text area by rerunning
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error submitting feedback: {str(e)}")