import streamlit as st
import os
import random
import datetime
import time
from utils.utils import *
# from IPython.display import display, Markdown
from openai import OpenAI
# import openai
from utils.llm_utils import *

from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream, save

import ffmpeg

from datetime import date

today = date.today()

# Month abbreviation, day and year	
today_clean = today.strftime("%b_%d_%Y")


st.write("# Story")

# OTHER PARAMS AND OPENAI
cwd = os.getcwd()
current_time = datetime.time()

client = OpenAI(api_key=st.secrets.openai_credentials.api_key)

client_elabs = ElevenLabs(api_key=st.secrets.elevenlabs_credentials.api_key)

# initialization of chat history
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4o"





##################STATES & ESSENTIAL LISTS AND PARAMS############################
# Initializing session states for Criteria matcher
if 'person_chosen' not in st.session_state:
    st.session_state['person_chosen'] = 'Select'

if 'input_submitted' not in st.session_state: 
    st.session_state['input_submitted'] = False

if 'extra_metapher_option' not in st.session_state:
    st.session_state['extra_metapher_option'] = " "

if 'selected_model' not in st.session_state: 
    st.session_state['selected_model'] = "gpt-3.5-turbo"  

if 'selected_language' not in st.session_state: 
    st.session_state['selected_language'] = "deutsch"  

if 'extra_personality_option' not in st.session_state: 
    st.session_state['extra_personality_option'] = " "  

if 'user_input' not in st.session_state: 
    st.session_state['user_input'] = " "  

list_of_personalities = ['Select', 'Bekannte Persönlichkeit aus Eldrador', 'Bekannte Persönlichkeit aus Ninjago', 'Joe Rogan', 
                         'Bekannte Persönlichkeit aus Harry Potter', 'Bekannte Persönlichkeit aus Pokemon', 'Фёдор Достоевский', 'Arthur Schopenhauer', 
                         'Friedrich Nietzsche', 'Рамзан Кадыров', 'Dan Pena']

###################################APP########################################
###################################APP########################################
###################################APP########################################

#Title of the Page
_, col_title, _ = st.columns(3)
with col_title:
    app_coloured_title = st.write("<h1><span style='color:#40E761'>Story Teller</span></h1>",
                                    unsafe_allow_html=True)
    v_spacer(height=4, sb=False) 


########################################SIDEBAR SETTINGS####################################

############################################CHOOSING PERSON################################################################
v_spacer(height=4, sb=True)

personality_selector = st.sidebar.selectbox(label='Select Personality', options=list_of_personalities, label_visibility='hidden')
if personality_selector == 'Select':
    st.sidebar.write("<h4><span style='color:#40E761'>Select Personality</span></h4>",
                        unsafe_allow_html=True)
else:
    st.sidebar.write(f"<h4><span style='color:#40E761'>{personality_selector}</span></h4>",
                        unsafe_allow_html=True)

if 'Bekannte Persönlichkeit aus Eldrador' in personality_selector:
    selected_personality = "Bekannte Persönlichkeit aus Eldrador"
    # picture = picture_trump

if 'Bekannte Persönlichkeit aus Ninjago' in personality_selector:
    selected_personality = "Bekannte Persönlichkeit aus Ninjago"

            
if 'Bekannte Persönlichkeit aus Harry Potter' in personality_selector:
    selected_personality = "Bekannte Persönlichkeit aus Harry Potter"

            
if 'Bekannte Persönlichkeit aus Pokemon' in personality_selector:
    selected_personality = "Bekannte Persönlichkeit aus Pokemon"


if 'Elon Musk' in personality_selector:
    selected_personality = "Elon Musk"


if 'Franz Kafka' in personality_selector:
    selected_personality = "Franz Kafka"


if 'Фёдор Достоевский' in personality_selector:
    selected_personality = "Фёдор Достоевский"


if 'Friedrich Nietzsche' in personality_selector:
    selected_personality = "Friedrich Nietzsche"


if 'Arthur Schopenhauer' in personality_selector:
    selected_personality = "Arthur Schopenhauer"


if 'Рамзан Кадыров' in personality_selector:
    selected_personality = "Рамзан Кадыров"


if 'Dan Pena' in personality_selector:
    selected_personality = "Dan Pena"



st.session_state['person_chosen'] = personality_selector

v_spacer(height=4, sb=True)
output_language = st.sidebar.radio('Chose language', ["deutsch", "русский", "english" ])
st.session_state['selected_language'] = output_language

v_spacer(height=4, sb=True)
input_temperature = st.sidebar.slider("Chose temperature", step=0.1, value=(0.7), key="temperature_input", min_value=0.1, max_value=1.5)
chosen_temperature = input_temperature


##########################################################################
################################STAGE 1############################
#########################################################################

if st.session_state['person_chosen'] != 'Select':

########################################MAIN PART SETTING ROW####################################
    col1_settings_row, col2_settings_row, col3_settings_row, col4_settings_row, col5_settings_row, col6_settings_row, _, _ = st.columns(8)

    with col2_settings_row:
        v_spacer(height=3, sb=False) 
        extra_personality_toggle = st.toggle(label="Maximize", 
                                             key="Key3", 
                                             )

    with col4_settings_row:
        v_spacer(height=3, sb=False) 
        model_toggle = st.toggle(label="GPT-4" , 
                                 key="Key1", 
                                )

    with col6_settings_row:
        v_spacer(height=3, sb=False) 
        extra_metapher_toggle = st.toggle(label="Metaphorize", 
                                          key="Key2", 
                                         )
    
  
    if extra_metapher_toggle:
        st.session_state['extra_metapher_option'] = "Sei sehr Sarkastisch in deiner Ausdrucksweise und integriere sehr häufig lustige oder sarkastische Metapher."
    else:
        st.session_state['extra_metapher_option'] = "Sei freundlich und uplifting is deiner Ausdrucksweise." 

    if model_toggle:
        st.session_state['selected_model'] = "gpt-4"
    else:
        st.session_state['selected_model'] = "gpt-3.5-turbo" 
            
    if extra_personality_toggle:
        st.session_state['extra_personality_option'] = f"Es muss sehr stark nach {selected_personality} klingen, sodass die Leute leicht erkennen dass es von {selected_personality} kommt."
    else:
        st.session_state['extra_personality_option'] = " " 


#########################################1. USER INPUT############################################################################
    v_spacer(height=2, sb=False) 
    form = st.form(key='my-form')
    st.session_state['user_input'] = form.text_input(label=f'''{st.session_state["selected_model"]} | 
                                                               {st.session_state["selected_language"]} | 
                                                               {st.session_state["extra_metapher_option"]} | 
                                                               {st.session_state['extra_personality_option']}''')
    submit_user_input = form.form_submit_button(f'GO {selected_personality.split()[0]}!')


#########################################2. SHOW PHOTO AND START THE ALGORITHM############################################################################
    if submit_user_input:
        st.session_state['input_submitted'] = True
        if personality_selector:
            st.session_state['person_chosen'] = True 
            if st.session_state['person_chosen'] == True and st.session_state['input_submitted'] == True:
                v_spacer(height=4, sb=False) 
                col1_image_row, col2_image_row, col3_image_row = st.columns(3)
                with col2_image_row:
                    st.image(r"media\wallpaper\transformers4.png", use_column_width=True) # width=400
    


#########################################2. PROMPT############################################################################


    if st.session_state['person_chosen'] != 'Select' and st.session_state['input_submitted'] == True:
            
        result_raw = client.chat.completions.create(
                model=st.session_state["selected_model"],
                messages=[
                    {"role": "system", 
                     "content": f'''Du bist {selected_personality}, und du erzählst Geschichten die lehrreich aber auch witzig sind. Die Geschichten sind für einen Jungen der David heißt und 9 Jahre alt ist.
                                    Der junge David mag es zu trainieren um stärker zu werden. Er übt auch fließig tricks und Übungen auf Reck und Barren und möchte stark wie ein Titan sein. 
                                    Bitte formuliere einen Text im Stil von {selected_personality} um und rede dabei {st.session_state['selected_language']}. 
                                    {st.session_state['extra_metapher_option']} 
                                    {st.session_state['extra_personality_option']}
                                    Hier sind weitere Ereignisse oder Sachen die du in die geschichte für 9 jährigen David mit einbauen solltest: "{st.session_state['user_input']}"
                                '''},
                        ],
                temperature = chosen_temperature
                        )

        answer_raw = show_result_new(result_raw)





        

        v_spacer(height=5, sb=False) 
        st.text_area("You said: ", {st.session_state['user_input']} , key="input") #height=220 #answer_raw

        v_spacer(height=3, sb=False) 
        st.text_area(f"{selected_personality} said:" , answer_raw , key="output") #height=


        v_spacer(height=3, sb=False) 
        print("0. gelich generiere ich was")
        audio = client_elabs.generate(
                            text=f"{answer_raw}",
                            voice="Rachel",
                            model="eleven_multilingual_v2"
                            )
        
        print("1. habe was generiert")
        
        path_audio = f"{selected_personality}_audio_{today}.mp3"
        print(f"2. werde es gleich speichern unter dem pfad: {path_audio}")
        save(audio, path_audio)
        print("3. habs gespeicher ")

   
        # print("3. gleich spiele ich es ab ")
        # play(audio)
        # print("4. elevenlabs hat abgespielt ")

        
        
        # saves audio to file
        
     
        
    
        print("4. gleich spuielt es streamlit ab ")
        st.audio(path_audio, format="audio/mpeg", loop=True)
        
        









# initialization of chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # displays chat messages from history on app
# for message in st.session_state.messages:
#      with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if prompt := st.chat_input(placeholder="What do you want to know?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message(name="assistant"):
#         stream = client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True
#             )
#         response = st.write_stream(stream)
#     st.session_state.messages.append({"role": "assistant", "content": response})



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



