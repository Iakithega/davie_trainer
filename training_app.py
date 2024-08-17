import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import matplotlib.dates as mdates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU

from utils.utils import *
from utils.data_engineering import *

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




initial_data = load_raw_excel(path_to_excel)

data = weight_reps_exctracter(initial_data)






col1_params_normal_plot, col2_params_normal_plot = st.columns([3, 2], gap="large")
#show here the elements with columns for normal plot
with col1_params_normal_plot:
    all_exersices = [column_name for column_name in data.columns]
    selected_exersices = st.multiselect("Choose exersices", all_exersices)



plt.style.use('seaborn-v0_8')
fig, axs = plt.subplot_mosaic([
                             ['1', '1', '1'],
                             ],
                             figsize=(11, 3))

plt.subplots_adjust(wspace=.2)
plt.subplots_adjust(hspace=.6)

# fig.suptitle(f'''Training''', size=18)

axs['1'].set_title(f"Progress Liegestütz", size=14)
axs['1'].set_xlabel(' ', size=14)
axs['1'].set_ylabel('Value', size=12)
axs['1'].set_xlim([pd.to_datetime("2024.08.10"), pd.to_datetime("2024.08.20")]), 
# axs['1'].set_ylim([0, 14])

# Set font size for major and minor ticks
axs['1'].tick_params(axis='x', labelsize=7, rotation=45)  
axs['1'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

axs['1'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
axs['1'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
axs['1'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

axs['1'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
axs['1'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
axs['1'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

# Plotting the three sets next to each other
bar_width = 0.2
dates = data.index

axs['1'].bar(dates - pd.Timedelta(hours=4), data["Liegestütz set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
axs['1'].bar(dates, data["Liegestütz set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
axs['1'].bar(dates + pd.Timedelta(hours=4), data["Liegestütz set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")

st.pyplot(fig)




plt.style.use('seaborn-v0_8')
fig, axs = plt.subplot_mosaic([
                             ['1', '1', '1'],
                             ],
                             figsize=(11, 3))
plt.subplots_adjust(wspace=.2)
plt.subplots_adjust(hspace=.6)

# fig.suptitle(f'''Training''', size=18)

axs['1'].set_title(f"Progress Planke", size=14)
axs['1'].set_xlabel(' ', size=14)
axs['1'].set_ylabel('Value', size=12)
axs['1'].set_xlim([pd.to_datetime("2024.08.10"), pd.to_datetime("2024.08.20")]), 
# axs['1'].set_ylim([0, 14])

# Set font size for major and minor ticks
axs['1'].tick_params(axis='x', labelsize=7, rotation=45)  
axs['1'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

axs['1'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
axs['1'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
axs['1'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

axs['1'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
axs['1'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
axs['1'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

# Plotting the three sets next to each other
bar_width = 0.2
dates = data.index

axs['1'].bar(dates - pd.Timedelta(hours=4), data["Planke set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
axs['1'].bar(dates, data["Planke set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
axs['1'].bar(dates + pd.Timedelta(hours=4), data["Planke set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")

st.pyplot(fig)





plt.style.use('seaborn-v0_8')
fig, axs = plt.subplot_mosaic([
                             ['1', '1', '1'],
                             ],
                             figsize=(11, 3))
plt.subplots_adjust(wspace=.2)
plt.subplots_adjust(hspace=.6)

# fig.suptitle(f'''Training''', size=18)

axs['1'].set_title(f"Progress Kniebeugen", size=14)
axs['1'].set_xlabel(' ', size=14)
axs['1'].set_ylabel('Value', size=12)
axs['1'].set_xlim([pd.to_datetime("2024.08.10"), pd.to_datetime("2024.08.20")]), 
# axs['1'].set_ylim([0, 14])

# Set font size for major and minor ticks
axs['1'].tick_params(axis='x', labelsize=7, rotation=45)  
axs['1'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

axs['1'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
axs['1'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
axs['1'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

axs['1'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
axs['1'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
axs['1'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

# Plotting the three sets next to each other
bar_width = 0.2
dates = data.index

axs['1'].bar(dates - pd.Timedelta(hours=4), data["Kniebeugen set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
axs['1'].bar(dates, data["Kniebeugen set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
axs['1'].bar(dates + pd.Timedelta(hours=4), data["Kniebeugen set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")

st.pyplot(fig)





plt.style.use('seaborn-v0_8')
fig, axs = plt.subplot_mosaic([
                             ['1', '1', '1'],
                             ],
                             figsize=(11, 3))
plt.subplots_adjust(wspace=.2)
plt.subplots_adjust(hspace=.6)

# fig.suptitle(f'''Training''', size=18)

axs['1'].set_title(f"Progress Hammer Curls", size=14)
axs['1'].set_xlabel(' ', size=14)
axs['1'].set_ylabel('Value', size=12)
axs['1'].set_xlim([pd.to_datetime("2024.08.10"), pd.to_datetime("2024.08.20")]), 
# axs['1'].set_ylim([0, 14])

# Set font size for major and minor ticks
axs['1'].tick_params(axis='x', labelsize=7, rotation=45)  
axs['1'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

axs['1'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
axs['1'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
axs['1'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

axs['1'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
axs['1'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
axs['1'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

# Plotting the three sets next to each other
bar_width = 0.2
dates = data.index

axs['1'].bar(dates - pd.Timedelta(hours=4), data["Weighted Hammer Curls set 1 reps"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
axs['1'].bar(dates, data["Weighted Hammer Curls set 2 reps"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
axs['1'].bar(dates + pd.Timedelta(hours=4), data["Weighted Hammer Curls set 3 reps"], alpha=1, color="darkviolet", width=bar_width, label="Set 3") 

st.pyplot(fig)






plt.style.use('seaborn-v0_8')
fig, axs = plt.subplot_mosaic([
                             ['1', '1', '1'],
                             ],
                             figsize=(11, 3))
plt.subplots_adjust(wspace=.2)
plt.subplots_adjust(hspace=.6)

# fig.suptitle(f'''Training''', size=18)

axs['1'].set_title(f"Progress Weighted Turm Rudern", size=14)
axs['1'].set_xlabel(' ', size=14)
axs['1'].set_ylabel('Value', size=12)
axs['1'].set_xlim([pd.to_datetime("2024.08.10"), pd.to_datetime("2024.08.20")]), 
# axs['1'].set_ylim([0, 14])

# Set font size for major and minor ticks
axs['1'].tick_params(axis='x', labelsize=7, rotation=45)  
axs['1'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

axs['1'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
axs['1'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
axs['1'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

axs['1'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
axs['1'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
axs['1'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

# Plotting the three sets next to each other
bar_width = 0.2
dates = data.index

axs['1'].bar(dates - pd.Timedelta(hours=4), data["Weighted Turm Rudern set 1 reps"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
axs['1'].bar(dates, data["Weighted Turm Rudern set 2 reps"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
axs['1'].bar(dates + pd.Timedelta(hours=4), data["Weighted Turm Rudern set 3 reps"], alpha=1, color="darkviolet", width=bar_width, label="Set 3") 

st.pyplot(fig)