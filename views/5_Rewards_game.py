import streamlit as st
from utils.utils import *
import os.path
import random
import time



st.write("# The Game")
# v_spacer(height=5, sb=False)

cwd = os.getcwd()
creature_images_path = os.path.join(cwd, "media", "pics_of_creatures")
creature_question_mark_image_path = os.path.join(cwd, "media", "pics_of_creatures", "backup", "creature_question_mark.png")
path_audio = os.path.join(cwd, "media", "music", "action_epic.mp3")
path_to_style = os.path.join(cwd, "assets", "style.css")


# css funcs
hide_header_css() 
with open(path_to_style) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state for controlling the game and storing last images
if 'start' not in st.session_state:
    st.session_state.start = False
if 'selected_image' not in st.session_state:
    st.session_state.selected_image = creature_question_mark_image_path  
if 'selected_image_name' not in st.session_state:
    st.session_state.selected_image_name = "???"  
if 'selected_images' not in st.session_state:
    st.session_state.selected_images = []  # Track already selected images


@st.cache_data
def load_image_paths(creature_images_path):
    # Join the base directory with the creature images path to create an absolute path
    absolute_creature_images_path = os.path.join(creature_images_path)

    # Dictionary to store the image paths
    image_paths = {}
    for filename in os.listdir(absolute_creature_images_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_name = os.path.splitext(filename)[0]
            full_path = os.path.join(absolute_creature_images_path, filename)
            image_paths[image_name] = full_path
    return image_paths
 


# Load and cache image paths
creature_image_paths = load_image_paths(creature_images_path)
# Available images list (excluding selected ones)
available_images = {k: v for k, v in creature_image_paths.items() if k not in st.session_state.selected_images}

  
 

gap1_img_firstline, col_image, gap2_img_firstline = st.columns([1,2,1], gap="large", vertical_alignment="center")
with col_image:
    col_inside_img_start, col_inside_img_gap, col_inside_img_stop = st.columns([1, 2, 1], gap="large", vertical_alignment="center")
    # Start and Stop buttons
    with col_inside_img_start:
        start_button = st.button("Start", key="start_button")     
    with col_inside_img_stop:
        stop_button = st.button("Stop", key="stop_button")
    placeholder_image = st.empty()  # Placeholder for the image display
    placeholder_image_text = st.empty()
    placeholder_image_audio_expander = st.empty()

# with gap1_img_firstline:
#     # placeholder_available = st.empty()
# with gap2_img_firstline:
#     # placeholder_selected = st.empty()

    

# Update session state based on button clicks
if start_button:
    st.session_state.start = True
if stop_button:
    st.session_state.start = False

############################################################################################


# Spinning through random images
if st.session_state.start and available_images:
    with placeholder_image_audio_expander.expander("Audio"):
        st.audio(path_audio, format="audio/mpeg", loop=True, autoplay=True)
    while st.session_state.start:
        # Pick a random image name from available images
        name = random.choice(list(available_images.keys()))
        
        # Display image and name in the placeholder
        placeholder_image.image(available_images[name], use_container_width='auto')
        
        # Store the last displayed image in session state
        st.session_state.selected_image = available_images[name]
        st.session_state.selected_image_name = name
        
        time.sleep(0.1)  # Control the speed of spinning
        
        # Stop spinning if "Stop" button is pressed
        if not st.session_state.start:
            break

# Display the last selected image and update selected list
if not st.session_state.start:
    placeholder_image.image(st.session_state.selected_image, use_container_width='auto')
    placeholder_image_text.markdown(
        f"<h2 style='text-align: center;'>{st.session_state.selected_image_name.upper()}</h2>", 
        unsafe_allow_html=True
                                    )    
    
    # Add the selected image to the list of already chosen images if not already there
    if st.session_state.selected_image_name not in st.session_state.selected_images:
        st.session_state.selected_images.append(st.session_state.selected_image_name)
        # placeholder_available.write(available_images)
        # placeholder_selected.write(st.session_state.selected_images)

    # Update available images to exclude already selected ones
    available_images = {name: path for name, path in creature_image_paths.items() if name not in st.session_state.selected_images}



    # Notify user when all images are selected
    if not available_images:
        st.write("All images have been selected! Click 'Reset Game' to play again.")









# @st.cache_data
# def load_images(creature_images_path):
#     # Dictionary to store loaded images by name
#     image_data = {}
#     for filename in os.listdir(creature_images_path):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
#             key = os.path.splitext(filename)[0]
#             full_path = os.path.join(creature_images_path, filename)
#             # Load the image and store it in the dictionary
#             image_data[key] = Image.open(full_path)
#     return image_data



# # CHANGED: Load and cache images, not just paths
# creature_images = load_images(creature_images_path)
# # Available images list (excluding selected ones)
# available_images = {k: v for k, v in creature_images.items() if k not in st.session_state.selected_images}

    # # Update available images to exclude already selected ones
    # available_images = {k: v for k, v in creature_images.items() if k not in st.session_state.selected_images}