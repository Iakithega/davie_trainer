import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import matplotlib.dates as mdates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from datetime import datetime

from utils.utils import *
from utils.data_engineering import *
from utils.plotting_functions import *

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


start_date = "2024.08.10"
# Get the current date
current_date = datetime.today() + timedelta(days=1)
# Format the date as 'YYYY-MM-DD'
current_date = current_date.strftime('%Y-%m-%d')

# load the data
initial_data = load_raw_excel(path_to_excel)

# extract weights and reps and band strength
data = weight_reps_exctracter(initial_data)


# calculate no weight averages, max and sum for liegestütze, planke and kniebeugen
data = calc_sets_overview_no_weights(data)

# calculate no weight averages, max and sum for weighted Hammer Curls, and Turm Zug
data = calc_sets_overview_with_weights(data)

# implements weight factored column
data = compute_hammer_curls_scores(data)
data = calc_hammer_curls_score_overview(data)

data = compute_trmrd_scores(data)
data = calc_trmrd_score_overview(data)

# calculate no weight averages, max and sum for distanced Turm Rudern
data = calc_sets_overview_with_weights_dstanced(data)


with st.expander("Raw Table"): 
    st.dataframe(data)

v_spacer(height=4, sb=False)



col1_params_normal_plot, col2_params_normal_plot = st.columns([3, 2], gap="large")
#show here the elements with columns for normal plot
with col1_params_normal_plot:
    all_exersices = [column_name for column_name in data.columns]
    selected_exersices = st.multiselect("Choose exersices", all_exersices)


v_spacer(height=4, sb=False)


fig_pushup = pushup_plot(data, start_date, current_date)
st.pyplot(fig_pushup)

fig_planke = plank_plot(data, start_date, current_date)
st.pyplot(fig_planke)

fig_kniebeuge = kniebeuge_plot(data, start_date, current_date)
st.pyplot(fig_kniebeuge)

fig_hammercurl = hamcurls_plot(data, start_date, current_date)
st.pyplot(fig_hammercurl)

fig_turmrud = turmrud_plot(data, start_date, current_date)
st.pyplot(fig_turmrud)

fig_turmzg = turmzg_plot(data, start_date, current_date)
st.pyplot(fig_turmzg)




# plt.style.use('seaborn-v0_8')
# fig, axs = plt.subplot_mosaic([
#                              ['1', '1', '1'],
#                              ],
#                              figsize=(11, 3))
# plt.subplots_adjust(wspace=.2)
# plt.subplots_adjust(hspace=.6)

# # fig.suptitle(f'''Training''', size=18)

# axs['1'].set_title(f"Progress Weighted Turm Rudern", size=14)
# axs['1'].set_xlabel(' ', size=14)
# axs['1'].set_ylabel('Value', size=12)
# axs['1'].set_xlim([pd.to_datetime("2024.08.10"), pd.to_datetime("2024.09.05")]), # TODAYS DATE 
# # axs['1'].set_ylim([0, 14])

# # Set font size for major and minor ticks
# axs['1'].tick_params(axis='x', labelsize=7, rotation=45)  
# axs['1'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

# axs['1'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
# axs['1'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
# axs['1'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

# axs['1'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
# axs['1'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
# axs['1'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

# # Plotting the three sets next to each other
# bar_width = 0.2
# dates = data.index

# axs['1'].bar(dates - pd.Timedelta(hours=4), data["Weighted Turm Rudern set 1 reps"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
# axs['1'].bar(dates, data["Weighted Turm Rudern set 2 reps"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
# axs['1'].bar(dates + pd.Timedelta(hours=4), data["Weighted Turm Rudern set 3 reps"], alpha=1, color="darkviolet", width=bar_width, label="Set 3") 

# st.pyplot(fig)