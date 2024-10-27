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
if 'selected_images' not in st.session_state:
    st.session_state.selected_images = []  # Track already selected images


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
# Available images list (excluding selected ones)
available_images = {k: v for k, v in creature_image_paths.items() if k not in st.session_state.selected_images}



gap1_img_firstline, col_image, gap2_img_firstline = st.columns([1,2,1], gap="large", vertical_alignment="center")
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

with gap1_img_firstline:
    placeholder_available = st.empty()

with gap2_img_firstline:
    placeholder_selected = st.empty()

        

# Update session state based on button clicks
if start_button:
    st.session_state.start = True
if stop_button:
    st.session_state.start = False

############################################################################################



# Spinning through random images
if st.session_state.start and available_images:
    while st.session_state.start:
        # Pick a random image name from available images
        name = random.choice(list(available_images.keys()))
        
        # Display image and name in the placeholder
        placeholder_image.image(available_images[name], use_column_width='auto')
        
        # Store the last displayed image in session state
        st.session_state.last_image = available_images[name]
        st.session_state.last_image_name = name
        
        time.sleep(0.1)  # Control the speed of spinning
        
        # Stop spinning if "Stop" button is pressed
        if not st.session_state.start:
            break

# Display the last selected image and update selected list
if not st.session_state.start:
    placeholder_image.image(st.session_state.last_image, use_column_width='auto')
    placeholder_image_text.markdown(
        f"<h2 style='text-align: center;'>{st.session_state.last_image_name.upper()}</h2>", 
        unsafe_allow_html=True
                                    )    
    # Add the selected image to the list of already chosen images if not already there
    if st.session_state.last_image_name not in st.session_state.selected_images:
        st.session_state.selected_images.append(st.session_state.last_image_name)
        # placeholder_available.write(available_images)
        # placeholder_selected.write(st.session_state.selected_images)

    # Update available images to exclude already selected ones
    available_images = {k: v for k, v in creature_image_paths.items() if k not in st.session_state.selected_images}

    # Notify user when all images are selected
    if not available_images:
        st.write("All images have been selected! Click 'Reset Game' to play again.")


