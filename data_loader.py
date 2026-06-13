import pandas as pd
import streamlit as st
from typing import Optional

def load_data(uploaded_file) -> Optional[pd.DataFrame]:
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            return pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload CSV, XLS, or XLSX.")
            return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None