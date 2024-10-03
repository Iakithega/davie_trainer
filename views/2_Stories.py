import streamlit as st
import os
import random
import time
from utils.utils import *
# from IPython.display import display, Markdown
from openai import OpenAI
# import openai
from utils.llm_utils import *

st.write("# Strorieeess")

# OTHER PARAMS AND OPENAI
cwd = os.getcwd()
# client = OpenAI(api_key=st.secrets.openai_credentials.api_key)
# openai.api_key = st.secrets.openai_credentials.api_key
client = OpenAI(api_key=st.secrets.openai_credentials.api_key)

# initialization of chat history
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"

# initialization of chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# displays chat messages from history on app
for message in st.session_state.messages:
     with st.chat_message(message["role"]):
        st.markdown(message["content"])



if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# # Reaction to user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#           st.markdown(prompt)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})



#     # Display assistant response im chat message container

#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         for response in client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]} 
#                 for m in st.session_state.messages],
#             stream=True):
         

#             delta = response.choices[0].delta
#             if 'content' in delta:
#                 full_response += delta['content']
#                 message_placeholder.markdown(full_response + " ")
#             # full_response += response.choices[0].delta.get("content", "")
#             # message_placeholder.markdown(full_response + " ")

        
#         message_placeholder.markdown(full_response)


#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": full_response})



# prompt = st.chat_message(name="user")
# if prompt:
#         st.write(f"user has sent following prompt: {prompt}")

# with st.chat_message(name="user", avatar=None):
#       st.write("Hello ")




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


papath = os.path.join("media", "wallpaper", "transformers1.png")

#Path to your local folder containing images
image_folder = r'media\wallpaper'

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



