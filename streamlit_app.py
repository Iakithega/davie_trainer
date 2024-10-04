import streamlit as st
import os
import random

st.set_page_config(
    #  page_title="RHEALIZER!",
    #  page_icon="🤖", 
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': None
     }
 )

# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

st.logo(
    r"media\veeery_lomng.png",
    link="https://streamlit.io/gallery", # size="large"
    icon_image=None
)


# Define the main navigation
pg0 = st.Page(r"streamlit_app.py", title=" ", default=False, icon=None, url_path=None) # icon=":material/home:" url_path=None, default=False # DAVID THE TITAN
pg1 = st.Page(r"views\1_Progress.py", title="Progress", default=True, icon=":material/bar_chart_4_bars:")
pg2 = st.Page(r"views\3_Rewards.py", title="Rewards", icon=":material/emoji_events:")
pg3 = st.Page(r"views\2_Stories.py", title="Strories", icon=":material/sword_rose:")
pg4 = st.Page(r"views\3_dialogue_with_the_master.py", title="Master", icon=":material/self_improvement:")
pgz = st.Page(r"views\zz_css_stuff.py", title="css_etc", default=False, icon=None, url_path=None) # icon=":material/sword_rose:"


pg = st.navigation({
    "Overview": [pg0, pg1, pg2],
    "Adventure": [pg3, pg4],
    "Else": [pgz]
})




try:
    pg.run()
except Exception as e:
    st.error(f"Something went wrong: {str(e)}")







