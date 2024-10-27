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


config_path = os.path.join("utils", "paths.ini")
creature_images_path = os.path.join("media", "pics_of_creatures")
creaturealready_won_images_path = os.path.join("media", "pics_of_creatures", "already_won_creatures")


# Initialize session state for controlling the game and storing last images
if 'start' not in st.session_state:
    st.session_state.start = False
if 'last_image' not in st.session_state:
    st.session_state.last_image = None
if 'last_image_name' not in st.session_state:
    st.session_state.last_image_name = None


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

# Start and Stop buttons
start_button = st.button("Start")
stop_button = st.button("Stop")

# Update session state based on button clicks
if start_button:
    st.session_state.start = True
if stop_button:
    st.session_state.start = False

# Random order of images
image_names = list(creature_image_paths.keys())
random.shuffle(image_names)

# Display area
placeholder = st.empty()  # Placeholder for the image display

# Spinning through images
if st.session_state.start:
    for name in image_names:
        # Display image and name in the placeholder
        placeholder.image(creature_image_paths[name], use_column_width='auto')
        st.markdown(f"{name.upper()}")
        
        # Store the last displayed image in session state
        st.session_state.last_image = creature_image_paths[name]
        st.session_state.last_image_name = name
        
        time.sleep(0.2)  # Control the speed of spinning
        
        # Stop spinning if "Stop" button is pressed
        if not st.session_state.start:
            break

# Display the last image shown when stopped
if not st.session_state.start and st.session_state.last_image:
    placeholder.image(st.session_state.last_image, use_column_width='auto')
    st.markdown(f"{st.session_state.last_image_name.upper()}")


















# # Initialize session state for controlling the game and storing last images
# if 'start' not in st.session_state:
#     st.session_state.start = False
# if 'last_images' not in st.session_state:
#     st.session_state.last_images = {}
# if 'current_tab' not in st.session_state:  
#     st.session_state.current_tab = 0  



# @st.cache_data
# def load_image_paths(creature_images_path=creature_images_path):
#     # Get all image files in the media folder (assuming .jpg and .png formats)
#     image_paths = {}
#     for filename in os.listdir(creature_images_path):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
#             # Use the filename as the key and the full path as the value
#             key = os.path.splitext(filename)[0]
#             full_path = os.path.join(creature_images_path, filename)
#             image_paths[key] = full_path
    
#     return image_paths

# # Bildpfade laden und cachen
# creature_image_paths = load_image_paths(creature_images_path)



# # Start and Stop buttons
# start_button = st.button("Start")
# stop_button = st.button("Stop")

# # # Update session state based on button clicks
# if start_button:
#     st.session_state.start = True
#     st.session_state.current_tab = 0
# if stop_button:
#     st.session_state.start = False


# # Random order of images
# image_names = list(creature_image_paths.keys())
# random.shuffle(image_names)



# # Set up dynamic tabs for each creature
# tab_names = list(creature_image_paths.keys())

# col1, col2, col3 = st.columns([1,2,1], gap="large")
# with col2:
#     tabs = st.tabs([name.upper() for name in tab_names])


# # Loop through each tab and each image, displaying images if "Start" is active
# if st.session_state.start:
#     for name in image_names:
#         # NEW: Select the current tab based on the current index
#         current_tab_name = tab_names[st.session_state.current_tab]
#         with tabs[st.session_state.current_tab]:  # Display in the active tab
#             placeholder = st.empty()  # Placeholder for the image
#             # Display image and name in the current tab
#             placeholder.image(creature_image_paths[name], use_column_width='auto')
#             st.markdown(f"{name.upper()}")
            
#             # Store the last displayed image for each tab in session state
#             st.session_state.last_images[current_tab_name] = creature_image_paths[name]

#             # Wait for a short period before switching to the next tab
#             time.sleep(0.2)

#             # NEW: Update to the next tab, looping back to the first tab if necessary
#             st.session_state.current_tab = (st.session_state.current_tab + 1) % len(tab_names)

#             # Break if stopped
#             if not st.session_state.start:
#                 break
# else:
#     # Show the last image displayed for each tab after stopping
#     for idx, tab_name in enumerate(tab_names):
#         with tabs[idx]:
#             placeholder = st.empty()
#             if tab_name in st.session_state.last_images:
#                 placeholder.image(st.session_state.last_images[tab_name], use_column_width='auto')
#                 st.markdown(f"{tab_name.upper()}")
                
# # Loop through each tab, displaying images if "Start" is active
# for idx, tab_name in enumerate(tab_names):
#     with tabs[idx]:
#         with col2:
#             placeholder = st.empty()  # Placeholder for the image
#             if st.session_state.start:
#                 for name in image_names:
#                     # Display image and name in the current tab
#                     placeholder.image(creature_image_paths[name], use_column_width='auto')
#                     st.markdown(f"{name.upper()}")
                    
#                     # Store the last displayed image for each tab in session state
#                     st.session_state.last_images[tab_name] = creature_image_paths[name]
                    
#                     time.sleep(0.2)  # Control the speed of spinning
#                     if not st.session_state.start:
#                         break
#             else:
#                 # Show the last image displayed when spinning stopped
#                 if tab_name in st.session_state.last_images:
#                     placeholder.image(st.session_state.last_images[tab_name], use_column_width='auto')
#                     st.markdown(f"{tab_name.upper()}")











# Call the function to cache the data
# data, monthly_stats_data = load_and_process_data() 




# # overview of the datas in a dataframe after Data Wrangeling 
# with st.expander("Raw Table monthly stats"): 
#     st.dataframe(monthly_stats_data)
# v_spacer(height=7, sb=False)



