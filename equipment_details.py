import streamlit as st
import pandas as pd

st.markdown("""
    <h1 style='text-align: center; color: #1F618D; font-size: 40px;'>
        ⚡ Power Plant Configuration Selector
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <h2 style='color: #1F618D; font-size: 32px;'>
        📊 Select equipment
    </h2>
""", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"], label_visibility="collapsed")

def get_biss_lines (data):
    return (data[data["Group"] == "Business  Line"]["Description"].unique())

def get_pp_type (data):
    return (data[data["Group"] == "Power Plant Type"]["Description"].unique())

def get_equipment (data):
    return (data[data["Group"] == "Equipments"]["Description"].unique())

def get_data_req(data):
    return (data[data["Group"] == "Data Required"]["Description"].unique())

num_data = st.number_input("How many equipments do you want to choose?", 1, 100, 1)

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file, sheet_name="Key")  # Reads the first sheet
    biss_lines_sym = []
    pp_types_sym = []
    sel_equipments = []
    equ_syms = []

    for i in range(int(num_data)):
        st.markdown(f"#### equipment {i+1}")
        ## select the buisiness lines
        biss_lines = get_biss_lines(data)
        selected_biss_line = st.selectbox("Select Business Lines:", biss_lines , key=f"biss_{i+1}")
        selected_biss_line_sym = data[data["Description"] == selected_biss_line]["symbol"].iloc[0]
        biss_lines_sym.append(selected_biss_line_sym)

        ## select the power plant type
        pp_types = get_pp_type(data)
        selected_pp_type = st.selectbox("Select powerplant type:", pp_types , key=f"pp_{i+1}")
        selected_pp_type_sym = data[data["Description"] == selected_pp_type]["symbol"].iloc[0]
        pp_types_sym.append(selected_pp_type_sym)

        ## select the equipment
        equipments = get_equipment(data)
        selected_equipment = st.selectbox("Select equipment:", equipments , key=f"eq_{i+1}")
        selected_equ_sym = data[data["Description"] == selected_equipment]["symbol"].iloc[0]
        sel_equipments.append(selected_equipment)
        equ_syms.append(selected_equ_sym)

    if st.button("Next"):
        st.session_state["biss_line"] = biss_lines_sym
        st.session_state["pp_type"] = pp_types_sym
        st.session_state["equipment_sym"] = equ_syms
        st.session_state["equipment"] = sel_equipments
        st.session_state["data"] = uploaded_file
        st.switch_page("pages/equipment_specifications.py")
        



