import streamlit as st
import pandas as pd

if "selected_data" not in st.session_state:
    st.warning("Please go to the Equipment details page first.")
    st.stop()
else:
    st.success("✅ Data selections saved.")
    df = pd.DataFrame(st.session_state["selected_data"], columns=["requirements"])
    df.to_excel("requirements.xlsx", index=False)