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

config = configparser.ConfigParser()
config.read("utils/paths.ini")
cwd = os.getcwd()
path_to_excel = os.path.join(cwd, config["paths"]["path_to_excel"])

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
min_date = datetime.strptime("2024.08.10", "%Y.%m.%d")
# Get the current date
current_date = datetime.today() + timedelta(days=3)
last_50_days = datetime.today() - timedelta(days=50)
# Format the date as 'YYYY-MM-DD'
current_date = current_date.strftime('%Y-%m-%d')



# @st.cache_data
def load_and_process_data():
    initial_data = load_raw_excel(path_to_excel)
    data, monthly_stats_data = complete_data_wrangeling(initial_data)
    return data, monthly_stats_data

# Call the function to cache the data
data, monthly_stats_data = load_and_process_data() 


# overview of the datas in a dataframe after Data Wrangeling 
with st.expander("Raw Table all data"): 
    st.dataframe(data)

# overview of the datas in a dataframe after Data Wrangeling 
with st.expander("Raw Table monthly stats"): 
    st.dataframe(monthly_stats_data)
v_spacer(height=5, sb=False)


with st.expander("Adjust time periods"):
    # picking starting date for the plots
    date_col1, date_col2 = st.columns([1, 10])
    with date_col1:
        start_date = st.date_input(label="Start Date for Training Plots", value=last_50_days, min_value=min_date)
        v_spacer(height=2, sb=False)
    with date_col2:
        st.write("TOGGLE for syncing boxplots from Alltime to defined starting time. ALSO CHANGE THE TITLE in BOOXPLOTS FROM ALL TIME TO Selected Time period so it would be clear")



fig_pushup = pushup_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_pushup)
v_spacer(height=2, sb=False)

fig_planke = plank_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_planke)
v_spacer(height=2, sb=False)

fig_kniebeuge = kniebeuge_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_kniebeuge)
v_spacer(height=2, sb=False)

fig_hammercurl = hamcurls_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_hammercurl)
v_spacer(height=2, sb=False)

fig_turmrud = turmrud_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_turmrud)
v_spacer(height=2, sb=False)

fig_turmzg = turmzg_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_turmzg)
v_spacer(height=2, sb=False)


