import streamlit as st
import os
import random
import time
from utils.utils import *

st.write("#Strorieeess")

papath = os.path.join("media", "wallpaper", "transformers1.png")


#Path to your local folder containing images
image_folder = r'media\wallpaper'

# Get the list of image files from the folder
image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('png', 'jpg', 'jpeg'))]

# Select a random image from the folder
def get_random_image():
    return random.choice(image_paths)

image_path = random.choice(image_paths)

col1, col2, col3 = st.columns([1,2,1], gap="large")

with col2:
    st.markdown(' ## Photo?')
    v_spacer(5, False)
    placeholder = st.empty()
    for img_path in image_paths:
        placeholder.image(img_path, use_column_width='auto')
        time.sleep(10)

# st.image(image_path, caption="Sunrise by the mountains")

