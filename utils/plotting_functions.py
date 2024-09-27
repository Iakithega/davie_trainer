import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd 

import numpy as np

import matplotlib.dates as mdates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU

from datetime import datetime
from datetime import timedelta
import time

import calendar
import yaml
import json

from streamlit_extras.mandatory_date_range import date_range_picker 
# from toggle_button_set import toggle_button_set

from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import matplotlib.path as mpath

from utils.utils import *
from utils.data_engineering import *



def pushup_plot(data, start_date, current_date):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['LGSTZ_REC', 'LGSTZ_REC', 'LGSTZ_REC'],
                                ['LGSTZ', 'LGSTZ', 'LGSTZ'],
                                ['LGSTZ', 'LGSTZ', 'LGSTZ']
                                ],
                                figsize=(10, 5))

    plt.subplots_adjust(wspace=.2, hspace=.8)
    # plt.subplots_adjust()

    # fig.suptitle(f'''Training''', size=18)

    axs['LGSTZ'].set_title(f"Progress Liegestütz", size=10)
    axs['LGSTZ'].set_xlabel(' ', size=14)
    axs['LGSTZ'].set_ylabel('Reps', size=8)
    axs['LGSTZ'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['LGSTZ'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['LGSTZ'].tick_params(axis='x', which='minor', labelsize=5, rotation=45) 
    axs['LGSTZ'].tick_params(axis='y', which='major', labelsize=6)

    axs['LGSTZ'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['LGSTZ'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['LGSTZ'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['LGSTZ'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['LGSTZ'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['LGSTZ'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    axs['LGSTZ'].bar(dates - pd.Timedelta(hours=10), data["Liegestütz set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['LGSTZ'].bar(dates, data["Liegestütz set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['LGSTZ'].bar(dates + pd.Timedelta(hours=10), data["Liegestütz set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")

    for set_name, offset in zip(["Liegestütz set 1", "Liegestütz set 2", "Liegestütz set 3"], [-pd.Timedelta(hours=12), pd.Timedelta(0), pd.Timedelta(hours=12)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['LGSTZ'].text(date + offset, value + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')


    # axs['LGSTZ_REC'].set_title(f"Progress Liegestütz", size=10)
    axs['LGSTZ_REC'].set_xlabel(' ', size=14)
    axs['LGSTZ_REC'].set_ylabel('Reps', size=8)
    axs['LGSTZ_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['LGSTZ_REC'].set_ylim([0, 100])

    # Set font size for major and minor ticks
    axs['LGSTZ_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['LGSTZ_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['LGSTZ_REC'].tick_params(axis='y', which='major', labelsize=6) 

    axs['LGSTZ_REC'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['LGSTZ_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['LGSTZ_REC'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['LGSTZ_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['LGSTZ_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['LGSTZ_REC'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    axs['LGSTZ_REC'].bar(dates - pd.Timedelta(hours=10), data["Liegestütz Average all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['LGSTZ_REC'].bar(dates, data["Liegestütz Max all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['LGSTZ_REC'].bar(dates + pd.Timedelta(hours=10), data["Liegestütz Sum all sets"], alpha=1, color="gray", width=bar_width, label="Amount")

    # Adding legend
    axs['LGSTZ_REC'].legend(loc='best', fontsize=5)


    # Initialize dictionaries to keep track of the maximum values for each set name
    max_values = {
        "Liegestütz Average all sets": -float('inf'),
        "Liegestütz Max all sets": -float('inf'),
        "Liegestütz Sum all sets": -float('inf')
    }

    # Iterate over the three metrics and add the annotation
    for set_name, offset in zip(
        ["Liegestütz Average all sets", "Liegestütz Max all sets", "Liegestütz Sum all sets"], 
        [-pd.Timedelta(hours=10), pd.Timedelta(0), pd.Timedelta(hours=10)]
    ):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value) and value != 0:
                # Check if the current value is a new record (higher than the previous maximum)
                if value > max_values[set_name]:
                    # Update the maximum value for this set_name
                    max_values[set_name] = value
                    
                    # Highlight the record by adding a background color (e.g., yellow)
                    axs['LGSTZ_REC'].text(date + offset, value + 3, f"{round(value)}", 
                                        va='center', ha='center', fontsize=4, color='black', 
                                        bbox=dict(facecolor='green', alpha=0.3, edgecolor='none', pad=0.15))
                else:
                    # Regular annotation for non-record values (without background)
                    axs['LGSTZ_REC'].text(date + offset, value + 3, f"{round(value)}", 
                                        va='center', ha='center', fontsize=4, color='black')



    return fig


def plank_plot(data, start_date, current_date):

    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['PLK_REC', 'PLK_REC', 'PLK_REC'],
                                ['PLK', 'PLK', 'PLK'],
                                ['PLK', 'PLK', 'PLK'],
                                ],
                                figsize=(10, 5))
    plt.subplots_adjust(wspace=.2, hspace=.8)

    # fig.suptitle(f'''Training''', size=18)

    axs['PLK'].set_title(f"Progress Planke", size=12)
    axs['PLK'].set_xlabel(' ', size=14)
    axs['PLK'].set_ylabel('Sec', size=8)
    axs['PLK'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['PLK'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['PLK'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['PLK'].tick_params(axis='y', which='major', labelsize=6)
     

    axs['PLK'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['PLK'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['PLK'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['PLK'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['PLK'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['PLK'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    axs['PLK'].bar(dates - pd.Timedelta(hours=12), data["Planke set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['PLK'].bar(dates, data["Planke set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['PLK'].bar(dates + pd.Timedelta(hours=12), data["Planke set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")


    for set_name, offset in zip(["Planke set 1", "Planke set 2", "Planke set 3"], [-pd.Timedelta(hours=16), pd.Timedelta(0), pd.Timedelta(hours=16)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['PLK'].text(date + offset, value + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')
    
    
    # axs['LGSTZ_REC'].set_title(f"Progress Liegestütz", size=10)
    axs['PLK_REC'].set_xlabel(' ', size=14)
    axs['PLK_REC'].set_ylabel('Sec', size=8)
    axs['PLK_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['PLK_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['PLK_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['PLK_REC'].tick_params(axis='y', which='major', labelsize=6) 

    axs['PLK_REC'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['PLK_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['PLK_REC'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['PLK_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['PLK_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['PLK_REC'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    axs['PLK_REC'].bar(dates - pd.Timedelta(hours=10), data["Planke Average all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['PLK_REC'].bar(dates, data["Planke Max all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['PLK_REC'].bar(dates + pd.Timedelta(hours=10), data["Planke Sum all sets"], alpha=1, color="gray", width=bar_width, label="Amount")

    # Adding legend
    axs['PLK_REC'].legend(loc='best', fontsize=5)


    
    # Initialize dictionaries to keep track of the maximum values for each set name
    max_values = {
        "Planke Average all sets": -float('inf'),
        "Planke Max all sets": -float('inf'),
        "Planke Sum all sets": -float('inf')
    }

    # Iterate over the three metrics and add the annotation
    for set_name, offset in zip(
        ["Planke Average all sets", "Planke Max all sets", "Planke Sum all sets"], 
        [-pd.Timedelta(hours=12), pd.Timedelta(0), pd.Timedelta(hours=12)]
    ):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value) and value != 0:
                # Check if the current value is a new record (higher than the previous maximum)
                if value > max_values[set_name]:
                    # Update the maximum value for this set_name
                    max_values[set_name] = value
                    
                    # Highlight the record by adding a background color (e.g., yellow)
                    axs['PLK_REC'].text(date + offset, value + 5, f"{round(value)}", 
                                        va='center', ha='center', fontsize=4, color='black', 
                                        bbox=dict(facecolor='green', alpha=0.3, edgecolor='none', pad=0.15))
                else:
                    # Regular annotation for non-record values (without background)
                    axs['PLK_REC'].text(date + offset, value + 5, f"{round(value)}", 
                                        va='center', ha='center', fontsize=4, color='black')

    return fig



def kniebeuge_plot(data, start_date, current_date):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['KNBG_REC', 'KNBG_REC', 'KNBG_REC'],
                                ['KNBG', 'KNBG', 'KNBG'],
                                ['KNBG', 'KNBG', 'KNBG'],
                                ],
                                figsize=(10, 5))
    
    plt.subplots_adjust(wspace=.2, hspace=.8)

    # fig.suptitle(f'''Training''', size=18)

    axs['KNBG'].set_title(f"Progress Kniebeugen", size=12)
    axs['KNBG'].set_xlabel(' ', size=14)
    axs['KNBG'].set_ylabel('Reps', size=8)
    axs['KNBG'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['KNBG'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['KNBG'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['KNBG'].tick_params(axis='y', which='major', labelsize=6) 

    axs['KNBG'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['KNBG'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['KNBG'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['KNBG'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['KNBG'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['KNBG'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    axs['KNBG'].bar(dates - pd.Timedelta(hours=10), data["Kniebeugen set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['KNBG'].bar(dates, data["Kniebeugen set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['KNBG'].bar(dates + pd.Timedelta(hours=10), data["Kniebeugen set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")


    for set_name, offset in zip(["Kniebeugen set 1", "Kniebeugen set 2", "Kniebeugen set 3"], [-pd.Timedelta(hours=12), pd.Timedelta(0), pd.Timedelta(hours=12)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['KNBG'].text(date + offset, value + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')
    


    # axs['LGSTZ_REC'].set_title(f"Progress Liegestütz", size=10)
    axs['KNBG_REC'].set_xlabel(' ', size=14)
    axs['KNBG_REC'].set_ylabel('Reps', size=8)
    axs['KNBG_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['KNBG_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['KNBG_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['KNBG_REC'].tick_params(axis='y', which='major', labelsize=6) 

    axs['KNBG_REC'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['KNBG_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['KNBG_REC'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['KNBG_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['KNBG_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['KNBG_REC'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    axs['KNBG_REC'].bar(dates - pd.Timedelta(hours=10), data["Kniebeugen Average all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['KNBG_REC'].bar(dates, data["Kniebeugen Max all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['KNBG_REC'].bar(dates + pd.Timedelta(hours=10), data["Kniebeugen Sum all sets"], alpha=1, color="gray", width=bar_width, label="Amount")

    # Adding legend
    axs['KNBG_REC'].legend(loc='best', fontsize=5)

    
    # Initialize dictionaries to keep track of the maximum values for each set name
    max_values = {
        "Kniebeugen Average all sets": -float('inf'),
        "Kniebeugen Max all sets": -float('inf'),
        "Kniebeugen Sum all sets": -float('inf')
    }

    # Iterate over the three metrics and add the annotation
    for set_name, offset in zip(
        ["Kniebeugen Average all sets", "Kniebeugen Max all sets", "Kniebeugen Sum all sets"], 
        [-pd.Timedelta(hours=10), pd.Timedelta(0), pd.Timedelta(hours=10)]
    ):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value) and value != 0:
                # Check if the current value is a new record (higher than the previous maximum)
                if value > max_values[set_name]:
                    # Update the maximum value for this set_name
                    max_values[set_name] = value
                    
                    # Highlight the record by adding a background color (e.g., yellow)
                    axs['KNBG_REC'].text(date + offset, value + 0.5, f"{round(value)}", 
                                        va='center', ha='center', fontsize=4, color='black', 
                                        bbox=dict(facecolor='green', alpha=0.3, edgecolor='none', pad=0.15))
                else:
                    # Regular annotation for non-record values (without background)
                    axs['KNBG_REC'].text(date + offset, value + 0.5, f"{round(value)}", 
                                        va='center', ha='center', fontsize=4, color='black')


    return fig


def hamcurls_plot(data, start_date, current_date):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['HMCRL_REC', 'HMCRL_REC', 'HMCRL_REC'],
                                ['HMCRL', 'HMCRL', 'HMCRL'],
                                ['HMCRL', 'HMCRL', 'HMCRL'],
                                ],
                                figsize=(10, 5))
    
    plt.subplots_adjust(wspace=.2, hspace=.8)

    # fig.suptitle(f'''Training''', size=18)

    axs['HMCRL'].set_title(f"Progress Hammer Curls", size=12)
    axs['HMCRL'].set_xlabel(' ', size=14)
    axs['HMCRL'].set_ylabel('Reps', size=8)
    axs['HMCRL'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['HMCRL'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['HMCRL'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['HMCRL'].tick_params(axis='y', which='major', labelsize=6) 

    axs['HMCRL'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['HMCRL'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['HMCRL'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['HMCRL'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['HMCRL'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['HMCRL'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    axs['HMCRL'].bar(dates - pd.Timedelta(hours=10), data["Weighted Hammer Curls set 1 reps"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['HMCRL'].bar(dates, data["Weighted Hammer Curls set 2 reps"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['HMCRL'].bar(dates + pd.Timedelta(hours=10), data["Weighted Hammer Curls set 3 reps"], alpha=1, color="darkviolet", width=bar_width, label="Set 3") 

    for set_name, offset in zip(["Weighted Hammer Curls set 1 reps", "Weighted Hammer Curls set 2 reps", "Weighted Hammer Curls set 3 reps"], [-pd.Timedelta(hours=12), pd.Timedelta(0), pd.Timedelta(hours=12)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['HMCRL'].text(date + offset, value + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')
    
    for set_name, offset in zip(["Weighted Hammer Curls set 1 weight", "Weighted Hammer Curls set 2 weight", "Weighted Hammer Curls set 3 weight"], [-pd.Timedelta(hours=12), pd.Timedelta(0), pd.Timedelta(hours=12)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['HMCRL'].text(date + offset, value/2 + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')
    

    # axs['LGSTZ_REC'].set_title(f"Progress Liegestütz", size=10)
    axs['HMCRL_REC'].set_xlabel(' ', size=14)
    axs['HMCRL_REC'].set_ylabel('Reps', size=8)
    axs['HMCRL_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['HMCRL_REC'].set_ylim([0, 100])

    # Set font size for major and minor ticks
    axs['HMCRL_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['HMCRL_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['HMCRL_REC'].tick_params(axis='y', which='major', labelsize=6) 

    axs['HMCRL_REC'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['HMCRL_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['HMCRL_REC'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['HMCRL_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['HMCRL_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['HMCRL_REC'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    axs['HMCRL_REC'].bar(dates - pd.Timedelta(hours=10), data["Hammer Curls Average reps all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['HMCRL_REC'].bar(dates, data["Hammer Curls Max reps all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['HMCRL_REC'].bar(dates + pd.Timedelta(hours=10), data["Hammer Curls Sum reps all sets"], alpha=1, color="gray", width=bar_width, label="Amount")

    # Adding legend
    axs['HMCRL_REC'].legend(loc='best', fontsize=5)

    

    # Initialize dictionaries to keep track of the maximum values for each metric
    max_values = {
        "Hammer Curls Average reps all sets": -float('inf'),
        "Hammer Curls Max reps all sets": -float('inf'),
        "Hammer Curls Sum reps all sets": -float('inf'),
        "Hammer Curls Average score all sets": -float('inf'),
        "Hammer Curls Max score all sets": -float('inf'),
        "Hammer Curls Sum score all sets": -float('inf')
    }

    # Iterate over the metrics and add the annotations
    for reps_metric, score_metric, offset in zip(
        ["Hammer Curls Average reps all sets", "Hammer Curls Max reps all sets", "Hammer Curls Sum reps all sets"],
        ["Hammer Curls Average score all sets", "Hammer Curls Max score all sets", "Hammer Curls Sum score all sets"],
        [-pd.Timedelta(hours=10), pd.Timedelta(0), pd.Timedelta(hours=10)]
    ):
        for date, reps_value in data[reps_metric].loc[start_date:current_date].items():
            if not pd.isna(reps_value) and reps_value != 0:
                # Get the corresponding score value
                score_value = data.loc[date, score_metric]

                # Check for new record in reps
                if reps_value > max_values[reps_metric]:
                    max_values[reps_metric] = reps_value
                    # Highlight the record for reps
                    axs['HMCRL_REC'].text(date + offset, reps_value + 0.5, f"{round(reps_value)}",
                                        va='center', ha='center', fontsize=4, color='black',
                                        bbox=dict(facecolor='green', alpha=0.3, edgecolor='none', pad=0.15))
                else:
                    # Regular annotation for reps
                    axs['HMCRL_REC'].text(date + offset, reps_value + 0.5, f"{round(reps_value)}",
                                        va='center', ha='center', fontsize=4, color='black')

                # Now, annotate the score above the reps annotation
                # Adjust the y-position by adding an additional offset
                score_y = reps_value + 10  # Adjust this value as needed to position the score annotation above
                if not pd.isna(score_value) and score_value != 0:
                    # Check for new record in score
                    if score_value > max_values[score_metric]:
                        max_values[score_metric] = score_value
                        # Highlight the record for score
                        axs['HMCRL_REC'].text(date + offset, score_y, f"{round(score_value)}",
                                            va='center', ha='center', fontsize=4, color='black',
                                            bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none', pad=0.15))
                    else:
                        # Regular annotation for score
                        axs['HMCRL_REC'].text(date + offset, score_y, f"{round(score_value)}",
                                            va='center', ha='center', fontsize=4, color='black')



    return fig




def turmrud_plot(data, start_date, current_date):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['TRMRD_REC', 'TRMRD_REC', 'TRMRD_REC'],
                                ['TRMRD', 'TRMRD', 'TRMRD'],
                                ['TRMRD', 'TRMRD', 'TRMRD'],
                                ],
                                figsize=(10, 5))
    
    plt.subplots_adjust(wspace=.2, hspace=.8)

    # fig.suptitle(f'''Training''', size=18)

    axs['TRMRD'].set_title(f"Progress Turmrudern", size=12)
    axs['TRMRD'].set_xlabel(' ', size=14)
    axs['TRMRD'].set_ylabel('Reps', size=8)
    axs['TRMRD'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['TRMRD'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['TRMRD'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['TRMRD'].tick_params(axis='y', which='major', labelsize=6) 

    axs['TRMRD'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['TRMRD'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['TRMRD'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['TRMRD'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['TRMRD'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['TRMRD'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    axs['TRMRD'].bar(dates - pd.Timedelta(hours=10), data["Weighted Turm Rudern set 1 reps"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['TRMRD'].bar(dates, data["Weighted Turm Rudern set 2 reps"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['TRMRD'].bar(dates + pd.Timedelta(hours=10), data["Weighted Turm Rudern set 3 reps"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")

    for set_name, offset in zip(["Weighted Turm Rudern set 1 reps", "Weighted Turm Rudern set 2 reps", "Weighted Turm Rudern set 3 reps"], [-pd.Timedelta(hours=12), pd.Timedelta(0), pd.Timedelta(hours=12)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['TRMRD'].text(date + offset, value + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')
    
    for set_name, offset in zip(["Weighted Turm Rudern set 1 band", "Weighted Turm Rudern set 2 band", "Weighted Turm Rudern set 3 band"], [-pd.Timedelta(hours=14), pd.Timedelta(0), pd.Timedelta(hours=14)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['TRMRD'].text(date + offset, value/10 + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black') 
    
    for set_name, offset in zip(["Weighted Turm Rudern set 1 distance", "Weighted Turm Rudern set 2 distance", "Weighted Turm Rudern set 3 distance"], [-pd.Timedelta(hours=16), pd.Timedelta(0), pd.Timedelta(hours=16)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['TRMRD'].text(date + offset, value/6 + 0.5, f"{value}", va='center', ha='center', fontsize=5, color='black')



    # axs['LGSTZ_REC'].set_title(f"Progress Liegestütz", size=10)
    axs['TRMRD_REC'].set_xlabel(' ', size=14)
    axs['TRMRD_REC'].set_ylabel('Reps', size=8)
    axs['TRMRD_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['TRMRD_REC'].set_ylim([0, 80])

    # Set font size for major and minor ticks
    axs['TRMRD_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['TRMRD_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['TRMRD_REC'].tick_params(axis='y', which='major', labelsize=6) 

    axs['TRMRD_REC'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['TRMRD_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['TRMRD_REC'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['TRMRD_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['TRMRD_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['TRMRD_REC'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    axs['TRMRD_REC'].bar(dates - pd.Timedelta(hours=10), data["Weighted Turm Rudern Average reps all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['TRMRD_REC'].bar(dates, data["Weighted Turm Rudern Max reps all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['TRMRD_REC'].bar(dates + pd.Timedelta(hours=10), data["Weighted Turm Rudern Sum reps all sets"], alpha=1, color="gray", width=bar_width, label="Amount")

    # Adding legend
    axs['TRMRD_REC'].legend(loc='best', fontsize=5)


    # for set_name, offset in zip(["Weighted Turm Rudern Average reps all sets", "Weighted Turm Rudern Max reps all sets", "Weighted Turm Rudern Sum reps all sets"], 
    #                         [-pd.Timedelta(hours=10), pd.Timedelta(0), pd.Timedelta(hours=10)]):
    #     for date, value in data[set_name].loc[start_date:current_date].items():
    #         if not pd.isna(value) and value != 0:
    #             axs['TRMRD_REC'].text(date + offset, value + 2, f"{round(value)}", va='center', ha='center', fontsize=4, color='black')
    

    # Initialize dictionaries to keep track of the maximum values for each metric
    max_values = {
        "Weighted Turm Rudern Average reps all sets": -float('inf'),
        "Weighted Turm Rudern Max reps all sets": -float('inf'),
        "Weighted Turm Rudern Sum reps all sets": -float('inf'),
        "Weighted Turm Rudern Average score all sets": -float('inf'),
        "Weighted Turm Rudern Max score all sets": -float('inf'),
        "Weighted Turm Rudern Sum score all sets": -float('inf')
    }

    # Iterate over the metrics and add the annotations
    for reps_metric, score_metric, offset in zip(
        ["Weighted Turm Rudern Average reps all sets", "Weighted Turm Rudern Max reps all sets", "Weighted Turm Rudern Sum reps all sets"],
        ["Weighted Turm Rudern Average score all sets", "Weighted Turm Rudern Max score all sets", "Weighted Turm Rudern Sum score all sets"],
        [-pd.Timedelta(hours=10), pd.Timedelta(0), pd.Timedelta(hours=10)]
    ):
        for date, reps_value in data[reps_metric].loc[start_date:current_date].items():
            if not pd.isna(reps_value) and reps_value != 0:
                # Get the corresponding score value
                score_value = data.loc[date, score_metric]

                # Check for new record in reps
                if reps_value > max_values[reps_metric]:
                    max_values[reps_metric] = reps_value
                    # Highlight the record for reps
                    axs['TRMRD_REC'].text(date + offset, reps_value + 0.5, f"{round(reps_value)}",
                                        va='center', ha='center', fontsize=4, color='black',
                                        bbox=dict(facecolor='green', alpha=0.3, edgecolor='none', pad=0.15))
                else:
                    # Regular annotation for reps
                    axs['TRMRD_REC'].text(date + offset, reps_value + 0.5, f"{round(reps_value)}",
                                        va='center', ha='center', fontsize=4, color='black')

                # Now, annotate the score above the reps annotation
                # Adjust the y-position by adding an additional offset
                score_y = reps_value + 10  # Adjust this value as needed to position the score annotation above
                if not pd.isna(score_value) and score_value != 0:
                    # Check for new record in score
                    if score_value > max_values[score_metric]:
                        max_values[score_metric] = score_value
                        # Highlight the record for score
                        axs['TRMRD_REC'].text(date + offset, score_y, f"{round(score_value)}",
                                            va='center', ha='center', fontsize=4, color='black',
                                            bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none', pad=0.15))
                    else:
                        # Regular annotation for score
                        axs['TRMRD_REC'].text(date + offset, score_y, f"{round(score_value)}",
                                            va='center', ha='center', fontsize=4, color='black')


    return fig





def turmzg_plot(data, start_date, current_date):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['TRMZG_REC', 'TRMZG_REC', 'TRMZG_REC'],
                                ['TRMZG', 'TRMZG', 'TRMZG'],
                                ['TRMZG', 'TRMZG', 'TRMZG'],
                                ],
                                figsize=(10, 5))
    plt.subplots_adjust(wspace=.2, hspace=.8)

    # fig.suptitle(f'''Training''', size=18)

    axs['TRMZG'].set_title(f"Progress Turmzug", size=12)
    axs['TRMZG'].set_xlabel(' ', size=14)
    axs['TRMZG'].set_ylabel('Reps', size=8)
    axs['TRMZG'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['TRMZG'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['TRMZG'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['TRMZG'].tick_params(axis='y', which='major', labelsize=6) 

    axs['TRMZG'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['TRMZG'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['TRMZG'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['TRMZG'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['TRMZG'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['TRMZG'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    axs['TRMZG'].bar(dates - pd.Timedelta(hours=10), data["Weighted Turm Zug set 1 reps"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['TRMZG'].bar(dates, data["Weighted Turm Zug set 2 reps"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['TRMZG'].bar(dates + pd.Timedelta(hours=10), data["Weighted Turm Zug set 3 reps"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")


    for set_name, offset in zip(["Weighted Turm Zug set 1 reps", "Weighted Turm Zug set 2 reps", "Weighted Turm Zug set 3 reps"], [-pd.Timedelta(hours=12), pd.Timedelta(0), pd.Timedelta(hours=12)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['TRMZG'].text(date + offset, value + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')
    
    for set_name, offset in zip(["Weighted Turm Zug set 1 weight", "Weighted Turm Zug set 2 weight", "Weighted Turm Zug set 3 weight"], [-pd.Timedelta(hours=14), pd.Timedelta(0), pd.Timedelta(hours=14)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['TRMZG'].text(date + offset, value/15 + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')  

    

    # axs['LGSTZ_REC'].set_title(f"Progress Liegestütz", size=10)
    axs['TRMZG_REC'].set_xlabel(' ', size=14)
    axs['TRMZG_REC'].set_ylabel('Reps', size=8)
    axs['TRMZG_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['TRMZG_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['TRMZG_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['TRMZG_REC'].tick_params(axis='y', which='major', labelsize=6) 

    axs['TRMZG_REC'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['TRMZG_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m'''))
    axs['TRMZG_REC'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['TRMZG_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['TRMZG_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['TRMZG_REC'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    axs['TRMZG_REC'].bar(dates - pd.Timedelta(hours=10), data["Turm Zug Average reps all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['TRMZG_REC'].bar(dates, data["Turm Zug Max reps all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['TRMZG_REC'].bar(dates + pd.Timedelta(hours=10), data["Turm Zug Sum reps all sets"], alpha=1, color="gray", width=bar_width, label="Amount")

    # Adding legend
    axs['TRMZG_REC'].legend(loc='best', fontsize=5)



    for set_name, offset in zip(["Turm Zug Average reps all sets", "Turm Zug Max reps all sets", "Turm Zug Sum reps all sets"], 
                            [-pd.Timedelta(hours=10), pd.Timedelta(0), pd.Timedelta(hours=10)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value) and value != 0:
                axs['TRMZG_REC'].text(date + offset, value + 1.5, f"{round(value)}", va='center', ha='center', fontsize=4, color='black')


    return fig





