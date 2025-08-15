import streamlit as st
import pandas as pd

# Streamlit UI setup
st.title('Value Match Checker')

# Upload CSV files
check_file = st.file_uploader("Upload CSV to check values", type="csv")
reference_file = st.file_uploader("Upload CSV for reference", type="csv")

# Check if both files are uploaded
if check_file is not None and reference_file is not None:
    # Load CSV files into pandas DataFrames
    check_df = pd.read_csv(check_file)
    reference_df = pd.read_csv(reference_file)

    # Display the DataFrames
    st.subheader('Check DataFrame')
    st.write(check_df.head())

    st.subheader('Reference DataFrame')
    st.write(reference_df.head())

    # Check if the user has selected the columns
    check_column = st.selectbox("Select the column to check", check_df.columns)
    reference_column = st.selectbox("Select the column to reference", reference_df.columns)

    if st.button('Check for Matches'):
        # Check if values from the check column are in the reference column
        check_df['Match Found'] = check_df[check_column].isin(reference_df[reference_column])
        
        # Display the results
        st.subheader('Match Results')
        st.write(check_df)

        # Option to download the result
        result_csv = check_df.to_csv(index=False)
        st.download_button("Download Match Results", data=result_csv, file_name="match_results.csv", mime="text/csv")
else:
    st.warning("Please upload both files.")
