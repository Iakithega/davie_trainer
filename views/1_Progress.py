import streamlit as st
import os
from configparser import ConfigParser
from datetime import datetime

from utils.utils import *
from utils.data_engineering import complete_data_wrangeling
from utils.plotting_functions import *




# paths and configs
cwd = os.getcwd()
config = ConfigParser()
config.read("utils/paths.ini")
path_to_excel = os.path.join(cwd, config["paths"]["path_to_excel"])
path_to_wallpaper = os.path.join(cwd, "static", "backaragraunda.jpg")

# css funcs from utils
set_background_css(path_to_wallpaper)
hide_header_css()

if "boxplot_all_data" not in st.session_state:
    st.session_state["boxplot_all_data"] = False


st.title("David Titan")



# min date for restricting the calendar for chosing dates
min_date = datetime.strptime("2024.08.10", "%Y.%m.%d")
# Get the current date
current_date = datetime.today() + timedelta(days=3)
last_50_days = datetime.today() - timedelta(days=50)
current_date = current_date.strftime('%Y-%m-%d')



@st.cache_data
def load_and_process_data():
    initial_data = load_raw_excel(path_to_excel)
    data, monthly_stats_data = complete_data_wrangeling(initial_data)
    return data, monthly_stats_data

# Call the function to cache the data
data, monthly_stats_data = load_and_process_data() 


# overview of the datas in a dataframe after Data Wrangeling 
with st.expander("Raw Table all data"): 
    st.dataframe(data)

# overview of the datas in a dataframe after Data Wrangeling 
with st.expander("Raw Table monthly stats"): 
    st.dataframe(monthly_stats_data)
v_spacer(height=5, sb=False)


with st.expander("Adjust time periods"):
    # picking starting date for the plots
    date_col1, date_col2 = st.columns([1, 10])
    with date_col1:
        start_date = st.date_input(label="Start Date for Training Plots", value=last_50_days, min_value=min_date)
        v_spacer(height=2, sb=False)
    with date_col2:
        boxplot_filter_toggle = st.toggle(label="Boxplots for all data", value=False)
        if boxplot_filter_toggle:
            st.session_state["boxplot_all_data"] = True
        else:
            st.session_state["boxplot_all_data"] = False


fig_pushup = pushup_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_pushup)
v_spacer(height=2, sb=False)

fig_planke = plank_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_planke)
v_spacer(height=2, sb=False)

fig_kniebeuge = kniebeuge_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_kniebeuge)
v_spacer(height=2, sb=False)

fig_hammercurl = hamcurls_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_hammercurl)
v_spacer(height=2, sb=False)

fig_turmrud = turmrud_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_turmrud)
v_spacer(height=2, sb=False)

fig_turmzg = turmzg_plot(data=data, monthly_stats_data=monthly_stats_data, start_date=start_date, current_date=current_date)
st.pyplot(fig_turmzg)
v_spacer(height=2, sb=False)


