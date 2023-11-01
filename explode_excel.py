# Import necessary libraries
import streamlit as st
import pandas as pd
import base64
from io import BytesIO

# Function to create a download link for the dataframe
def get_excel_download_link(df, filename="transformed_data.xlsx"):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download transformed Excel file</a>'

# Streamlit app
st.title('Excel Column Exploder for Shintia bb')

# Upload the excel file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Read the excel file
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        selected_sheet = st.selectbox('Select a sheet:', sheet_names)
        
        df = xls.parse(selected_sheet)

        # Display the first 5 rows of the dataframe
        st.write('First 5 rows of the uploaded data:')
        st.dataframe(df.head())
        
        # Get the column to explode and the delimiter
        column_to_explode = st.selectbox('Select the column to explode:', df.columns)
        delimiter = st.text_input('Enter the delimiter:', value=',')

        # Explode the column
        df_exploded = df.assign(**{column_to_explode: df[column_to_explode].str.split(delimiter)}).explode(column_to_explode)
        
        st.write('First 5 rows of the transformed data:')
        st.dataframe(df_exploded.head())

        # Offer the transformed dataframe for download
        st.markdown(get_excel_download_link(df_exploded), unsafe_allow_html=True)

    except Exception as e:
        st.write("An error occurred: ", e)

