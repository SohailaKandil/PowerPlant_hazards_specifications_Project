import streamlit as st
import pandas as pd
from openpyxl import load_workbook

output_file = "output.xlsx"

if "selected_data" not in st.session_state:
    st.warning("Please go to the Equipment details page first.")
    st.stop()
else: 
    try:
        # Load workbook and sheet
        wb = load_workbook(output_file)
        ws = wb.active  # Or use wb['SheetName'] if needed

        # Start looking for the first empty row after the header (assumes headers in row 1)
        start_row = 2
        for row in range(start_row, ws.max_row + 1):
            if ws.cell(row=row, column=1).value is None and ws.cell(row=row, column=2).value is None:
                next_empty_row = row
                break
        else:
            next_empty_row = ws.max_row + 1  # In case all rows are filled

        # Write data to empty rows
        for item, desc in zip(st.session_state["selected_data"], st.session_state["selected_data_desc"]):
            ws.cell(row=next_empty_row, column=1, value=item)
            ws.cell(row=next_empty_row, column=2, value=desc)
            next_empty_row += 1

        # Save changes
        wb.save(output_file)
        st.success("✅ Data selections saved to the formatted sheet.")
    
    except PermissionError:
        st.warning("⚠️ Please close the output file before saving and try again.")
    except Exception as e:
        st.error(f"❌ Error: {e}")