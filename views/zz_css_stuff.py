import streamlit as st

st.write("# CSS & Stuffs")

# st.text_input("", placeholder="Streamlit CSS ")

# input_style = """
# <style>
# input[type="text"] {
#     background-color: transparent;
#     color: #a19eae;  // This changes the text color inside the input box
# }
# div[data-baseweb="base-input"] {
#     background-color: transparent !important;
# }
# [data-testid="stAppViewContainer"] {
#     background-color: transparent !important;
# }
# </style>
# """
# st.markdown(input_style, unsafe_allow_html=True)

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


# Path to your local folder containing images
# image_folder = r'media\wallpaper'

# # Get the list of image files from the folder
# image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('png', 'jpg', 'jpeg'))]

# # Select a random image from the folder
# def get_random_image():
#     return random.choice(image_paths)

# image_path = random.choice(image_paths)



# st.markdown(background_image, unsafe_allow_html=True)