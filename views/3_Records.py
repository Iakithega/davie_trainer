import streamlit as st
from utils.utils import *
from utils.data_engineering import complete_data_wrangeling
from utils.plotting_functions import rec_overview_plot

# hides the header - also possible to hide the footer: footer {visibility: hidden;}  /* Hides the footer */
hide_st_style ="""
    <style>
        header.st-emotion-cache-1n4a2v9 {visibility: hidden;}  /* Hides the Streamlit header element identified in the console */ 
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)  

st.write("# Prices")

@st.cache_data
def load_and_process_data():
    initial_data = load_raw_excel(path_to_excel)
    data, monthly_stats_data = complete_data_wrangeling(initial_data)
    return data, monthly_stats_data

# Call the function to cache the data
data, monthly_stats_data = load_and_process_data() 

# overview of the datas in a dataframe after Data Wrangeling 
with st.expander("Raw Table monthly stats"): 
    st.dataframe(monthly_stats_data)
v_spacer(height=7, sb=False)


fig_rec_overview = rec_overview_plot(data=data, monthly_stats_data=monthly_stats_data)
st.pyplot(fig_rec_overview)
