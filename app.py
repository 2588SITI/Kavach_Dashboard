import streamlit as st
import pandas as pd

# The ID from your URL
SHEET_ID = "1Rk73UDXkULAkboFj5TcQAE2GDyRmBJcSQqGhpz2iOeY"
XLSX_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

st.set_page_config(page_title="Kavach Master Dashboard", layout="wide")

@st.cache_data(ttl=600)
def load_all_pages():
    # We use engine='openpyxl' explicitly to tell pandas what to use
    all_sheets = pd.read_excel(XLSX_URL, sheet_name=None, engine='openpyxl')
    
    # This loop fixes the 'S.No' date error by converting everything to text
    cleaned_sheets = {}
    for name, df in all_sheets.items():
        df = df.astype(str).replace('nan', '')
        cleaned_sheets[name] = df
    return cleaned_sheets

st.sidebar.title("🚉 Kavach Dashboard")

try:
    data_dict = load_all_pages()
    sheet_names = list(data_dict.keys())
    selection = st.sidebar.radio("Select Tab:", sheet_names)

    st.title(f"📊 {selection}")
    
    # Using the new 'use_container_width' parameter to avoid warnings
    st.dataframe(data_dict[selection], use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Error: {e}")
    st.info("If it says 'openpyxl missing', please restart VS Code.")
