import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("🔍 Interactive Data Explorer")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    st.subheader("📊 Data Summary")
    st.write(df.describe())

    # Select columns for filtering
    st.subheader("🎯 Filter Your Data")
    selected_column = st.selectbox("Select a column to filter", df.columns)

    unique_values = df[selected_column].unique()
    selected_value = st.selectbox(f"Select a value from {selected_column}", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(f"Filtered data based on {selected_column} = {selected_value}")
    st.dataframe(filtered_df)

    # Simple visualization
    st.subheader("📈 Quick Visualization")
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

    if len(numeric_columns) > 0:
        col_to_plot = st.selectbox("Choose a numeric column to plot", numeric_columns)
        fig, ax = plt.subplots()
        sns.histplot(df[col_to_plot], kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.write("No numeric columns available for plotting.")

else:
    st.info("⬆️ Please upload a CSV file to get started!")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
