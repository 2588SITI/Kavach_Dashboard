import streamlit as st
import pandas as pd

# The ID from your URL
SHEET_ID = "1Rk73UDXkULAkboFj5TcQAE2GDyRmBJcSQqGhpz2iOeY"
# This URL format tells Google to give us the whole list of tabs
XLSX_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

st.set_page_config(page_title="Kavach Master Dashboard", layout="wide")

@st.cache_data
def load_all_pages():
    # We download as Excel (.xlsx) because it contains ALL tabs in one file
    all_sheets = pd.read_excel(XLSX_URL, sheet_name=None)
    return all_sheets

st.sidebar.title("🚉 Kavach Dashboard")
st.sidebar.info("Select a page below to view data")

try:
    # Load the dictionary of dataframes
    pages_dict = load_all_pages()
    
    # Create the navigation based on actual Tab Names in your Google Sheet
    sheet_names = list(pages_dict.keys())
    selection = st.sidebar.radio("Go to Page:", sheet_names)

    st.title(f"📊 {selection}")
    
    # Get the data for the selected page
    df = pages_dict[selection]
    
    # Data Cleaning: Remove empty rows and fix headers
    df = df.dropna(how='all').reset_index(drop=True)
    df.columns = [str(c).strip() for c in df.columns]

    # --- Page Content Logic ---
    if "Loco no." in df.columns:
        c1, c2 = st.columns(2)
        c1.metric("Total Rows", len(df))
        c2.metric("Unique Locos", df["Loco no."].nunique())

    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Failed to fetch data: {e}")
    st.markdown("### 🛠️ How to fix the Permission Block:")
    st.write("1. Open your Google Sheet.")
    st.write("2. Click **File > Share > Publish to web**.")
    st.write("3. Click **Publish** (Entire Document).")
    st.write("4. Close that window and try running the dashboard again.")
