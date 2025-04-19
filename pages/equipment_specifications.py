import streamlit as st
import pandas as pd

def get_data_req(data):
    return (data[data["Group"] == "Data Required"]["Description"].unique())

st.markdown("""
    <h2 style='color: #1F618D; font-size: 32px;'>
        📊 Select Data Required
    </h2>
""", unsafe_allow_html=True)

# Check for previous session data
if "biss_line" not in st.session_state or "pp_type" not in st.session_state or "equipment" not in st.session_state or "equipment_sym" not in st.session_state or "data" not in st.session_state:
    st.warning("Please go to the Equipment details page first.")
    st.stop()

uploaded_file = st.session_state["data"]
key_page = pd.read_excel(uploaded_file, sheet_name="Key")

num_equipments = len(st.session_state["equipment"])
if not all(
    len(st.session_state[key]) == num_equipments
    for key in ["biss_line", "pp_type", "equipment_sym"]
):
    st.error("Session state mismatch. Please go back and reselect equipment.")
    st.stop()
data_selections = []

for j , equipment in enumerate(st.session_state["equipment"]):
    try:
        data_page = pd.read_excel(uploaded_file, sheet_name=str(equipment))
    except:
        st.markdown(f"""
            <h3 style='font-size: 20px; color: green;'>
                Selected Equipment: {equipment}
            </h3>
        """, unsafe_allow_html=True)
        st.warning(f"Please add a sheet for {equipment}")
        continue

    st.markdown(f"""
        <h3 style='font-size: 20px; color: green;'>
            Selected Equipment: {equipment}
        </h3>
    """, unsafe_allow_html=True)

    # Get data required
    data_reqs = get_data_req(key_page)

    # Number of data items to choose
    num_data = st.number_input("How many data items do you want to choose?", 1, 100, 1 , key=f"num_data_{j}")

    for i in range(int(num_data)):
        st.markdown(f"""
            <h6 style='font-size: 20px; color: #1F618D;'>
                Data required number {i+1}
            </h6>
        """, unsafe_allow_html=True)
        selected_req = st.selectbox(f"Select data requirement #{i+1}:", data_reqs, key=f"req_{i}{j}")
        selected_req_sym = key_page[key_page["Description"] == selected_req]["symbol"].iloc[0]

        # Get sub-options (assuming they are linked by 'Parent' column)
        sub_opts = data_page[data_page["Data Reqired"] == selected_req_sym]["Column1"].unique()
        selected_sub_req = st.selectbox(f"Select sub data requirement #{i+1}:", sub_opts , key=f"sub_req_{i}{j}")
        sub_opts_sym = data_page[data_page["Column1"] == selected_sub_req]["Column2"].iloc[0]

        selection = str(st.session_state["biss_line"][j])+"-"+str(st.session_state["pp_type"][j])+"-"+str(st.session_state["equipment_sym"][j])+"-"+str(selected_req_sym)+"-"+str(sub_opts_sym)
        data_selections.append(selection)

if st.button("Finish"):
    st.session_state["selected_data"] = data_selections
    st.switch_page("pages/save_reqs.py")