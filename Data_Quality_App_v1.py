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
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns

    if len(numeric_columns) > 0 or len(categorical_columns) > 0:
        plot_type = st.selectbox("Select Plot Type", ["Scatterplot", "Bar Chart", "Pie Chart"], key="plot_type")

        if plot_type == "Scatterplot":
            st.write("Select columns for the scatterplot:")
            x_axis = st.selectbox("X-axis", numeric_columns, key="scatter_x")
            y_axis = st.selectbox("Y-axis", numeric_columns, key="scatter_y")

            if x_axis and y_axis:
                fig, ax = plt.subplots()
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
                ax.set_title(f"Scatterplot of {x_axis} vs {y_axis}")
                st.pyplot(fig)

        elif plot_type == "Bar Chart":
            st.write("Select a categorical column and a numeric column for the bar chart:")
            bar_column = st.selectbox("Categorical Column", categorical_columns, key="bar_column")
            numeric_column = st.selectbox("Numeric Column", numeric_columns, key="bar_numeric")
            agg_function = st.selectbox("Aggregation Function", ["Count", "Sum", "Mean", "Median"], key="bar_agg")

            if bar_column and numeric_column:
                if agg_function == "Count":
                    aggregated_data = df[bar_column].value_counts()
                elif agg_function == "Sum":
                    aggregated_data = df.groupby(bar_column)[numeric_column].sum()
                elif agg_function == "Mean":
                    aggregated_data = df.groupby(bar_column)[numeric_column].mean()
                elif agg_function == "Median":
                    aggregated_data = df.groupby(bar_column)[numeric_column].median()

                fig, ax = plt.subplots()
                aggregated_data.plot(kind='bar', ax=ax, color='skyblue')
                ax.set_title(f"Bar Chart of {bar_column} ({agg_function} of {numeric_column})")
                ax.set_ylabel(agg_function)
                st.pyplot(fig)

        elif plot_type == "Pie Chart":
            st.write("Select a categorical column and a numeric column for the pie chart:")
            pie_column = st.selectbox("Categorical Column", categorical_columns, key="pie_column")
            numeric_column = st.selectbox("Numeric Column", numeric_columns, key="pie_numeric")
            agg_function = st.selectbox("Aggregation Function", ["Count", "Sum", "Mean", "Median"], key="pie_agg")

            if pie_column and numeric_column:
                if agg_function == "Count":
                    aggregated_data = df[pie_column].value_counts()
                elif agg_function == "Sum":
                    aggregated_data = df.groupby(pie_column)[numeric_column].sum()
                elif agg_function == "Mean":
                    aggregated_data = df.groupby(pie_column)[numeric_column].mean()
                elif agg_function == "Median":
                    aggregated_data = df.groupby(pie_column)[numeric_column].median()

                fig, ax = plt.subplots()
                aggregated_data.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
                ax.set_title(f"Pie Chart of {pie_column} ({agg_function} of {numeric_column})")
                ax.set_ylabel("")  # Hide the default y-axis label
                st.pyplot(fig)
    else:
        st.write("No suitable columns available for plotting.")

else:
    st.info("⬆️ Please upload a CSV file to get started!")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
