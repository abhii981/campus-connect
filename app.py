import streamlit as st
from login import login_page
from student import student_dashboard
from admin import admin_dashboard

st.set_page_config(
    page_title="Campus Connect",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "name" not in st.session_state:
    st.session_state.name = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ---------------- ROUTING ----------------
if not st.session_state.logged_in:
    # 🔐 Show login page (login.py has its own styling)
    login_page()

else:
    st.markdown("""
    <style>
    /* ================= GLOBAL SETTINGS ================= */

    /* Hide Streamlit branding for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Main app background */
    .stApp {
        background-color: #f8fafc !important;
    }

    /* Smooth transitions for all interactive elements */
    * {
        transition: all 0.2s ease;
    }

    /* ================= TYPOGRAPHY & TEXT ================= */

    /* Breadcrumb */
    .breadcrumb {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .breadcrumb span {
        color: #3b82f6;
        font-weight: 600;
    }

    /* Header */
    .header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }

    /* Subheader */
    .subheader {
        font-size: 18px;
        color: #3b82f6;
        font-weight: 600;
        margin-bottom: 24px;
    }

    /* Title */
    .title {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }

    /* Description */
    .desc {
        font-size: 15px;
        color: #475569;
        margin-bottom: 12px;
        line-height: 1.6;
    }

    /* Card with hover effect */
    .card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }

    .card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
        border-color: #3b82f6;
    }

    /* Welcome bar enhancement */
    .welcome-bar {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 18px 24px;
        border-radius: 14px;
        margin-bottom: 28px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }

    .welcome-text {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
    }

    .welcome-role {
        font-size: 14px;
        color: #64748b;
        font-weight: 500;
        margin-left: 8px;
    }


    /* Date badge with icon */
    .badge {
        font-size: 13px;
        background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
        color: #1e40af;
        padding: 5px 12px;
        border-radius: 16px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        margin-bottom: 8px;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(30, 64, 175, 0.1);
    }

    /* Subject badge */
    .subject {
        font-size: 13px;
        background: linear-gradient(135deg, #cffafe 0%, #ecfeff 100%);
        color: #0369a1;
        padding: 5px 12px;
        border-radius: 16px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        margin-bottom: 8px;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(3, 105, 161, 0.1);
    }

    /* ================= SIDEBAR ================= */

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #e2e8f0;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: #e2e8f0 !important;
    }

    /* ================= FORM ELEMENTS ================= */

    /* Text input fields - DASHBOARD PAGES (white background) */
    div[data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }

    /* Text input labels - DASHBOARD PAGES */
    div[data-testid="stTextInput"] label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }

    .stTextArea label {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Select box styling */
    .stSelectbox > div > div {
        border-radius: 10px !important;
    }

    .stSelectbox label {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Select box dropdown text */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
    }

    .stSelectbox div[data-baseweb="select"] span {
        color: #0f172a !important;
    }

    /* File uploader container */
    div[data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 20px !important;
        border: 2px dashed #cbd5e1 !important;
    }

    /* File uploader label */
    div[data-testid="stFileUploader"] label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* File uploader text - ALL TEXT VISIBLE */
    div[data-testid="stFileUploader"] section {
        background-color: #f8fafc !important;
        border-radius: 8px !important;
    }

    div[data-testid="stFileUploader"] section * {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    /* Drag & drop text */
    div[data-testid="stFileUploader"] small {
        color: #64748b !important;
        font-weight: 500 !important;
    }

    /* Browse files button inside uploader */
    div[data-testid="stFileUploader"] button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        border: none !important;
    }

    div[data-testid="stFileUploader"] button:hover {
        background-color: #2563eb !important;
    }


    /* Button styling improvement */
    .stButton > button {
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        background-color: #1e293b !important;
        color: #ffffff !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        background-color: #334155 !important;
    }

    /* Download button specific styling */
    .stDownloadButton > button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
    }

    .stDownloadButton > button:hover {
        background-color: #2563eb !important;
    }

    /* ================= OTHER COMPONENTS ================= */

    /* Metric cards enhancement */
    [data-testid="stMetric"] {
        background: white;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    [data-testid="stMetric"] label {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0f172a !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        color: #475569;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #3b82f6;
    }

    /* Success/Error message styling */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }

    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Sidebar brand */
    .sidebar-brand {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        letter-spacing: 1px;
        margin-top: 10px;
        margin-bottom: 18px;
    }

    .sidebar-divider {
        height: 1px;
        background: rgba(255,255,255,0.25);
        margin-bottom: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- WELCOME BAR ----------
    role_emoji = "👨‍💼" if st.session_state.role == "admin" else "🎓"
    
    st.markdown(f"""
<div class="welcome-bar">
    <div class="welcome-text">
        👋 Welcome back, {st.session_state.name}!
        <span class="welcome-role">
            {role_emoji} {st.session_state.role.capitalize()}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
    
    with st.sidebar:
        st.sidebar.markdown(
            "<div class='sidebar-brand'>CAMPUS CONNECT</div>",
            unsafe_allow_html=True
        )

        st.sidebar.markdown(
            "<div class='sidebar-divider'></div>",
            unsafe_allow_html=True
        )
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        student_dashboard()
