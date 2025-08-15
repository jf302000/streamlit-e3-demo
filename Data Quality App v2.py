import streamlit as st
import pandas as pd
import numpy as np
import re
import time
import concurrent.futures

# Title of the app
st.title('CSV Data Summary and Cleaning with Feedback')

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

def remove_weird_characters(text):
    # Remove non-ASCII characters
    if isinstance(text, str):
        return ''.join([i if ord(i) < 128 else ' ' for i in text])  # Replace non-ASCII with space
    return text

def clean_column(col):
    # Remove leading/trailing whitespace
    col = col.apply(lambda x: x.strip() if isinstance(x, str) else x)
    # Convert empty strings to NaN
    col = col.replace('', np.nan)
    # Remove weird characters
    if col.dtype == 'object':
        col = col.apply(remove_weird_characters)
        # Unify string case
        col = col.str.lower()
    # Convert inf/-inf to NaN
    if pd.api.types.is_numeric_dtype(col):
        col = col.replace([np.inf, -np.inf], np.nan)
    return col

def handle_missing_values(df, method):
    """Handle missing values in the DataFrame based on the selected method."""
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if method == 'Fill with Mean' and df[col].dtype in ['float64', 'int64']:
                df[col] = df[col].fillna(df[col].mean())
            elif method == 'Fill with Median' and df[col].dtype in ['float64', 'int64']:
                df[col] = df[col].fillna(df[col].median())
            elif method == 'Fill with Mode':
                mode = df[col].mode()
                if not mode.empty:
                    df[col] = df[col].fillna(mode[0])
            elif method == 'Drop Rows':
                df = df.dropna(subset=[col])
    return df

if uploaded_file is not None:
    # Add error handling for file upload
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()
    
    # Store a copy of the original dataframe for comparison
    original_df = df.copy()

    # Try to automatically detect date columns and convert them to datetime
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col], errors='raise')
            except (ValueError, TypeError):
                continue  # If it cannot be converted, leave as is
    
    # Clean all columns in parallel for performance
    with concurrent.futures.ThreadPoolExecutor() as executor:
        cleaned_cols = list(executor.map(clean_column, [df[c] for c in df.columns]))
    df = pd.concat(cleaned_cols, axis=1)
    df.columns = original_df.columns

    # Convert mixed types to string for object columns
    for col in df.select_dtypes(include=['object']).columns:
        try:
            df[col] = df[col].astype(str)
        except Exception:
            pass

    # Display the first few rows of the dataframe
    st.subheader('Data Preview')
    preview_rows = 100 if df.shape[0] > 100 else df.shape[0]
    st.write(df.head(preview_rows))
    
    # Data Summary
    st.subheader('Data Summary')
    st.write(df.describe())
    
    # Data types and missing values
    st.subheader('Data Types and Missing Values')
    # Filter only columns with missing values for Data Types and Missing Values section
    missing_values_columns = df.columns[df.isnull().any()]
    data_info = pd.DataFrame({
        'Data Type': df[missing_values_columns].dtypes,
        'Missing Values': df[missing_values_columns].isnull().sum()
    })
    st.write(data_info)

    # Data Cleaning Section
    st.subheader('Data Cleaning')

    # Add a global option to handle missing values for all columns
    st.write("### Global Missing Value Handling")
    st.selectbox(
        "Select a global method to handle missing values for all columns:",
        ('None', 'Fill with Mean', 'Fill with Median', 'Fill with Mode', 'Drop Rows'),
        key='global_missing_values',
        help="Choose how to handle missing values across all columns."
    )

    global_method = st.session_state.get('global_missing_values', 'None')

    if global_method != 'None':
        df = handle_missing_values(df, global_method)
        st.success(f"Applied global method '{global_method}' to all columns with missing values!")

    # Optimize missing value handling: batch fill
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    object_cols = df.select_dtypes(include=['object']).columns
    if st.button('Auto-Fix Missing Values (Mean/Mode)'):
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        for col in object_cols:
            mode = df[col].mode()
            if not mode.empty:
                df[col] = df[col].fillna(mode[0])
        st.success('Auto-filled missing values for all columns!')

    # Check for remaining missing values
    st.write("### Checking Remaining Missing Values")
    missing_after = df.isnull().sum()
    missing_after = missing_after[missing_after > 0]  # Filter only columns with missing values
    missing_after_df = missing_after.reset_index()
    missing_after_df.columns = ['Column', 'Missing Values']
    st.table(missing_after_df)

    # Detect and remove weird characters (non-ASCII) from object columns
    st.write("### Remove Weird Characters")
    weird_characters_found = {}
    for col in df.select_dtypes(include=['object']).columns:
        weird_characters_rows = df[col].apply(lambda x: isinstance(x, str) and bool(re.search('[^\x00-\x7F]+', x)))
        if weird_characters_rows.any():
            weird_characters_found[col] = df[weird_characters_rows]
            df[col] = df[col].apply(remove_weird_characters)
            st.write(f"Removed weird characters from column '{col}'.")

    # Show preview of affected rows where weird characters were removed
    if weird_characters_found:
        st.write("#### Preview of Rows with Weird Characters Removed")
        for col, rows in weird_characters_found.items():
            st.write(f"Column: {col}")
            st.write(rows)

    # Reintroduce the 'Remove Duplicates' section with improvements
    st.write("### Remove Duplicates")
    remove_duplicates = st.checkbox('Remove Duplicate Rows')

    if remove_duplicates:
        num_duplicates = df.duplicated().sum()
        if num_duplicates > 0:
            df.drop_duplicates(inplace=True)
            st.success(f"Removed {num_duplicates} duplicate rows.")
        else:
            st.info("No duplicate rows found.")

    # Allow the user to download the cleaned CSV
    st.write("### Download Cleaned CSV")
    cleaned_csv = df.to_csv(index=False)
    download_button = st.download_button(
        label="Download Cleaned CSV",
        data=cleaned_csv,
        file_name='cleaned_data.csv',
        mime='text/csv'
    )

    # Add final balloon effect when download is triggered
    if download_button:
        st.balloons()  # Fun balloon effect when download is triggered
