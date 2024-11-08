import streamlit as st
import os
from utils.utils import set_streamlit_page_config_once

set_streamlit_page_config_once()

cwd = os.getcwd()
path_to_logo = os.path.join(cwd, "media", "veeery_lomng.png")
path_to_page_progress = os.path.join(cwd, "views", "1_Progress.py")
path_to_page_records = os.path.join(cwd, "views", "3_Records.py")
path_to_page_stories = os.path.join(cwd, "views", "2_Stories.py")
path_to_page_rewards_game = os.path.join(cwd, "views", "5_Rewards_game.py")
path_to_page_dialogue_with_the_master = os.path.join(cwd, "views", "3_dialogue_with_the_master.py")
path_to_page_css_stuff = os.path.join(cwd, "views", "zz_css_stuff.py")

path_to_wallpaper = os.path.join(cwd, "media","wallpaper", "backaragraunda.jpg")


st.logo(
    path_to_logo,
    link="https://streamlit.io/gallery", 
    size="large",
    icon_image=None
)


# Define the main navigation
pg0 = st.Page(r"streamlit_app.py", title="_____", default=False, icon=None, url_path=None) # icon=":material/home:" url_path=None, default=False # DAVID THE TITAN
pg1 = st.Page(path_to_page_progress, default=True, title="Progress", icon=":material/bar_chart_4_bars:")
pg2 = st.Page(path_to_page_records, default=False, title="Records", icon=":material/emoji_events:")
pg3 = st.Page(path_to_page_stories, default=False, title="Strories", icon=":material/sword_rose:")
pg4 = st.Page(path_to_page_rewards_game, default=False, title="Rewards Game", icon=":material/casino:")
pg5 = st.Page(path_to_page_dialogue_with_the_master, default=False, title="Master", icon=":material/self_improvement:")
pgz = st.Page(path_to_page_css_stuff, title="css_etc", default=False, icon=None, url_path=None) # icon=":material/sword_rose:"


pg = st.navigation({
    "Overview": [pg0, pg1, pg2],
    "Adventure": [pg3, pg4, pg5],
    "Else": [pgz]
})




try:
    pg.run()
except Exception as e:
    st.error(f"Something went wrong: {str(e)}")







