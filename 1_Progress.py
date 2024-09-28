import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import matplotlib.dates as mdates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from datetime import datetime

from utils.utils import *
from utils.data_engineering import *
from utils.plotting_functions import *







# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

# st.text_input("", placeholder="Streamlit CSS ")

input_style = """
<style>
input[type="text"] {
    background-color: transparent;
    color: #a19eae;  // This changes the text color inside the input box
}
div[data-baseweb="base-input"] {
    background-color: transparent !important;
}
[data-testid="stAppViewContainer"] {
    background-color: transparent !important;
}
</style>
"""
st.markdown(input_style, unsafe_allow_html=True)


#######################################################################################################################

# original_title = '<h1 style="font-family: serif; color:white; font-size: 20px;">Streamlit CSS Styling✨ </h1>'
# st.markdown(original_title, unsafe_allow_html=True)

#############################################################################################################################


# #remove logo
# hide_st_style = """
#             <style>
#              footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)  

st.title("David Train")



start_date = "2024.08.10"
# Get the current date
current_date = datetime.today() + timedelta(days=3)
# Format the date as 'YYYY-MM-DD'
current_date = current_date.strftime('%Y-%m-%d')

# load the data
initial_data = load_raw_excel(path_to_excel)

# extract weights and reps and band strength
data = weight_reps_exctracter(initial_data)


# calculate no weight averages, max and sum for liegestütze, planke and kniebeugen
data = calc_sets_overview_no_weights(data)

# calculate no weight averages, max and sum for weighted Hammer Curls, and Turm Zug
data = calc_sets_overview_with_weights(data)

# implements weight factored score column for hammer curls
data = compute_hammer_curls_scores(data)
data = calc_hammer_curls_score_overview(data)

# implements weight factored score column for Turm Rudern
data = compute_trmrd_scores(data)
data = calc_trmrd_score_overview(data)

# implements weight factored score column for Turm Zug
data = compute_trmzg_scores(data)
data = calc_trmzg_score_overview(data)

# calculate no weight averages, max and sum for distanced Turm Rudern
data = calc_sets_overview_with_weights_dstanced(data)


with st.expander("Raw Table"): 
    st.dataframe(data)

v_spacer(height=4, sb=False)



# col1_params_normal_plot, col2_params_normal_plot = st.columns([3, 2], gap="large")
# #show here the elements with columns for normal plot
# with col1_params_normal_plot:
#     all_exersices = [column_name for column_name in data.columns]
#     selected_exersices = st.multiselect("Choose exersices", all_exersices)


v_spacer(height=4, sb=False)


fig_pushup = pushup_plot(data, start_date, current_date)
st.pyplot(fig_pushup)

fig_planke = plank_plot(data, start_date, current_date)
st.pyplot(fig_planke)

fig_kniebeuge = kniebeuge_plot(data, start_date, current_date)
st.pyplot(fig_kniebeuge)

fig_hammercurl = hamcurls_plot(data, start_date, current_date)
st.pyplot(fig_hammercurl)

fig_turmrud = turmrud_plot(data, start_date, current_date)
st.pyplot(fig_turmrud)

fig_turmzg = turmzg_plot(data, start_date, current_date)
st.pyplot(fig_turmzg)


