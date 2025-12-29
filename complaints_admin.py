import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db import get_connection

def admin_complaints_page():
    # Custom styling for this page
    st.markdown("""
    <style>
    /* Page headers - dark and visible */
    .complaints-header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
    }
    
    .complaints-subtitle {
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
    
    /* Table header styling */
    [data-testid="stDataFrame"] thead tr th {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 12px !important;
        border: none !important;
    }
    
    /* Table body styling */
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
    
    /* Alternating row colors */
    [data-testid="stDataFrame"] tbody tr:nth-child(even) {
        background: #f8fafc !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="complaints-header">🧾 Complaint Management & Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="complaints-subtitle">View, monitor and analyze all campus complaints</div>', unsafe_allow_html=True)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch all complaints
        cursor.execute("""
            SELECT 
                complaint_id, user_id, complaint_text, category, area,
                urgency, status, created_at
            FROM complaints
            ORDER BY created_at DESC
        """)
        
        data = cursor.fetchall()
        
        # Get column names from cursor description
        columns = [desc[0] for desc in cursor.description]
        
        cursor.close()
        conn.close()

        if not data or len(data) == 0:
            st.info("📋 No complaints available in the system yet.")
            return
        
        # Create DataFrame with proper column names
        df = pd.DataFrame(data, columns=columns)
        
        # Display All Complaints
        st.markdown('<div class="section-header">📋 All Complaints</div>', unsafe_allow_html=True)
        display_df = df.copy()
        
        # Convert created_at to datetime and format properly
        try:
            display_df["created_at"] = pd.to_datetime(display_df["created_at"], errors='coerce').dt.strftime("%d %b %Y %H:%M")
        except:
            # If conversion fails, keep as is
            pass

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # High Urgency Complaints
        st.markdown(
            "<h3 style='color:#dc2626; font-size:24px; font-weight:700; margin-top:30px;'>🚨 High Urgency Complaints</h3>",
            unsafe_allow_html=True
        )

        urgent_df = df[df["urgency"].str.lower() == "high"]
        if urgent_df.empty:
            st.success("✅ No high urgency complaints 🎉")
        else:
            for _, row in urgent_df.iterrows():
                st.markdown(
                    f"""
                    <div style="
                        background:#fee2e2;
                        border-left:6px solid #dc2626;
                        padding:16px 20px;
                        border-radius:12px;
                        margin-bottom:12px;
                        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
                    ">
                        <b style="color:#0f172a; font-size:16px;">📌 {row['complaint_text']}</b><br>
                        <span style="font-size:14px; color:#7f1d1d; margin-top:6px; display:block;">
                            Area: <strong>{row['area']}</strong> | Category: <strong>{row['category']}</strong> | Status: <strong>{row['status']}</strong>
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Complaint Analysis Section
        st.markdown('<div class="section-header">📊 Complaint Analysis</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # Chart 1: Complaints by Area
        with col1:
            st.markdown(
                "<div style='font-size:18px; font-weight:700; color:#0f172a; margin-bottom:10px;'>📍 Complaints by Area</div>",
                unsafe_allow_html=True
            )
            
            if df["area"].notna().any():
                area_counts = df["area"].value_counts()

                fig, ax = plt.subplots(figsize=(8, 6))
                sns.barplot(
                    x=area_counts.values,
                    y=area_counts.index,
                    ax=ax,
                    palette="Blues_d"
                )
                ax.set_xlabel("Number of Complaints", fontsize=12, color="#0f172a")
                ax.set_ylabel("Area", fontsize=12, color="#0f172a")
                ax.tick_params(colors="#0f172a")
                
                # Add value labels on bars
                for i, v in enumerate(area_counts.values):
                    ax.text(v + 0.1, i, str(v), color="#0f172a", va='center', fontweight='bold')
                
                fig.patch.set_facecolor('white')
                ax.set_facecolor('#f8fafc')
                st.pyplot(fig)
            else:
                st.info("No area data available yet")

        # Chart 2: Complaints by Category
        with col2:
            st.markdown(
                "<div style='font-size:18px; font-weight:700; color:#0f172a; margin-bottom:10px;'>🏷 Complaints by Category</div>",
                unsafe_allow_html=True
            )

            if df["category"].notna().any():
                category_counts = df["category"].value_counts()

                fig, ax = plt.subplots(figsize=(8, 6))
                sns.barplot(
                    x=category_counts.index,
                    y=category_counts.values,
                    ax=ax,
                    palette="Greens_d"
                )
                ax.set_ylabel("Number of Complaints", fontsize=12, color="#0f172a")
                ax.set_xlabel("Category", fontsize=12, color="#0f172a")
                ax.tick_params(axis='x', rotation=30, colors="#0f172a")
                ax.tick_params(axis='y', colors="#0f172a")
                
                # Add value labels on bars
                for i, v in enumerate(category_counts.values):
                    ax.text(i, v + 0.1, str(v), ha='center', color="#0f172a", fontweight='bold')
                
                fig.patch.set_facecolor('white')
                ax.set_facecolor('#f8fafc')
                st.pyplot(fig)
            else:
                st.info("No category data available yet")
        
        # Chart 3: Complaints Over Time
        st.markdown(
            "<div style='font-size:18px; font-weight:700; color:#0f172a; margin-bottom:10px; margin-top:30px;'>⏱ Complaints Over Time</div>",
            unsafe_allow_html=True
        )

        try:
            # Create a proper date column for time series
            df["display_date"] = pd.to_datetime(df["created_at"], errors='coerce').dt.date
            
            # Remove any NaT values
            df_filtered = df[df["display_date"].notna()]
            
            if not df_filtered.empty:
                time_counts = df_filtered.groupby("display_date").size().reset_index(name="count")

                fig, ax = plt.subplots(figsize=(12, 5))
                sns.lineplot(
                    data=time_counts,
                    x="display_date",
                    y="count",
                    marker="o",
                    ax=ax,
                    color="#3b82f6",
                    linewidth=2.5,
                    markersize=8
                )
                ax.set_xlabel("Date", fontsize=12, color="#0f172a")
                ax.set_ylabel("Number of Complaints", fontsize=12, color="#0f172a")
                ax.tick_params(colors="#0f172a")
                ax.grid(True, alpha=0.3)
                
                fig.patch.set_facecolor('white')
                ax.set_facecolor('#f8fafc')
                
                st.pyplot(fig)
            else:
                st.info("No date data available for time series analysis")
                
        except Exception as e:
            st.warning(f"Unable to generate time series chart: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Error loading complaints data: {str(e)}")
        st.info("Please check your database connection and table structure.")