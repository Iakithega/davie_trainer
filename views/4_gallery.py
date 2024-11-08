
import os
import time


# OTHER PARAMS
cwd = os.getcwd()

lego_pic_folder = os.path.join('src', 'pics', 'lego')
lego_music_folder = os.path.join('src', 'music')

# function to find paths of the loaded files by given names
def find_lego_pics():
    all_pics = []
    gal_pics = []
        # Walking top-down from the root
    for file in os.listdir(lego_pic_folder):
        all_pics.append(os.path.join(lego_pic_folder, file))
        if 'gal' in file:
            gal_pics.append(os.path.join(lego_pic_folder, file))
    return all_pics, gal_pics

def find_lego_music():
    all_music = []
        # Walking top-down from the root
    for song in os.listdir(lego_music_folder):
        all_music.append(os.path.join(lego_music_folder, song))

    return all_music


all_pics, gal_pics = find_lego_pics()
all_music = find_lego_music()



# OTHER PARAMS
cwd = os.getcwd()

lego_pic_folder = os.path.join('src', 'pics', 'lego')
lego_music_folder = os.path.join('src', 'music')

# function to find paths of the loaded files by given names
def find_lego_pics():
    all_pics = []
    gal_pics = []
        # Walking top-down from the root
    for file in os.listdir(lego_pic_folder):
        all_pics.append(os.path.join(lego_pic_folder, file))
        if 'gal' in file:
            gal_pics.append(os.path.join(lego_pic_folder, file))
    return all_pics, gal_pics

def find_lego_music():
    all_music = []
        # Walking top-down from the root
    for song in os.listdir(lego_music_folder):
        all_music.append(os.path.join(lego_music_folder, song))

    return all_music


all_pics, gal_pics = find_lego_pics()
all_music = find_lego_music()



selection = st.radio(label="Selecta", options=all_music)
st.write(selection)

audio_file = open(selection, 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/ogg')


col1, col2, col3 = st.columns([1,2,1], gap="large")

with col2:
    st.markdown(' ## Photo?')
    v_spacer(5, False)
    placeholder = st.empty()
    for pic in gal_pics:
        placeholder.image(pic, use_column_width='auto')
        time.sleep(10)