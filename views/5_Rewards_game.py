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

@st.cache_data
def load_and_process_data():
    initial_data = load_raw_excel(path_to_excel)
    data, monthly_stats_data = complete_data_wrangeling(initial_data)
    return data, monthly_stats_data



config_path = os.path.join("utils", "paths.ini")
creature_images_path = os.path.join("media", "pics_of_creatures")

# @st.cache_data
# def load_all_images(config_file=config_path):
#     # Read paths from the ini file
#     config = configparser.ConfigParser()
#     config.read(config_file)

#         # Ensure the section [img_paths] exists
#     if 'img_paths' not in config:
#         raise ValueError("Section 'img_paths' not found in the config file.")
    
#     # Dictionary to store the images
#     images = {}
#     for key, path in config['img_paths'].items():
#         try:
#             images[key] = Image.open(path)  # Load the image and store it in the dictionary
#         except FileNotFoundError:
#             raise FileNotFoundError(f"Image at path '{path}' not found.")
    
#     return images


# # load images
# images = load_all_images(config_path)
# push_pic, knbg_pic, plnk_pic, hmcrl_pic, tmrd_pic, tmzg_pic = (images['push_pic'], images['knbg_pic'], images['plnk_pic'],
#                                                                images['hmcrl_pic'],images['tmrd_pic'], images['tmzg_pic'])

@st.cache_data
def load_image_paths(creature_images_path=creature_images_path):
    # Get all image files in the media folder (assuming .jpg and .png formats)
    image_paths = {}
    for filename in os.listdir(creature_images_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Use the filename as the key and the full path as the value
            key = os.path.splitext(filename)[0]
            full_path = os.path.join(creature_images_path, filename)
            image_paths[key] = full_path
    
    return image_paths

# Bildpfade laden und cachen
creature_image_paths = load_image_paths(creature_images_path)


# UI: Image Carousel
st.title("Image Carousel")

# "Stop" button
stop_button = st.button("Stop")

# Random order of images
image_names = list(creature_image_paths.keys())
random.shuffle(image_names)


col1, col2, col3 = st.columns([1,1,1], gap="large")
with col2:
    v_spacer(5, False)
    placeholder = st.empty()
    for name in image_names:
        placeholder.image(creature_image_paths[name], use_column_width='auto')
        st.markdown(f'{name}')
        time.sleep(0.2)


# # Start carousel
# stop = False
# for key in image_keys:
#     if stop_button:
#         stop = True
#     if stop:
#         st.image(creature_image_paths[key], caption=key)
#         break
#     st.image(creature_image_paths[key], caption=key)
#     time.sleep(0.5)

# # Show the selected image after stopping
# if stop:
#     st.write(f"Selected Image: {key}")


# # UI: Bild-Karussell
# st.title("Bild-Karussell")

# # "Stopp"-Button
# stop_button = st.button("Stopp")

# # Zufällige Reihenfolge der Bildpfade generieren
# image_keys = list(image_paths.keys())
# random.shuffle(image_keys)

# # Karussell starten
# stop = False
# for key in image_keys:
#     if stop_button:
#         stop = True
#     if stop:
#         st.image(image_paths[key], caption=key)
#         break
#     st.image(image_paths[key], caption=key)
#     time.sleep(0.5)

# # Letztes ausgewähltes Bild anzeigen
# if stop:
#     st.write(f"Ausgewähltes Bild: {key}")













# Call the function to cache the data
data, monthly_stats_data = load_and_process_data() 




# # overview of the datas in a dataframe after Data Wrangeling 
# with st.expander("Raw Table monthly stats"): 
#     st.dataframe(monthly_stats_data)
# v_spacer(height=7, sb=False)



