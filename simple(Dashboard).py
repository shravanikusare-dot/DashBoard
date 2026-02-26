import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data Dashboard", layout="wide")

st.title("📊 Interactive Data Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:

    # Load data
    df = pd.read_csv(uploaded_file)

    # 🔥 Fix MultiIndex / duplicate index issue
    df = df.reset_index(drop=True)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Info")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Shape:", df.shape)

    with col2:
        st.write("Columns:", list(df.columns))

    st.subheader("Basic Statistics")
    st.write(df.describe())

    # Column Selection
    column = st.selectbox("Select Column for Visualization", df.columns)

    # Create Plot
    fig, ax = plt.subplots()

    # If categorical → Countplot
    if df[column].dtype == "object":
        sns.countplot(x=column, data=df, ax=ax)
        plt.xticks(rotation=45)

    # If numeric → Histogram
    else:
        sns.histplot(df[column], kde=True, ax=ax)

    st.pyplot(fig)

    # Correlation Heatmap (Only numeric)
    st.subheader("Correlation Heatmap")

    numeric_df = df.select_dtypes(include=["int64", "float64"])

    if not numeric_df.empty:
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax2)
        st.pyplot(fig2)
    else:
        st.write("No numeric columns available for correlation heatmap.")

else:
    st.info("Please upload a CSV file to start.")