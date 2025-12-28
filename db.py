import psycopg2
import streamlit as st
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host=st.secrets["PGHOST"],
        port=st.secrets["PGPORT"],
        dbname=st.secrets["PGDATABASE"],
        user=st.secrets["PGUSER"],
        password=st.secrets["PGPASSWORD"],
        sslmode="require",
        cursor_factory=RealDictCursor
    )
