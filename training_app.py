import streamlit as st

st.set_page_config(
     page_title="RHEALIZER!",
     page_icon="🤖", 
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.bulabula.com/help',
         'Report a bug': 'https://www.bulabula.com/help',
         'About': "# We are thinkering with ChatGPT here!"
     }
 )

#remove logo
hide_st_style = """
            <style>
             footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)  

st.title("David Train")