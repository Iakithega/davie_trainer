import streamlit as st
from utils.utils import *
from utils.data_engineering import complete_data_wrangeling
from utils.plotting_functions import rec_overview_plot
import os.path
from PIL import Image
import configparser
import random
import time

# hides the header - also possible to hide the footer: footer {visibility: hidden;}  /* Hides the footer */
hide_st_style ="""
    <style>
        header.st-emotion-cache-1n4a2v9 {visibility: hidden;}  /* Hides the Streamlit header element identified in the console */ 
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)  

st.write("# The Game")
# v_spacer(height=5, sb=False)


config_path = os.path.join("utils", "paths.ini")
creature_images_path = os.path.join("media", "pics_of_creatures")
creature_already_won_images_path = os.path.join("media", "pics_of_creatures", "already_won_creatures")
creature_question_mark_image_path = os.path.join("media", "pics_of_creatures", "backup", "creature_question_mark.png")


# Initialize session state for controlling the game and storing last images
if 'start' not in st.session_state:
    st.session_state.start = False
if 'last_image' not in st.session_state:
    st.session_state.last_image = creature_question_mark_image_path  # Set question mark as the default initial image
if 'last_image_name' not in st.session_state:
    st.session_state.last_image_name = "???"  # Default name for question mark


@st.cache_data
def load_image_paths(creature_images_path):
    # Get all image files in the media folder (assuming .jpg and .png formats)
    image_paths = {}
    for filename in os.listdir(creature_images_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            key = os.path.splitext(filename)[0]
            full_path = os.path.join(creature_images_path, filename)
            image_paths[key] = full_path
    return image_paths

# Load and cache image paths
creature_image_paths = load_image_paths(creature_images_path)


col_start_button, col_image, col_stop_button = st.columns([1,2,1], gap="large", vertical_alignment="center")

with col_image:
    # placeholder_image_text = st.empty()
    col_inside_img_start, col_inside_img_gap, col_inside_img_stop = st.columns([15, 70, 10], gap="large", vertical_alignment="center")
    
    # Start and Stop buttons
    with col_inside_img_start:
        start_button = st.button("Start")
    with col_inside_img_stop:
        stop_button = st.button("Stop")
    placeholder_image = st.empty()  # Placeholder for the image display
    placeholder_image_text = st.empty()
        

# Update session state based on button clicks
if start_button:
    st.session_state.start = True
if stop_button:
    st.session_state.start = False




# Spinning through random images
if st.session_state.start:
    while st.session_state.start:
        # Pick a random image name
        name = random.choice(list(creature_image_paths.keys()))
        
        # Display image and name in the placeholder
        placeholder_image.image(creature_image_paths[name], use_column_width='auto')
        
        # Store the last displayed image in session state
        st.session_state.last_image = creature_image_paths[name]
        st.session_state.last_image_name = name
        
        time.sleep(0.1)  # Control the speed of spinning
        
        # Stop spinning if "Stop" button is pressed
        if not st.session_state.start:
            break


# Display the question mark image if the game has not started, or show the last image when stopped
if not st.session_state.start:
    placeholder_image.image(st.session_state.last_image, use_column_width='auto')
    placeholder_image_text.markdown(f"## {st.session_state.last_image_name.upper()}")
























# Call the function to cache the data
# data, monthly_stats_data = load_and_process_data() 




# # overview of the datas in a dataframe after Data Wrangeling 
# with st.expander("Raw Table monthly stats"): 
#     st.dataframe(monthly_stats_data)
# v_spacer(height=7, sb=False)



