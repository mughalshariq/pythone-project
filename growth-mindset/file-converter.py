import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        if ext == "csv":
            df = pd.read_csv(file)
        elif ext == "xlsx":
            df = pd.read_excel(file)

            st.subheader(f"{file.name} - Preview")
            st.dataframe(df.head())

            if st.checkbox("Remove Duplicates - {file.name}"):
                df = df.drop_duplicates()
                st.success("Duplicates removed!")
                st.dataframe(df.head())

            if st.checkbox("fill missing values - {file.name}"):
                df = df.fillna(df.select_dtypes(include= ["number"]).mean(), inplace=True)
                st.success("Missing values filled!")
                st.dataframe(df.head())

                selected_columns = st.multiselect("Select columns - {file.name} ", df.columns, default=df.columns())
                df = df[selected_columns]
                st.dataframe(df.head())

            if st.checkbox("show chart - {file.name}") and not df.select_dtypes(include="number").empty:
                st.bar_chart(df.select_dtypes(include="number").iloc[:, 2])

            format_choise = st.radio(f"convert {file.name} to", {"csv","Excel"}, key=file.name)
            if st.button(f"Button {file.name} to {format_choise}"):
                if format_choise == "csv":
                    output = df.to_csv(index=False)
                    st.download_button("Download CSV", output, file_name=f"{file.name}.csv", mime="text/csv")
                elif format_choise == "Excel":
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df.to_excel(writer, index=False, sheet_name="Sheet1")
                    st.download_button("Download Excel", output.getvalue(), file_name=f"{file.name}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                    output.seek(0)
                    st.set_download_button ("Download Excel", output, file_name=f"{file.name}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    st.success("File converted and ready for download!")
            
            



