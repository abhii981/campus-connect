import streamlit as st
import base64
from datetime import datetime
from db import get_connection

def notices_page():

    # ==================== STYLES (UNCHANGED) ====================
    st.markdown("""
    <style>
    .notices-breadcrumb { font-size:14px;color:#64748b;margin-bottom:8px }
    .notices-breadcrumb span { color:#3b82f6;font-weight:600 }
    .notices-header { font-size:36px;font-weight:800;color:#0f172a;margin-bottom:8px }
    .notices-subheader { font-size:18px;color:#3b82f6;font-weight:600;margin-bottom:30px }
    .section-title { font-size:24px;font-weight:700;color:#0f172a }
    .section-subtitle { font-size:14px;color:#64748b }
    .notices-card {
        background:#fff;border:1px solid #e5e7eb;border-radius:12px;
        padding:20px;margin-bottom:16px
    }
    .notices-badge {
        font-size:13px;background:#eff6ff;color:#1e40af;
        padding:5px 12px;border-radius:16px;font-weight:600
    }
    .notices-title { font-size:18px;font-weight:700;color:#0f172a }
    .notices-desc { font-size:14px;color:#475569 }
    iframe { border-radius:12px;margin-top:16px }
    .new-indicator {
        background:#22c55e;color:white;padding:3px 10px;
        border-radius:12px;font-size:11px;font-weight:700
    }
    </style>
    """, unsafe_allow_html=True)

    # ==================== HEADER ====================
    st.markdown("<div class='notices-breadcrumb'>Home <span>/ Notices</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='notices-header'>🎓 Campus Connect</div>", unsafe_allow_html=True)
    st.markdown("<div class='notices-subheader'>Official campus notices & academic updates</div>", unsafe_allow_html=True)

    left_col, _, right_col = st.columns([10, 0.5, 10])

    # ==================== UTIL: SAFE BYTEA → BYTES ====================
    def to_bytes(file_data):
        if file_data is None:
            return None
        if isinstance(file_data, memoryview):
            return bytes(file_data)
        if isinstance(file_data, bytes):
            return file_data
        if isinstance(file_data, str) and file_data.startswith("\\x"):
            return bytes.fromhex(file_data[2:])
        return None

    # ==================== OFFICIAL NOTICES ====================
    with left_col:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT notice_id, title, description, file_data, file_name, created_at
                FROM notices
                ORDER BY created_at DESC
            """)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            cur.close()
            conn.close()

            if not rows:
                st.info("📭 No notices available yet.")
                return

            st.markdown(f"**📊 Total: {len(rows)} notices**")

            for idx, row in enumerate(rows):
                n = dict(zip(cols, row))

                st.markdown("<div class='notices-card'>", unsafe_allow_html=True)

                # ---- Date badge ----
                created_at = n.get("created_at")
                date_str = "Unknown date"
                is_new = False

                if created_at:
                    if hasattr(created_at, "strftime"):
                        dt = created_at
                    else:
                        dt = datetime.strptime(str(created_at), "%Y-%m-%d %H:%M:%S")
                    date_str = dt.strftime("%d %b %Y")
                    is_new = (datetime.now() - dt).days <= 7

                badge = f"<span class='new-indicator'>New</span>" if is_new else ""
                st.markdown(f"<div class='notices-badge'>📅 {date_str} {badge}</div>", unsafe_allow_html=True)

                st.markdown(f"<div class='notices-title'>{n['title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='notices-desc'>{n['description']}</div>", unsafe_allow_html=True)

                # ---- FILE HANDLING (FIXED) ----
                file_bytes = to_bytes(n.get("file_data"))
                file_name = n.get("file_name")

                if file_bytes:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.download_button(
                            "📥 Download PDF",
                            data=file_bytes,
                            file_name=file_name or "notice.pdf",
                            mime="application/pdf",
                            key=f"dl_{idx}"
                        )

                    with col2:
                        if st.button("👁️ View PDF", key=f"view_{idx}"):
                            st.session_state[f"show_{idx}"] = not st.session_state.get(f"show_{idx}", False)

                    if st.session_state.get(f"show_{idx}", False):
                        b64 = base64.b64encode(file_bytes).decode("utf-8")
                        st.markdown(
                            f"<iframe src='data:application/pdf;base64,{b64}' width='100%' height='600px'></iframe>",
                            unsafe_allow_html=True
                        )
                else:
                    st.info("📄 No PDF attached")

                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error loading notices: {e}")

    # ==================== CLUB EVENTS ====================
    with right_col:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT title, description, event_date, venue
                FROM club_events
                ORDER BY event_date ASC
            """)
            events = cur.fetchall()
            cur.close()
            conn.close()

            if not events:
                st.info("🎭 No club events announced yet.")
                return

            for e in events:
                title, desc, dt, venue = e
                date_str = dt.strftime("%d %b %Y") if dt else "Date TBA"

                st.markdown(f"""
                <div class="notices-card">
                    <div class="notices-title">{title}</div>
                    <div class="notices-desc">{desc}</div>
                    <div style="font-size:13px;color:#6b21a8;font-weight:600">
                        📍 {venue} • 📅 {date_str}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error loading events: {e}")
