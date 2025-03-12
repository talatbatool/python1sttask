import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: black;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# Title and Description
st.title("💽 Data Sweeper Sterling Integrator By Sayyed Jalees")
st.write("Upload your CSV or Excel file, clean the data, and convert it as needed!")

# File Uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx", "xls"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext in [".xlsx", ".xls"]:
                df = pd.read_excel(file, engine='openpyxl')

            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue

            # Display file details
            st.write(f"**File Name:** {file.name}")
            
            # Preview Data
            st.write("🔍 Preview of Data:")
            st.dataframe(df.head())

            # Data Cleaning Options
            st.subheader("🛠️ Data Cleaning Options")
            if st.checkbox(f"Clean data for {file.name}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"Remove Duplicates for {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.success("✅ Duplicates removed successfully!")

                with col2:
                    if st.button(f"Fill missing values for {file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✅ Missing values filled successfully!")

            # Column Selection
            st.subheader("🎯 Select Columns to Keep")
            columns = st.multiselect(f"Select columns to keep for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Visualize data for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # Conversion Options
            st.subheader("🔄 Convert File")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()

                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    file_name = file.name.replace(file_ext, ".xls")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)

                st.download_button(
                    label=f"Download {file_name} as {conversion_type}", 
                    data=buffer, 
                    file_name=file_name, 
                    mime=mime_type
                )
        
        except Exception as e:
            st.error(f"Error processing file {file.name}: {e}")

st.success("🎉 All files processed successfully!")