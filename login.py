import streamlit as st 
from db import get_connection 
import re

def login_page():
    st.markdown("""
<style>
/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stHeader"] {display: none;}
[data-testid="stToolbar"] {display: none;}
div:empty {display: none !important;}

/* Light purple/blue background like hotel system */
.stApp {
    background: linear-gradient(135deg, #e8eaf6 0%, #e3f2fd 100%) !important;
}

/* Page styling */
.block-container {
    padding-top: 1rem !important;
    max-width: 1400px !important;
}

/* Input fields - white with subtle shadow */
.stTextInput > div > div > input {
    background-color: #ffffff !important;
    border-radius: 12px !important;
    padding: 18px 24px !important;
    border: none !important;
    font-size: 16px !important;
    color: #2c3e50 !important;
    -webkit-text-fill-color: #2c3e50 !important;
    box-shadow: 0 2px 8px rgba(63, 81, 181, 0.1);
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    box-shadow: 0 4px 16px rgba(63, 81, 181, 0.2);
    transform: translateY(-2px);
}

/* Labels */
.stTextInput > label {
    color: #2c3e50 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    margin-bottom: 8px !important;
}

/* Button - matching hotel system blue */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #3f51b5 0%, #283593 100%) !important;
    color: white !important;
    padding: 18px 32px !important;
    border-radius: 12px !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    box-shadow: 0 4px 16px rgba(63, 81, 181, 0.4);
    border: none !important;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #283593 0%, #1a237e 100%) !important;
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(63, 81, 181, 0.5);
}

/* Hero header card - SMALLER SIZE */
.hero-banner {
    background: linear-gradient(135deg, #3f51b5 0%, #283593 100%);
    border-radius: 20px;
    padding: 30px 40px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(63, 81, 181, 0.3);
    margin-bottom: 30px;
}

.hero-icon {
    font-size: 50px;
    margin-bottom: 10px;
}

.hero-title {
    font-size: 38px;
    font-weight: 900;
    color: white;
    margin-bottom: 8px;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.95);
    font-weight: 500;
    margin-bottom: 0;
}

/* White cards - matching hotel cards */
.white-card {
    background: white;
    border-radius: 20px;
    padding: 35px;
    box-shadow: 0 4px 20px rgba(63, 81, 181, 0.08);
    transition: all 0.3s ease;
}

.white-card:hover {
    box-shadow: 0 8px 32px rgba(63, 81, 181, 0.15);
    transform: translateY(-4px);
}

.card-title {
    font-size: 26px;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 8px;
}

.card-subtitle {
    font-size: 15px;
    color: #7f8c8d;
    margin-bottom: 25px;
}

/* Feature list items - MORE COMPACT */
.feature-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 10px;
    margin-bottom: 10px;
    transition: all 0.3s ease;
}

.feature-item:hover {
    background: #e8eaf6;
    transform: translateX(8px);
}

.feature-icon {
    font-size: 24px;
}

.feature-text {
    font-size: 15px;
    color: #2c3e50;
    font-weight: 600;
}

/* Footer badge */
.footer-badge {
    text-align: center;
    margin-top: 25px;
    padding: 14px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(63, 81, 181, 0.08);
    font-size: 14px;
    color: #7f8c8d;
    font-weight: 600;
}

/* Text link styling */
.auth-links {
    text-align: center;
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #e0e0e0;
}

.auth-link {
    color: #3f51b5;
    cursor: pointer;
    font-weight: 600;
    font-size: 14px;
    text-decoration: none;
    transition: all 0.2s ease;
    display: inline-block;
    margin: 0 10px;
}

.auth-link:hover {
    color: #283593;
    text-decoration: underline;
}

/* Back link */
.back-link {
    color: #3f51b5;
    cursor: pointer;
    font-weight: 600;
    font-size: 14px;
    margin-top: 15px;
    display: inline-block;
}

.back-link:hover {
    color: #283593;
    text-decoration: underline;
}

/* Hide secondary buttons - FIXED SELECTOR */
button[data-testid="baseButton-secondary"] {
    background: transparent !important;
    color: #3f51b5 !important;
    border: 2px solid #3f51b5 !important;
    padding: 8px 16px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    margin: 5px !important;
    width: auto !important;
    border-radius: 8px !important;
}

button[data-testid="baseButton-secondary"]:hover {
    background: #f0f2ff !important;
    transform: translateY(-2px) !important;
}

/* Text link container */
.link-container {
    text-align: center;
    margin-top: 20px;
}

/* Container for navigation links */
.nav-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #e0e0e0;
}
.demo-box {
    margin-top: 18px;
    padding: 14px;
    background: #f5f7ff;
    border-radius: 10px;
    border-left: 4px solid #3f51b5;
    font-size: 14px;
    color: #2c3e50;
}
.demo-title {
    font-weight: 700;
    margin-bottom: 6px;
    color: #283593;
}
.demo-item {
    margin-left: 6px;
}

</style>
""", unsafe_allow_html=True)

    # Initialize session state for page switching
    if 'auth_page' not in st.session_state:
        st.session_state.auth_page = 'login'

    # Hero Banner - SMALLER
    st.markdown("""
<div class="hero-banner">
    <div class="hero-icon">🎓</div>
    <div class="hero-title">Campus Connect</div>
    <div class="hero-subtitle">Smart database-driven campus operations & analytics</div>
</div>
""", unsafe_allow_html=True)

    # Two columns
    col1, col2 = st.columns([1, 1], gap="large")

    # LEFT: Features
    with col1:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🌟 Portal Features</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-subtitle">Your unified campus information hub</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-item">
            <div class="feature-icon">📢</div>
            <div class="feature-text">Official notices & academic circulars</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">📚</div>
            <div class="feature-text">Study resources & PDF management</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🧑‍💼</div>
            <div class="feature-text">Role-based access for admins & students</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">💬</div>
            <div class="feature-text">Complaint & feedback resolution system</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🏫</div>
            <div class="feature-text">Centralized campus communication</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT: Forms (Login / Register / Forgot Password)
    with col2:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        
        # ==================== LOGIN PAGE ====================
        if st.session_state.auth_page == 'login':
            st.markdown('<div class="card-title">🔐 Sign in</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-subtitle">Access your campus portal securely</div>', unsafe_allow_html=True)

            user_id = st.text_input("Enrollment Number", placeholder="Enter your enrollment number", key="login_uid")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pwd")

            if st.button("Login", key="login_btn"):
                if not user_id.strip():
                    st.error("⚠️ Please enter your Enrollment Number")
                elif not password.strip():
                    st.error("⚠️ Please enter your Password")
                elif not user_id.isdigit():
                    st.error("⚠️ Enrollment Number must be numeric")
                else:
                    user_id = int(user_id)
                    try:
                        conn = get_connection()
                        cursor = conn.cursor(dictionary=True)
                        cursor.execute(
                            "SELECT * FROM users WHERE user_id=%s AND password=%s",
                            (user_id, password)
                        )
                        user = cursor.fetchone()
                        cursor.close()
                        conn.close()

                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_id = user["user_id"]
                            st.session_state.name = user["name"]
                            st.session_state.role = user["role"]
                            st.success("✅ Login successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Please try again.")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
            
            st.markdown("""
                <div class="demo-box">
                <div class="demo-title">🧪 Demo Credentials</div>
                <div class="demo-item">
            <b>Admin</b><br>
                User ID: <code>1</code> | Password: <code>admin123</code>
            </div>
            <br>
                <div class="demo-item">
            <b>Club Lead</b><br>
            User ID: <code>5</code> | Password: <code>stud123</code>
        </div>
        </div>
            """, unsafe_allow_html=True)

            # Navigation links
            st.markdown("""
            <div class="nav-container">
                <div style="color: #7f8c8d;">Don't have an account?</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Small navigation buttons
            nav_col1, nav_col2 = st.columns(2)
            with nav_col1:
                if st.button("Register here", key="go_register", type="secondary", use_container_width=True):
                    st.session_state.auth_page = 'register'
                    st.rerun()
            with nav_col2:
                if st.button("Forgot Password?", key="go_forgot", type="secondary", use_container_width=True):
                    st.session_state.auth_page = 'forgot'
                    st.rerun()
        
        # ==================== REGISTRATION PAGE ====================
        elif st.session_state.auth_page == 'register':
            st.markdown('<div class="card-title">📝 Student Registration</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-subtitle">Create your campus portal account</div>', unsafe_allow_html=True)

            enrollment = st.text_input("Enrollment Number", placeholder="Enter your enrollment number", key="reg_enrollment")
            name = st.text_input("Full Name", placeholder="Enter your full name", key="reg_name")
            email = st.text_input("Email", placeholder="your.email@campus.edu", key="reg_email")
            password = st.text_input("Password", type="password", placeholder="Create a strong password", key="reg_pwd")
            confirm_pwd = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", key="reg_confirm")

            if st.button("Register", key="register_btn"):
                # Validation
                if not all([enrollment, name, email, password, confirm_pwd]):
                    st.error("⚠️ All fields are required")
                elif password != confirm_pwd:
                    st.error("⚠️ Passwords do not match")
                elif len(password) < 6:
                    st.error("⚠️ Password must be at least 6 characters")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error("⚠️ Invalid email format")
                elif not enrollment.isdigit():
                    st.error("⚠️ Enrollment Number must be numeric")
                else:
                    try:
                        enrollment_num = int(enrollment)
                        conn = get_connection()
                        cursor = conn.cursor()
                        
                        # Check if enrollment number already exists
                        cursor.execute("SELECT * FROM users WHERE user_id = %s", (enrollment_num,))
                        existing_user = cursor.fetchone()
                        
                        if existing_user:
                            st.error("❌ This enrollment number is already registered")
                        else:
                            # Insert new user (role='student' by default)
                            cursor.execute("""
                                INSERT INTO users (user_id, name, email, password, role)
                                VALUES (%s, %s, %s, %s, 'student')
                            """, (enrollment_num, name, email, password))
                            
                            conn.commit()
                            cursor.close()
                            conn.close()
                            
                            st.success(f"✅ Registration successful! Your Enrollment Number is: **{enrollment_num}**")
                            st.info("💡 Please save your Enrollment Number for login")
                            st.balloons()
                            
                    except Exception as e:
                        st.error(f"❌ Registration failed: {str(e)}")
            
            # Small back button
            if st.button("← Back to Login", key="back_to_login_from_reg", type="secondary", use_container_width=True):
                st.session_state.auth_page = 'login'
                st.rerun()
        
        # ==================== FORGOT PASSWORD PAGE ====================
        elif st.session_state.auth_page == 'forgot':
            st.markdown('<div class="card-title">🔑 Reset Password</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-subtitle">Enter your details to reset password</div>', unsafe_allow_html=True)

            user_id = st.text_input("Enrollment Number", placeholder="Enter your enrollment number", key="forgot_uid")
            email = st.text_input("Email", placeholder="your.email@campus.edu", key="forgot_email")
            new_password = st.text_input("New Password", type="password", placeholder="Enter new password", key="forgot_new_pwd")
            confirm_pwd = st.text_input("Confirm New Password", type="password", placeholder="Re-enter new password", key="forgot_confirm")

            if st.button("Reset Password", key="reset_btn"):
                if not all([user_id, email, new_password, confirm_pwd]):
                    st.error("⚠️ All fields are required")
                elif not user_id.isdigit():
                    st.error("⚠️ Enrollment Number must be numeric")
                elif new_password != confirm_pwd:
                    st.error("⚠️ Passwords do not match")
                elif len(new_password) < 6:
                    st.error("⚠️ Password must be at least 6 characters")
                else:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor(dictionary=True)
                        
                        # Verify user exists with this email and enrollment number
                        cursor.execute(
                            "SELECT * FROM users WHERE user_id=%s AND email=%s",
                            (int(user_id), email)
                        )
                        user = cursor.fetchone()
                        
                        if user:
                            # Update password
                            cursor.execute(
                                "UPDATE users SET password=%s WHERE user_id=%s",
                                (new_password, int(user_id))
                            )
                            conn.commit()
                            cursor.close()
                            conn.close()
                            
                            st.success("✅ Password reset successful! You can now login with your new password.")
                            st.balloons()
                        else:
                            st.error("❌ Enrollment Number and Email do not match our records")
                            cursor.close()
                            conn.close()
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            # Small back button
            if st.button("← Back to Login", key="back_to_login_from_forgot", type="secondary", use_container_width=True):
                st.session_state.auth_page = 'login'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer-badge">
        🔒 Secure campus authentication powered by database-driven operations
    </div>
    """, unsafe_allow_html=True)