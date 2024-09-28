import streamlit as st


st.set_page_config(
    #  page_title="RHEALIZER!",
    #  page_icon="🤖", 
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.bulabula.com/help',
         'Report a bug': 'https://www.bulabula.com/help',
         'About': "# We are thinkering with ChatGPT here!"
     }
 )

# def wide_space_default():
#     st.set_page_config(layout="wide")

# wide_space_default()

st.logo(
    r"media\veeery_lomng.png",
    link="https://streamlit.io/gallery",
    icon_image=None,
)

# #remove logo
# hide_st_style = """
#             <style>
#              footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True) 

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


# Define the main navigation
pg0 = st.Page(r"streamlit_app.py", title="Start", default=False, icon=":material/home:")
pg1 = st.Page(r"1_Progress.py", title="Progress", default=True, icon=":material/bar_chart_4_bars:")
pg2 = st.Page(r"views\3_Rewards.py", title="Rewards", icon=":material/emoji_events:")
pg3 = st.Page(r"views\2_Stories.py", title="Strories", icon=":material/sword_rose:")



pg = st.navigation({
    "Overview": [pg0, pg1, pg2],
    "Adventure": [pg3],
})




try:
    pg.run()
except Exception as e:
    st.error(f"Something went wrong: {str(e)}")







