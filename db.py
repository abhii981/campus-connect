import psycopg2
import streamlit as st

def get_connection():
    return psycopg2.connect(
        host=st.secrets["PGHOST"],
        user=st.secrets["PGUSER"],
        password=st.secrets["PGPASSWORD"],
        dbname=st.secrets["PGDATABASE"],
        port=st.secrets.get("PGPORT", 5432)
    )
