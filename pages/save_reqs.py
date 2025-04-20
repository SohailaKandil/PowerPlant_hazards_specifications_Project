import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from io import BytesIO

# Let the user input a description for the top row
user_description = st.text_input("Enter a sheet description (will be added above the column headers)")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"], label_visibility="collapsed")

if uploaded_file:
    try:
        # Load the workbook
        in_memory_file = BytesIO(uploaded_file.read())
        wb = load_workbook(in_memory_file)
        ws = wb.active

        # Insert a new top row for the description (this shifts everything down)
        ws.insert_rows(1)
        ws.cell(row=1, column=1, value=user_description)  # Add description to A1

        # Continue if session data exists
        if "selected_data" in st.session_state:
            # Find the next empty row starting from row 3 (since headers are now in row 2)
            start_row = 3
            for row in range(start_row, ws.max_row + 1):
                if ws.cell(row=row, column=1).value is None and ws.cell(row=row, column=2).value is None:
                    next_empty_row = row
                    break
            else:
                next_empty_row = ws.max_row + 1

            # Insert session data
            for item, desc in zip(st.session_state["selected_data"], st.session_state["selected_data_desc"]):
                ws.cell(row=next_empty_row, column=1, value=item)
                ws.cell(row=next_empty_row, column=2, value=desc)
                next_empty_row += 1

        # Save and prepare for download
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        st.success("✅ Description and data written successfully.")

        st.download_button(
            label="📥 Download Updated Excel File",
            data=output,
            file_name="updated_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("📤 Please upload your Excel file first.")
