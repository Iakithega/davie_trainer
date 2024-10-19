import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

import matplotlib.dates as mdates
from datetime import datetime

from utils.utils import *
from utils.data_engineering import *
from utils.plotting_functions import *

papath = os.path.join("..", "media", "wallpaper", "transformers1.png")


# Path to your local folder containing images
# image_folder = r'media\wallpaper'

# # Get the list of image files from the folder
# image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('png', 'jpg', 'jpeg'))]

# # Select a random image from the folder
# def get_random_image():
#     return random.choice(image_paths)

# image_path = random.choice(image_paths)


# Set the background image  ###https://images.unsplash.com/photo-1542281286-9e0a16bb7366
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



# hides the header - also possible to hide the footer: footer {visibility: hidden;}  /* Hides the footer */
hide_st_style ="""
    <style>
        header.st-emotion-cache-1n4a2v9 {visibility: hidden;}  /* Hides the Streamlit header element identified in the console */ 
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)  



st.title("David Train")

# calculate the current date for plots
start_date = "2024.08.10"
# Get the current date
current_date = datetime.today() + timedelta(days=3)
# Format the date as 'YYYY-MM-DD'
current_date = current_date.strftime('%Y-%m-%d')


# load the data
initial_data = load_raw_excel(path_to_excel)
# run all the data wrangeling files
data, monthly_stats_data = complete_data_wrangeling(initial_data)


# overview of the datas in a dataframe after Data Wrangeling 
with st.expander("Raw Table"): 
    st.dataframe(data)

v_spacer(height=7, sb=False)



fig_pushup = pushup_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_pushup)

v_spacer(height=2, sb=False)

fig_planke = plank_plot(data, start_date, current_date)
st.pyplot(fig_planke)

v_spacer(height=2, sb=False)

fig_kniebeuge = kniebeuge_plot(data, start_date, current_date)
st.pyplot(fig_kniebeuge)

v_spacer(height=2, sb=False)

fig_hammercurl = hamcurls_plot(data, start_date, current_date)
st.pyplot(fig_hammercurl)

v_spacer(height=2, sb=False)

fig_turmrud = turmrud_plot(data, start_date, current_date)
st.pyplot(fig_turmrud)

v_spacer(height=2, sb=False)

fig_turmzg = turmzg_plot(data, start_date, current_date)
st.pyplot(fig_turmzg)


