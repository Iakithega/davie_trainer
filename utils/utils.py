import streamlit as st
import pandas as pd
import os
import base64

cwd = os.getcwd()

# from streamlit_lottie import st_lottie
# import requests

# function for creating space between elements
def v_spacer(height, sb=False) -> None:
    for _ in range(height):
        if sb:
            st.sidebar.write('\n')
        else:
            st.write('\n')

path_to_excel = os.path.join(cwd, "data", "davie_trainingsplan_2014.xlsx")

def load_raw_excel(path: str):
    data = pd.read_excel(path_to_excel, 
                         header=0, 
                         index_col="Datum", 
                         parse_dates=True)
    return data


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background_css(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    [data-testid="stMain"] {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def hide_header_css():
    hide_st_style ="""
    <style>
        header.st-emotion-cache-1n4a2v9 {visibility: hidden;}  /* Hides the Streamlit header element identified in the console */ 
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)  



def set_wide_layout_config():
    st.set_page_config(
        #  page_title="RHEALIZER!",
        #  page_icon="🤖", 
        layout="wide",
        initial_sidebar_state="expanded",
    )

def set_streamlit_page_config_once():
    try:
        st.set_page_config(layout="wide",
                           initial_sidebar_state="expanded",
                           page_title="Davie Titanchik",
                           )
    except st.errors.StreamlitAPIException as e:
        if "can only be called once per app" in e.__str__():
            # ignore this error
            return
        raise e
