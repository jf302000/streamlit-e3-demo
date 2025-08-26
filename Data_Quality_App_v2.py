import streamlit as st
import pandas as pd
import numpy as np
import re
import time
import concurrent.futures

# Title of the app
st.title('CSV Data Summary and Cleaning with Feedback')

# Step-by-step navigation
steps = ["Upload File", "Preview Data", "Handle Missing Values", "Remove Weird Characters", "Remove Duplicates", "Download Cleaned Data"]
current_step = st.sidebar.radio("Navigation", steps)

# Upload CSV file
if current_step == "Upload File":
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    if uploaded_file is not None:
        try:
            st.session_state['df'] = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully! Proceed to the next step.")
        except Exception as e:
            st.error(f"Error loading file: {e}")

# Preview Data
if current_step == "Preview Data" and 'df' in st.session_state:
    st.subheader('Data Preview')
    preview_rows = 100 if st.session_state['df'].shape[0] > 100 else st.session_state['df'].shape[0]
    st.write(st.session_state['df'].head(preview_rows))

# Handle Missing Values
if current_step == "Handle Missing Values" and 'df' in st.session_state:
    st.subheader('Check for Missing Values')

    # Check for missing values
    missing_summary = st.session_state['df'].isnull().sum()
    missing_columns = missing_summary[missing_summary > 0]

    if not missing_columns.empty:
        st.write("### Columns with Missing Values")
        st.write(missing_columns)

        # Option to search column-by-column or globally
        search_scope = st.radio("Search Scope", ["Global", "Column-by-Column"], key="missing_search_scope")

        if search_scope == "Column-by-Column":
            selected_column = st.selectbox("Select a column to handle missing values:", missing_columns.index)
            method = st.selectbox(
                f"Select a method to handle missing values in {selected_column}:",
                ["Fill with Mean", "Fill with Median", "Fill with Mode", "Drop Rows"]
            )
            if st.button("Apply to Selected Column"):
                if method == "Fill with Mean":
                    st.session_state['df'][selected_column] = st.session_state['df'][selected_column].fillna(st.session_state['df'][selected_column].mean())
                elif method == "Fill with Median":
                    st.session_state['df'][selected_column] = st.session_state['df'][selected_column].fillna(st.session_state['df'][selected_column].median())
                elif method == "Fill with Mode":
                    mode = st.session_state['df'][selected_column].mode()
                    if not mode.empty:
                        st.session_state['df'][selected_column] = st.session_state['df'][selected_column].fillna(mode[0])
                elif method == "Drop Rows":
                    st.session_state['df'] = st.session_state['df'].dropna(subset=[selected_column])
                st.success(f"Applied '{method}' to column {selected_column}.")
        else:
            global_method = st.selectbox(
                "Select a global method to handle missing values:",
                ["Fill with Mean", "Fill with Median", "Fill with Mode", "Drop Rows"]
            )
            if st.button("Apply Globally"):
                for col in missing_columns.index:
                    if global_method == "Fill with Mean" and st.session_state['df'][col].dtype in ['float64', 'int64']:
                        st.session_state['df'][col] = st.session_state['df'][col].fillna(st.session_state['df'][col].mean())
                    elif global_method == "Fill with Median" and st.session_state['df'][col].dtype in ['float64', 'int64']:
                        st.session_state['df'][col] = st.session_state['df'][col].fillna(st.session_state['df'][col].median())
                    elif global_method == "Fill with Mode":
                        mode = st.session_state['df'][col].mode()
                        if not mode.empty:
                            st.session_state['df'][col] = st.session_state['df'][col].fillna(mode[0])
                    elif global_method == "Drop Rows":
                        st.session_state['df'] = st.session_state['df'].dropna(subset=[col])
                st.success(f"Applied '{global_method}' to all columns with missing values.")
    else:
        st.info("No missing values found.")

# Define the remove_weird_characters function globally

def remove_weird_characters(text):
    if isinstance(text, str):
        return ''.join([i if ord(i) < 128 else ' ' for i in text])
    return text

# Remove Weird Characters
if current_step == "Remove Weird Characters" and 'df' in st.session_state:
    st.subheader('Check for Weird Characters')

    # Check for weird characters
    weird_characters_found = {}
    for col in st.session_state['df'].select_dtypes(include=['object']).columns:
        weird_characters_rows = st.session_state['df'][col].apply(lambda x: isinstance(x, str) and bool(re.search('[^\x00-\x7F]+', x)))
        if weird_characters_rows.any():
            weird_characters_found[col] = st.session_state['df'][weird_characters_rows]

    if weird_characters_found:
        st.write("### Columns with Weird Characters")
        for col, rows in weird_characters_found.items():
            st.write(f"Column: {col}")
            st.write(rows)

        # Option to search column-by-column or globally
        search_scope = st.radio("Search Scope", ["Global", "Column-by-Column"], key="weird_search_scope")

        if search_scope == "Column-by-Column":
            selected_column = st.selectbox("Select a column to remove weird characters:", list(weird_characters_found.keys()))
            if st.button("Remove Weird Characters from Selected Column"):
                st.session_state['df'][selected_column] = st.session_state['df'][selected_column].apply(remove_weird_characters)
                st.success(f"Removed weird characters from column {selected_column}.")
        else:
            if st.button("Remove Weird Characters Globally"):
                for col in weird_characters_found.keys():
                    st.session_state['df'][col] = st.session_state['df'][col].apply(remove_weird_characters)
                st.success("Removed weird characters from all columns.")
    else:
        st.info("No weird characters found.")

# Remove Duplicates
if current_step == "Remove Duplicates" and 'df' in st.session_state:
    st.subheader('Check for Duplicates')

    # Check for duplicates
    duplicate_summary = {}
    for col in st.session_state['df'].columns:
        duplicate_count = st.session_state['df'][col].duplicated(keep=False).sum()
        if duplicate_count > 0:
            duplicate_summary[col] = duplicate_count

    if duplicate_summary:
        st.write("### Columns with Duplicates")
        st.write(duplicate_summary)

        # Option to search column-by-column or globally
        search_scope = st.radio("Search Scope", ["Global", "Column-by-Column"], key="duplicate_search_scope")

        if search_scope == "Column-by-Column":
            selected_column = st.selectbox("Select a column to handle duplicates:", list(duplicate_summary.keys()))
            duplicate_action = st.radio(
                "How would you like to handle duplicates?",
                ["Keep First", "Keep Last", "Remove All"]
            )
            if st.button("Apply to Selected Column"):
                if duplicate_action == "Keep First":
                    st.session_state['df'] = st.session_state['df'].drop_duplicates(subset=[selected_column], keep='first')
                elif duplicate_action == "Keep Last":
                    st.session_state['df'] = st.session_state['df'].drop_duplicates(subset=[selected_column], keep='last')
                elif duplicate_action == "Remove All":
                    st.session_state['df'] = st.session_state['df'][~st.session_state['df'][selected_column].duplicated(keep=False)]
                st.success(f"Duplicates in column '{selected_column}' handled: {duplicate_action}.")
        else:
            duplicate_action = st.radio(
                "How would you like to handle duplicates globally?",
                ["Keep First", "Keep Last", "Remove All"]
            )
            if st.button("Apply Globally"):
                if duplicate_action == "Keep First":
                    st.session_state['df'] = st.session_state['df'].drop_duplicates(keep='first')
                elif duplicate_action == "Keep Last":
                    st.session_state['df'] = st.session_state['df'].drop_duplicates(keep='last')
                elif duplicate_action == "Remove All":
                    st.session_state['df'] = st.session_state['df'][~st.session_state['df'].duplicated(keep=False)]
                st.success(f"Duplicates handled globally: {duplicate_action}.")
    else:
        st.info("No duplicates found.")

    st.write("Preview after handling duplicates:")
    st.write(st.session_state['df'].head(10))

# Download Cleaned Data
if current_step == "Download Cleaned Data" and 'df' in st.session_state:
    st.subheader('Download Cleaned Data')
    cleaned_csv = st.session_state['df'].to_csv(index=False)
    st.download_button(
        label="Download Cleaned CSV",
        data=cleaned_csv,
        file_name='cleaned_data.csv',
        mime='text/csv'
    )
    st.balloons()
