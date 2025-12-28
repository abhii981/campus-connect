import streamlit as st
import os
import base64
from db import get_connection

def resources_page():
    
    st.markdown("""
    <style>
    .resources-breadcrumb {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 8px;
    }
    .resources-breadcrumb span {
        color: #3b82f6;
        font-weight: 600;
    }
    
    .resources-header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    
    .resources-subheader {
        font-size: 18px;
        color: #3b82f6;
        font-weight: 600;
        margin-bottom: 30px;
    }
    
    .resources-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .resources-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
        border-color: #3b82f6;
    }
    
    .resources-subject {
        font-size: 13px;
        background: linear-gradient(135deg, #cffafe 0%, #ecfeff 100%);
        color: #0369a1;
        padding: 5px 12px;
        border-radius: 16px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        margin-bottom: 12px;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(3, 105, 161, 0.1);
    }
    
    .resources-title {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 14px;
    }
    
    /* View button */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    iframe {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-top: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='resources-breadcrumb'>Home <span>/ Resources</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='resources-header'>📚 Resources</div>", unsafe_allow_html=True)
    st.markdown("<div class='resources-subheader'>Study materials and reference documents</div>", unsafe_allow_html=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT resource_title, resource_subject, file_url, created_at
        FROM resources
        ORDER BY created_at DESC
    """)
    resources = cursor.fetchall()

    if not resources:
        st.info("📂 No resources available yet. Check back soon!")
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                    padding: 12px 18px; 
                    border-radius: 10px; 
                    margin-bottom: 20px;
                    border-left: 4px solid #22c55e;">
            <span style="color: #15803d; font-weight: 600; font-size: 14px;">
                📊 Total Resources: <strong>{len(resources)}</strong>
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        for idx, r in enumerate(resources):
            with st.container():
                st.markdown("<div class='resources-card'>", unsafe_allow_html=True)

                if r["resource_subject"]:
                    st.markdown(
                        f"<div class='resources-subject'>📘 {r['resource_subject']}</div>",
                        unsafe_allow_html=True
                    )

                st.markdown(f"<div class='resources-title'>{r['resource_title']}</div>", unsafe_allow_html=True)

                file_path = r["file_url"]
                
                if file_path and os.path.exists(file_path):
                    # Buttons row
                    col1, col2 = st.columns([1, 1])

                    with col1:
                        view_clicked = st.button("📄 View Resource", key=f"res_{idx}")

                    with col2:
                        with open(file_path, "rb") as f:
                            st.download_button(
                                "⬇️ Download PDF",
                                data=f.read(),
                                file_name=os.path.basename(file_path),
                                mime="application/pdf",
                                key=f"download_res_{idx}"
                            )

                    if view_clicked:
                        with open(file_path, "rb") as f:
                            pdf_bytes = f.read()
                            base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

                        st.markdown(
                             f"""
                            <iframe src="data:application/pdf;base64,{base64_pdf}"
                            width="100%" height="650px"
                             style="
                            border:none;
                            margin-top:16px;
                            border-radius:12px;
                            box-shadow:0 6px 18px rgba(0,0,0,0.12);
                        ">
                        </iframe>
                        """,
                        unsafe_allow_html=True
                     )


                st.markdown("</div>", unsafe_allow_html=True)

    cursor.close()
    conn.close()
