import streamlit as st
import json
import configparser
import pandas as pd

# from streamlit_lottie import st_lottie
# import requests

# function for creating space between elements
def v_spacer(height, sb=False) -> None:
    for _ in range(height):
        if sb:
            st.sidebar.write('\n')
        else:
            st.write('\n')

path_to_excel = "data\davie trainingsplan 2014.xlsx"

def load_raw_excel(path: str):
    data = pd.read_excel(path_to_excel, 
                         header=0, 
                         index_col="Datum", 
                         parse_dates=True)
    return data