import streamlit as st
import pandas as pd

# The ID from your URL
SHEET_ID = "1Rk73UDXkULAkboFj5TcQAE2GDyRmBJcSQqGhpz2iOeY"
XLSX_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

st.set_page_config(page_title="Kavach Master Dashboard", layout="wide")

@st.cache_data(ttl=600)
def load_all_pages():
    # Load all sheets
    all_sheets = pd.read_excel(XLSX_URL, sheet_name=None)
    
    # Fix the data types to prevent the "ArrowInvalid" error
    cleaned_sheets = {}
    for name, df in all_sheets.items():
        # Convert everything to string/object to prevent date-conversion crashes
        df = df.astype(str) 
        # Replace 'nan' strings with empty spaces
        df = df.replace('nan', '')
        cleaned_sheets[name] = df
        
    return cleaned_sheets

st.sidebar.title("🚉 Kavach Dashboard")

try:
    data_dict = load_all_pages()
    sheet_names = list(data_dict.keys())
    selection = st.sidebar.radio("Go to Page:", sheet_names)

    st.title(f"📊 {selection}")
    
    df = data_dict[selection]

    # Show the table using the new 'width' parameter
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
