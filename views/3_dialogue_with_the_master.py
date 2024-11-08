import streamlit as st
import os
import random
from utils.utils import *
from openai import OpenAI
from utils.llm_utils import *


# OTHER PARAMS AND OPENAI
cwd = os.getcwd()
client = OpenAI(api_key=st.secrets.openai_credentials.api_key)
path_to_wallpaper = os.path.join(cwd, "static", "backaragraunda.jpg")


# css funcs from utils
set_background_css(path_to_wallpaper)
hide_header_css()



st.write("# Story")

# initialization of chat history
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4o"

# initialization of chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# displays chat messages from history on app
for message in st.session_state.messages:
     with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(placeholder="What do you want to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message(name="assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
            )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})



# audio = elevenlabs.generate(
#     text = "Hello my dear frien!",
#     voice = "Bella"

# )

# elevenlabs.play(audio)

# result_raw = client.chat.completions.create(
#                 model=st.session_state["selected_model"],
#                 messages=[
#                     {"role": "system", 
#                      "content": f'''"
#                                 '''},
#                         ],
#                 temperature = 0.7
#                         )

# answer_raw = show_result_new(result_raw)



v_spacer(4, sb=False)


papath = os.path.join(cwd, "media", "exercise_pictures", "turmzug_spacy_2.png") 

#Path to your local folder containing images
image_folder = os.path.join(cwd, "media", "exercise_pictures")

# Get the list of image files from the folder
image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('png', 'jpg', 'jpeg'))]

# Select a random image from the folder
def get_random_image():
    return random.choice(image_paths)

image_path = random.choice(image_paths)

# col1, col2, col3 = st.columns([1,2,1], gap="large")

# with col2:
#     st.markdown(f'## {image_path}')
#     v_spacer(5, False)
#     placeholder = st.empty()
#     for img_path in image_paths:
#         placeholder.image(img_path, use_column_width='auto')
#         time.sleep(10)

# st.image(image_path, caption="Sunrise by the mountains")








