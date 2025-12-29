import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db import get_connection
from gemini_helper import analyze_feedback_summary
from io import BytesIO
import streamlit.components.v1 as components
import json
from google_sheets_helper import export_to_google_sheets


@st.cache_data(ttl=60)
def load_feedback():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM feedback", conn)
    conn.close()
    return df


def feedback_admin_page():

    # ---------------- PAGE CSS ----------------
    st.markdown("""
    <style>
    .feedback-header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
    }

    .feedback-subtitle {
        font-size: 16px;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 30px;
    }

    .section-header {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* Table styling - matching theme */
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

    /* AI summary card */
    .ai-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 6px solid #3b82f6;
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.1);
        margin-bottom: 24px;
    }

    .ai-title {
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 12px;
    }

    .ai-text {
        font-size: 15px;
        color: #334155;
        line-height: 1.7;
    }
    
    /* Download buttons styling */
    .stDownloadButton > button,
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover,
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- HEADER ----------------
    st.markdown('<div class="feedback-header">💬 Student Feedback Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="feedback-subtitle">Analyze student feedback using AI insights</div>',
        unsafe_allow_html=True
    )

    # ---------------- FETCH DATA ----------------
    try:
        conn = get_connection()
        df = pd.read_sql(
            "SELECT feedback_id, user_id, feedback_text, created_at FROM feedback ORDER BY created_at DESC",
            conn
        )
        conn.close()

        if df.empty:
            st.info("📋 No feedback submitted yet")
            return

        # ---------------- TABLE ----------------
        st.markdown('<div class="section-header">📋 All Feedback</div>', unsafe_allow_html=True)

        display_df = df.copy()
        
        # Convert created_at to datetime with error handling for PostgreSQL
        try:
            display_df["created_at"] = pd.to_datetime(display_df["created_at"], errors='coerce').dt.strftime("%d %b %Y")
        except Exception as e:
            # If conversion fails, keep original format
            st.warning(f"Date formatting issue: {str(e)}")
            pass

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # ---------------- DOWNLOAD BUTTONS ----------------
        st.markdown('<div style="margin-top: 20px; margin-bottom: 30px;">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📊 Download as Google Sheets", use_container_width=True, key="google_sheets_btn"):
                with st.spinner("Exporting to Google Sheets..."):
                    try:
                        sheet_url = export_to_google_sheets(df)
                        st.success("✅ Exported successfully!")
                        st.markdown(f"🔗 [Open Google Sheet]({sheet_url})")
                    except Exception as e:
                        st.error(f"❌ Export failed: {str(e)}")

        with col2:
            st.download_button(
                "📄 Download CSV",
                data=df.to_csv(index=False),
                file_name="feedback.csv",
                mime="text/csv",
                use_container_width=True,
                key="csv_download_btn"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- GEMINI AI SUMMARY ----------------
        st.markdown('<div class="section-header">🧠 AI Feedback Insights</div>', unsafe_allow_html=True)

        combined_feedback = "\n".join(df["feedback_text"].tolist())

        with st.spinner("Analyzing feedback with Gemini AI..."):
            try:
                ai_result = analyze_feedback_summary(combined_feedback)

                st.markdown(f"""
                <div class="ai-card">
                    <div class="ai-title">🤖 AI Summary</div>
                    <div class="ai-text">{ai_result}</div>
                </div>
                """, unsafe_allow_html=True)

                # ---------------- VOICE FEATURE ----------------
                st.markdown('<div class="section-header">🔊 Listen to AI Summary</div>', unsafe_allow_html=True)

                if st.button("▶️ Play Voice Summary", key="voice_btn"):
                    safe_text = json.dumps(ai_result)

                    components.html(
                        f"""
                        <script>
                            const msg = new SpeechSynthesisUtterance({safe_text});
                            msg.rate = 0.95;
                            msg.pitch = 1;
                            msg.volume = 1;

                            window.speechSynthesis.cancel();
                            window.speechSynthesis.speak(msg);
                        </script>
                        """,
                        height=0
                    )
            except Exception as e:
                st.error(f"❌ AI analysis failed: {str(e)}")

        # ---------------- SENTIMENT ANALYSIS (BASIC) ----------------
        st.markdown('<div class="section-header">📊 Feedback Sentiment Overview</div>', unsafe_allow_html=True)

        # Simple keyword-based sentiment (safe + explainable)
        positive_keywords = ["good", "great", "helpful", "useful", "excellent", "nice", "love", "amazing", "wonderful"]
        negative_keywords = ["bad", "poor", "issue", "problem", "slow", "worst", "delay", "terrible", "horrible"]

        def classify_sentiment(text):
            text = str(text).lower()
            if any(word in text for word in positive_keywords):
                return "Positive"
            if any(word in text for word in negative_keywords):
                return "Negative"
            return "Neutral"

        df["sentiment"] = df["feedback_text"].apply(classify_sentiment)
        sentiment_counts = df["sentiment"].value_counts()

        # ---------------- PIE CHART ----------------
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = ["#22c55e", "#ef4444", "#facc15"]
        explode = (0.05, 0.05, 0.05) if len(sentiment_counts) == 3 else tuple([0.05] * len(sentiment_counts))
        
        wedges, texts, autotexts = ax.pie(
            sentiment_counts.values,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(sentiment_counts)],
            explode=explode[:len(sentiment_counts)],
            shadow=True,
            textprops={'fontsize': 12, 'weight': 'bold', 'color': '#0f172a'}
        )
        
        # Make percentage text white for better visibility
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_weight('bold')
        
        ax.set_title("Feedback Sentiment Distribution", fontsize=18, color="#0f172a", weight='bold', pad=20)
        fig.patch.set_facecolor("white")
        
        st.pyplot(fig)
        
        # ---------------- SENTIMENT STATS ----------------
        st.markdown("**Sentiment Statistics:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            positive_count = sentiment_counts.get("Positive", 0)
            st.metric("😊 Positive", f"{positive_count}", f"{(positive_count/len(df)*100):.1f}%")
        
        with col2:
            negative_count = sentiment_counts.get("Negative", 0)
            st.metric("😞 Negative", f"{negative_count}", f"{(negative_count/len(df)*100):.1f}%")
        
        with col3:
            neutral_count = sentiment_counts.get("Neutral", 0)
            st.metric("😐 Neutral", f"{neutral_count}", f"{(neutral_count/len(df)*100):.1f}%")
    
    except Exception as e:
        st.error(f"❌ Error loading feedback data: {str(e)}")
        st.info("Please check your database connection and table structure.")