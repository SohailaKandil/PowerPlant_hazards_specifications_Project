import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from io import BytesIO

# Let the user input values to be added to the first row
user_input_item = st.text_input("Enter Item (Column A)")
user_input_desc = st.text_input("Enter Description (Column B)")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"], label_visibility="collapsed")

if uploaded_file:
    try:
        # Load the workbook from uploaded file
        in_memory_file = BytesIO(uploaded_file.read())
        wb = load_workbook(in_memory_file)
        ws = wb.active  # Or use wb['SheetName'] if needed

        # Write to the first row (row=1)
        if user_input_item or user_input_desc:
            ws.cell(row=1, column=1, value=user_input_item)
            ws.cell(row=1, column=2, value=user_input_desc)

        # If you still want to use selected_data from session state:
        if "selected_data" in st.session_state:
            # Find first empty row starting from row 2
            start_row = 2
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

        # Save to memory for download
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        st.success("✅ Data written to Excel successfully.")

        # Download button
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
