import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import matplotlib.path as mpath
import matplotlib.dates as mdates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import matplotlib.image as mpimg
import seaborn as sns

from PIL import Image

import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker 

import pandas as pd 
import numpy as np

import os.path
import configparser

from datetime import datetime
from datetime import timedelta
import time

import calendar
import yaml
import json

from utils.utils import *
from utils.data_engineering import *


config_path = os.path.join("utils", "paths.ini")

@st.cache_data
def load_all_images(config_file=config_path):
    # Read paths from the ini file
    config = configparser.ConfigParser()
    config.read(config_file)

        # Ensure the section [img_paths] exists
    if 'img_paths' not in config:
        raise ValueError("Section 'img_paths' not found in the config file.")
    
    # Dictionary to store the images
    images = {}
    for key, path in config['img_paths'].items():
        try:
            images[key] = Image.open(path)  # Load the image and store it in the dictionary
        except FileNotFoundError:
            raise FileNotFoundError(f"Image at path '{path}' not found.")
    
    return images


# load images
images = load_all_images(config_path)
push_pic, knbg_pic, plnk_pic, hmcrl_pic, tmrd_pic, tmzg_pic = (images['push_pic'], images['knbg_pic'], images['plnk_pic'],
                                                               images['hmcrl_pic'],images['tmrd_pic'], images['tmzg_pic'])


def moving_average_plot(ax, data, name, window=3):
    # Filter out non-training days (where 'Liegestütz Average all sets' is not NaN)
    training_data = data.dropna(subset=[name])
    
    # Calculate moving average based on training days only
    ma_column = f'{name} MA{window}'
    training_data[ma_column] = training_data[name].rolling(window=window).mean()
    
    # Plot the moving average line
    sns.lineplot(
        data=training_data, 
        x=training_data.index, 
        y=ma_column, 
        linestyle='--', 
        linewidth=0.5,
        color="gray", 
        ax=ax
    )
    
    # Add scatter points for the moving average
    ax.scatter(training_data.index, training_data[ma_column], color="gray", s=10)


    
    
def pushup_plot(data, monthly_stats_data, start_date, current_date):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['LGSTZ_REC', 'LGSTZ_REC', 'LGSTZ_REC', 'LGSTZ_REC', 'LGSTZ_REC', 'LGSTZ_RECS'],
                                ['LGSTZ', 'LGSTZ', 'LGSTZ', 'LGSTZ', 'LGSTZ', 'LGSTZ_BX'],
                                ['LGSTZ', 'LGSTZ', 'LGSTZ', 'LGSTZ', 'LGSTZ', 'LGSTZ_BX']
                                ],
                                figsize=(10, 5))
    
    # Adjust the top margin to make space for the image and title
    plt.subplots_adjust(wspace=.2, hspace=.8, top=0.85)
    fig.suptitle(f'''Push Ups''', size=10, y=1)
    fig.patch.set_alpha(0.5)
    
    # Create an axes for the image in the upper left corner
    image_ax = fig.add_axes([0.07, 0.91, 0.25, 0.09], anchor='NW')  # [left, bottom, width, height]
    # Hide the axes frame and display the image in the axes
    image_ax.axis('off')
    image_ax.imshow(push_pic, alpha=0.6)

    
    axs['LGSTZ'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['LGSTZ'].set_title(f"Progress Push Ups", size=7)
    axs['LGSTZ'].set_xlabel(' ', size=14)
    axs['LGSTZ'].set_ylabel('Reps', size=8)
    axs['LGSTZ'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['LGSTZ'].set_ylim([0, 40])

    # Set font size for major and minor ticks
    axs['LGSTZ'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['LGSTZ'].tick_params(axis='x', which='minor', labelsize=5, rotation=45) 
    axs['LGSTZ'].tick_params(axis='y', which='major', labelsize=6)

    # Set major ticks and thick lines to be placed on the first of every month
    axs['LGSTZ'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['LGSTZ'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['LGSTZ'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)  

    axs['LGSTZ'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=())) # MO, TU, WE, TH, FR, SA, SU
    axs['LGSTZ'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['LGSTZ'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)


    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    axs['LGSTZ'].bar(dates - pd.Timedelta(hours=10), data["Liegestütz set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['LGSTZ'].bar(dates, data["Liegestütz set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['LGSTZ'].bar(dates + pd.Timedelta(hours=10), data["Liegestütz set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")

    for set_name, offset in zip(["Liegestütz set 1", "Liegestütz set 2", "Liegestütz set 3"], [-pd.Timedelta(hours=16), pd.Timedelta(0), pd.Timedelta(hours=16)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['LGSTZ'].text(date + offset, value + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')


    #Moving Average Plot
    moving_average_plot(ax=axs['LGSTZ'], data=data, name="Liegestütz Average all sets", window=3)

    axs['LGSTZ'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3) 


    # Records Plot
    axs['LGSTZ_REC'].set_title(f"Records Push Ups", size=7)
    axs['LGSTZ_REC'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['LGSTZ_REC'].set_xlabel(' ', size=14)
    axs['LGSTZ_REC'].set_ylabel('Reps', size=8)
    axs['LGSTZ_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['LGSTZ_REC'].set_ylim([0, 100])

    # Set font size for major and minor ticks
    axs['LGSTZ_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['LGSTZ_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['LGSTZ_REC'].tick_params(axis='y', which='major', labelsize=6) 

    # Set major ticks and thick lines to be placed on the first of every month
    axs['LGSTZ_REC'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['LGSTZ_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['LGSTZ_REC'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.3)  

    axs['LGSTZ_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['LGSTZ_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['LGSTZ_REC'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    axs['LGSTZ_REC'].bar(dates - pd.Timedelta(hours=10), data["Liegestütz Average all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['LGSTZ_REC'].bar(dates, data["Liegestütz Max all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['LGSTZ_REC'].bar(dates + pd.Timedelta(hours=10), data["Liegestütz Sum all sets"], alpha=1, color="gray", width=bar_width, label="Amount")



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
                    
    axs['LGSTZ_REC'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3) 



    # Statistics Plot
    # Reshape the data using pd.melt
    sets_columns = ["Liegestütz set 1", "Liegestütz set 2", "Liegestütz set 3"]
    lgstz_all_sets = data[sets_columns].melt(var_name='Set', value_name='Reps').dropna()

    # Clean up the 'Set' labels
    lgstz_all_sets['Set'] = lgstz_all_sets['Set'].str.replace('Liegestütz set ', 'Set ')

    # Add a constant column for x-axis grouping
    lgstz_all_sets['All Sets'] = 'All Sets'
    
    set_hue_palette = {'Set 1': 'limegreen', 'Set 2': 'dodgerblue', 'Set 3': 'darkviolet'}


    axs['LGSTZ_BX'].set_title(f"Push Ups Stats", size=7)
    axs['LGSTZ_BX'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['LGSTZ_BX'].set_xlabel(' ', size=8)
    axs['LGSTZ_BX'].yaxis.set_label_position("right")
    axs['LGSTZ_BX'].set_ylabel('Reps', size=8, labelpad=5)
    # axs['LGSTZ_BX'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['LGSTZ_BX'].set_ylim([0, 30])

    
    # Set font size for major and minor ticks
    axs['LGSTZ_BX'].tick_params(axis='x', which='major', labelsize=6, rotation=360)  
    axs['LGSTZ_BX'].tick_params(axis='x', which='minor', labelsize=6) 
    axs['LGSTZ_BX'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)

    # Set major ticks and thick lines to be placed on the first of every month
    # axs['LGSTZ_BX'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)  
    # axs['LGSTZ_BX'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

 
    # boxplot all sets
    sns.boxplot(data=lgstz_all_sets, x='All Sets', y='Reps', ax=axs['LGSTZ_BX'], color="lightgrey") 

    # Swarmplot with dodge
    sns.swarmplot(
        data=lgstz_all_sets,
        x='All Sets',
        y='Reps',
        hue='Set',
        palette=set_hue_palette,
        dodge=True,    # Automatically separates points by 'Set'
        size=3,
        ax=axs['LGSTZ_BX']
    )

    axs['LGSTZ_BX'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3, handletextpad=0.01, columnspacing=0.5)



    # THE RECORDS PLOT
    axs['LGSTZ_RECS'].set_title(f"Push Ups Records", size=7)
    axs['LGSTZ_RECS'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['LGSTZ_RECS'].set_xlabel(' ', size=8)
    axs['LGSTZ_RECS'].yaxis.set_label_position("right")
    axs['LGSTZ_RECS'].set_ylabel('Records', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['LGSTZ_RECS'].tick_params(axis='x', which='major', labelsize=6, rotation=45)
    axs['LGSTZ_RECS'].tick_params(axis='x', which='minor', labelsize=6)
    axs['LGSTZ_RECS'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['LGSTZ_RECS'].set_ylim([0, 8])

    # Define the exercise-specific categories for Liegestütz
    categories = ['Liegestütz Sum record broken', 'Liegestütz Max record broken', 'Liegestütz Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Liegestütz category

    # Define horizontal offsets for each category
    offset = 0.15  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['LGSTZ_RECS'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['LGSTZ_RECS'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['LGSTZ_RECS'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['LGSTZ_RECS'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=45)

    # Add grid
    axs['LGSTZ_RECS'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5)
    axs['LGSTZ_RECS'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.3)


   

    return fig


def plank_plot(data, monthly_stats_data, start_date, current_date):

    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['PLK_REC', 'PLK_REC', 'PLK_REC', 'PLK_REC', 'PLK_REC', 'PLK_RECS'],
                                ['PLK', 'PLK', 'PLK', 'PLK', 'PLK', 'PLK_BX'],
                                ['PLK', 'PLK', 'PLK', 'PLK', 'PLK', 'PLK_BX'],
                                ],
                                figsize=(10, 5))
    
    # Adjust the top margin to make space for the image and title
    plt.subplots_adjust(wspace=.2, hspace=.8, top=0.85)
    fig.patch.set_alpha(0.5)
    fig.suptitle(f'''Planke''', size=10, y=1)
    
    # Create an axes for the image in the upper left corner
    image_ax = fig.add_axes([0.07, 0.91, 0.25, 0.09], anchor='NW')  # [left, bottom, width, height]
    # Hide the axes frame and display the image in the axes
    image_ax.axis('off')
    image_ax.imshow(plnk_pic, alpha=0.5)


    axs['PLK'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['PLK'].set_title(f"Progress Planke", size=7)
    axs['PLK'].set_xlabel(' ', size=14)
    axs['PLK'].set_ylabel('Sec', size=8)
    axs['PLK'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['PLK'].set_ylim([0, 160])

    # Set font size for major and minor ticks
    axs['PLK'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['PLK'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['PLK'].tick_params(axis='y', which='major', labelsize=6)
     

    # Set major ticks and thick lines to be placed on the first of every month
    axs['PLK'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['PLK'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['PLK'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)  

    axs['PLK'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['PLK'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['PLK'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    axs['PLK'].bar(dates - pd.Timedelta(hours=12), data["Planke set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['PLK'].bar(dates, data["Planke set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['PLK'].bar(dates + pd.Timedelta(hours=12), data["Planke set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")


    for set_name, offset in zip(["Planke set 1", "Planke set 2", "Planke set 3"], [-pd.Timedelta(hours=22), pd.Timedelta(0), pd.Timedelta(hours=22)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['PLK'].text(date + offset, value + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')
    
    # Moving Average Plot
    moving_average_plot(ax=axs['PLK'], data=data, name="Planke Average all sets", window=3)

    axs['PLK'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3) 
    
    
    
    axs['PLK_REC'].set_title(f"Records Planke", size=7)
    axs['PLK_REC'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency
    axs['PLK_REC'].set_xlabel(' ', size=14)
    axs['PLK_REC'].set_ylabel('Sec', size=8)
    axs['PLK_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['PLK_REC'].set_ylim([0, 500])

    # Set font size for major and minor ticks
    axs['PLK_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['PLK_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['PLK_REC'].tick_params(axis='y', which='major', labelsize=6) 


    # Set major ticks and thick lines to be placed on the first of every month
    axs['PLK_REC'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['PLK_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['PLK_REC'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)  

    axs['PLK_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['PLK_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['PLK_REC'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    axs['PLK_REC'].bar(dates - pd.Timedelta(hours=10), data["Planke Average all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['PLK_REC'].bar(dates, data["Planke Max all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['PLK_REC'].bar(dates + pd.Timedelta(hours=10), data["Planke Sum all sets"], alpha=1, color="gray", width=bar_width, label="Amount")

    
    # Initialize dictionaries to keep track of the maximum values for each set name
    max_values = {
        "Planke Average all sets": -float('inf'),
        "Planke Max all sets": -float('inf'),
        "Planke Sum all sets": -float('inf')
    }

    # Iterate over the three metrics and add the annotation
    for set_name, offset in zip(
        ["Planke Average all sets", "Planke Max all sets", "Planke Sum all sets"], 
        [-pd.Timedelta(hours=14), pd.Timedelta(0), pd.Timedelta(hours=14)]
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
    
    axs['PLK_REC'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3)



    # Statistics Plot
    # Reshape the data using pd.melt
    sets_columns = ["Planke set 1", "Planke set 2", "Planke set 3"]
    plk_all_sets = data[sets_columns].melt(var_name='Set', value_name='Reps').dropna()

    # Clean up the 'Set' labels
    plk_all_sets['Set'] = plk_all_sets['Set'].str.replace('Planke set ', 'Set ')

    # Add a constant column for x-axis grouping
    plk_all_sets['All Sets'] = 'All Sets'
    
    set_hue_palette = {'Set 1': 'limegreen', 'Set 2': 'dodgerblue', 'Set 3': 'darkviolet'}


    axs['PLK_BX'].set_title(f"Planke Stats", size=7)
    axs['PLK_BX'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['PLK_BX'].set_xlabel(' ', size=8)
    axs['PLK_BX'].yaxis.set_label_position("right")
    axs['PLK_BX'].set_ylabel('Reps', size=8, labelpad=5)
    # axs['PLK_BX'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['PLK_BX'].set_ylim([0, 160])

    
    # Set font size for major and minor ticks
    axs['PLK_BX'].tick_params(axis='x', which='major', labelsize=6, rotation=360)  
    axs['PLK_BX'].tick_params(axis='x', which='minor', labelsize=6) 
    axs['PLK_BX'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)

    # Set major ticks and thick lines to be placed on the first of every month
    # axs['PLK_BX'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)  
    # axs['PLK_BX'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

 
    # boxplot all sets
    sns.boxplot(data=plk_all_sets, x='All Sets', y='Reps', ax=axs['PLK_BX'], color="lightgrey") 

    # Swarmplot with dodge
    sns.swarmplot(
        data=plk_all_sets,
        x='All Sets',
        y='Reps',
        hue='Set',
        palette=set_hue_palette,
        dodge=True,    # Automatically separates points by 'Set'
        size=3,
        ax=axs['PLK_BX']
    )

    axs['PLK_BX'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3, handletextpad=0.01, columnspacing=0.5)


    # THE RECORDS PLOT
    axs['PLK_RECS'].set_title(f"Planke Records", size=7)
    axs['PLK_RECS'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['PLK_RECS'].set_xlabel(' ', size=8)
    axs['PLK_RECS'].yaxis.set_label_position("right")
    axs['PLK_RECS'].set_ylabel('Records', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['PLK_RECS'].tick_params(axis='x', which='major', labelsize=6, rotation=45)
    axs['PLK_RECS'].tick_params(axis='x', which='minor', labelsize=6)
    axs['PLK_RECS'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['PLK_RECS'].set_ylim([0, 8])

    # Define the exercise-specific categories for Liegestütz
    categories = ['Planke Sum record broken', 'Planke Max record broken', 'Planke Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Liegestütz category

    # Define horizontal offsets for each category
    offset = 0.15  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['PLK_RECS'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['PLK_RECS'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['PLK_RECS'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['PLK_RECS'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=45)

    # Add grid
    axs['PLK_RECS'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5)
    axs['PLK_RECS'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.3)


    return fig



def kniebeuge_plot(data, monthly_stats_data, start_date, current_date):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['KNBG_REC', 'KNBG_REC', 'KNBG_REC', 'KNBG_REC', 'KNBG_REC', 'KNBG_RECS'],
                                ['KNBG', 'KNBG', 'KNBG', 'KNBG', 'KNBG', 'KNBG_BX'],
                                ['KNBG', 'KNBG', 'KNBG', 'KNBG', 'KNBG', 'KNBG_BX'],
                                ],
                                figsize=(10, 5))
    
    plt.subplots_adjust(wspace=.2, hspace=.8, top=0.85)
    fig.patch.set_alpha(0.5)
    fig.suptitle(f'''Kniebeugen''', size=10, y=1)
    
    # Create an axes for the image in the upper left corner
    image_ax = fig.add_axes([0.07, 0.91, 0.25, 0.09], anchor='NW')  # [left, bottom, width, height]
    # Hide the axes frame and display the image in the axes
    image_ax.axis('off')
    image_ax.imshow(knbg_pic, alpha=0.5)


    
    axs['KNBG'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['KNBG'].set_title(f"Progress Kniebeugen", size=7)
    axs['KNBG'].set_xlabel(' ', size=14)
    axs['KNBG'].set_ylabel('Reps', size=8)
    axs['KNBG'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['KNBG'].set_ylim([0, 60])

    # Set font size for major and minor ticks
    axs['KNBG'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['KNBG'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['KNBG'].tick_params(axis='y', which='major', labelsize=6) 

    # Set major ticks and thick lines to be placed on the first of every month
    axs['KNBG'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['KNBG'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['KNBG'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)

    axs['KNBG'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['KNBG'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['KNBG'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    axs['KNBG'].bar(dates - pd.Timedelta(hours=10), data["Kniebeugen set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['KNBG'].bar(dates, data["Kniebeugen set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['KNBG'].bar(dates + pd.Timedelta(hours=10), data["Kniebeugen set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")


    for set_name, offset in zip(["Kniebeugen set 1", "Kniebeugen set 2", "Kniebeugen set 3"], [-pd.Timedelta(hours=16), pd.Timedelta(0), pd.Timedelta(hours=16)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['KNBG'].text(date + offset, value + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')
    

    # Moving Average Plot
    moving_average_plot(ax=axs['KNBG'], data=data, name="Kniebeugen Average all sets", window=3)

    axs['KNBG'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3) 
    

    axs['KNBG_REC'].set_title(f"Records Kniebeugen", size=7)
    axs['KNBG_REC'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency
    axs['KNBG_REC'].set_xlabel(' ', size=14)
    axs['KNBG_REC'].set_ylabel('Reps', size=8)
    axs['KNBG_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['KNBG_REC'].set_ylim([0, 120])

    # Set font size for major and minor ticks
    axs['KNBG_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['KNBG_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['KNBG_REC'].tick_params(axis='y', which='major', labelsize=6) 

    # Set major ticks and thick lines to be placed on the first of every month
    axs['KNBG_REC'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['KNBG_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['KNBG_REC'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)

    axs['KNBG_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['KNBG_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['KNBG_REC'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    axs['KNBG_REC'].bar(dates - pd.Timedelta(hours=10), data["Kniebeugen Average all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['KNBG_REC'].bar(dates, data["Kniebeugen Max all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['KNBG_REC'].bar(dates + pd.Timedelta(hours=10), data["Kniebeugen Sum all sets"], alpha=1, color="gray", width=bar_width, label="Amount")


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

    axs['KNBG_REC'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3) 

    
    
    # Statistics Plot
    # Reshape the data using pd.melt
    sets_columns = ["Kniebeugen set 1", "Kniebeugen set 2", "Kniebeugen set 3"]
    knbg_all_sets = data[sets_columns].melt(var_name='Set', value_name='Reps').dropna()

    # Clean up the 'Set' labels
    knbg_all_sets['Set'] = knbg_all_sets['Set'].str.replace('Kniebeugen set ', 'Set ')

    # Add a constant column for x-axis grouping
    knbg_all_sets['All Sets'] = 'All Sets'
    
    set_hue_palette = {'Set 1': 'limegreen', 'Set 2': 'dodgerblue', 'Set 3': 'darkviolet'}


    axs['KNBG_BX'].set_title(f"Kniebeugen Stats", size=7)
    axs['KNBG_BX'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['KNBG_BX'].set_xlabel(' ', size=8)
    axs['KNBG_BX'].yaxis.set_label_position("right")
    axs['KNBG_BX'].set_ylabel('Reps', size=8, labelpad=5)
    # axs['KNBG_BX'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['KNBG_BX'].set_ylim([0, 50])

    
    # Set font size for major and minor ticks
    axs['KNBG_BX'].tick_params(axis='x', which='major', labelsize=6, rotation=360)  
    axs['KNBG_BX'].tick_params(axis='x', which='minor', labelsize=6) 
    axs['KNBG_BX'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)

    # Set major ticks and thick lines to be placed on the first of every month
    # axs['KNBG_BX'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)  
    # axs['KNBG_BX'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    # boxplot all sets
    sns.boxplot(data=knbg_all_sets, x='All Sets', y='Reps', ax=axs['KNBG_BX'], color="lightgrey") 

    # Swarmplot with dodge
    sns.swarmplot(
        data=knbg_all_sets,
        x='All Sets',
        y='Reps',
        hue='Set',
        palette=set_hue_palette,
        dodge=True,    # Automatically separates points by 'Set'
        size=3,
        ax=axs['KNBG_BX']
    )

    axs['KNBG_BX'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3, handletextpad=0.01, columnspacing=0.5)





    # THE RECORDS PLOT
    axs['KNBG_RECS'].set_title(f"Kniebeugen Records", size=7)
    axs['KNBG_RECS'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['KNBG_RECS'].set_xlabel(' ', size=8)
    axs['KNBG_RECS'].yaxis.set_label_position("right")
    axs['KNBG_RECS'].set_ylabel('Records', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['KNBG_RECS'].tick_params(axis='x', which='major', labelsize=6, rotation=45)
    axs['KNBG_RECS'].tick_params(axis='x', which='minor', labelsize=6)
    axs['KNBG_RECS'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['KNBG_RECS'].set_ylim([0, 8])

    # Define the exercise-specific categories for Liegestütz
    categories = ['Kniebeugen Sum record broken', 'Kniebeugen Max record broken', 'Kniebeugen Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Liegestütz category

    # Define horizontal offsets for each category
    offset = 0.15  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['KNBG_RECS'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['KNBG_RECS'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['KNBG_RECS'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['KNBG_RECS'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=45)

    # Add grid
    axs['KNBG_RECS'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['KNBG_RECS'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.3)

    return fig


def hamcurls_plot(data, monthly_stats_data, start_date, current_date):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['HMCRL_REC', 'HMCRL_REC', 'HMCRL_REC', 'HMCRL_REC', 'HMCRL_REC', 'HMCRL_RECS'],
                                ['HMCRL', 'HMCRL', 'HMCRL', 'HMCRL', 'HMCRL', 'HMCRL_BX'],
                                ['HMCRL', 'HMCRL', 'HMCRL', 'HMCRL', 'HMCRL', 'HMCRL_BX'],
                                ],
                                figsize=(10, 5))
    
    plt.subplots_adjust(wspace=.2, hspace=.8, top=0.85)
    fig.suptitle(f'''Hammer Curls''', size=10, y=1) 
    fig.patch.set_alpha(0.5)
    
    # Create an axes for the image in the upper left corner
    image_ax = fig.add_axes([0.07, 0.91, 0.25, 0.09], anchor='NW')  # [left, bottom, width, height]
    # Hide the axes frame and display the image in the axes
    image_ax.axis('off')
    image_ax.imshow(hmcrl_pic, alpha=0.5)


    axs['HMCRL'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['HMCRL'].set_title(f"Progress Hammer Curls", size=7)
    axs['HMCRL'].set_xlabel(' ', size=14)
    axs['HMCRL'].set_ylabel('Reps', size=8)
    axs['HMCRL'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['HMCRL'].set_ylim([0, 35])

    # Set font size for major and minor ticks
    axs['HMCRL'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['HMCRL'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['HMCRL'].tick_params(axis='y', which='major', labelsize=6) 

    # Set major ticks and thick lines to be placed on the first of every month
    axs['HMCRL'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['HMCRL'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['HMCRL'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)  

    axs['HMCRL'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['HMCRL'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['HMCRL'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    axs['HMCRL'].bar(dates - pd.Timedelta(hours=10), data["Weighted Hammer Curls set 1 reps"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['HMCRL'].bar(dates, data["Weighted Hammer Curls set 2 reps"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['HMCRL'].bar(dates + pd.Timedelta(hours=10), data["Weighted Hammer Curls set 3 reps"], alpha=1, color="darkviolet", width=bar_width, label="Set 3") 

    for set_name, offset in zip(["Weighted Hammer Curls set 1 reps", "Weighted Hammer Curls set 2 reps", "Weighted Hammer Curls set 3 reps"], [-pd.Timedelta(hours=16), pd.Timedelta(0), pd.Timedelta(hours=12)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['HMCRL'].text(date + offset, value + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')
    
    for set_name, offset in zip(["Weighted Hammer Curls set 1 weight", "Weighted Hammer Curls set 2 weight", "Weighted Hammer Curls set 3 weight"], [-pd.Timedelta(hours=16), pd.Timedelta(0), pd.Timedelta(hours=12)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['HMCRL'].text(date + offset, value/2 + 0.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')
    

    # Moving Average Plot
    moving_average_plot(ax=axs['HMCRL'], data=data, name="Weighted Hammer Curls Average reps all sets", window=3)

    axs['HMCRL'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3) 


    axs['HMCRL_REC'].set_title(f"Records Hammer Curls", size=7)
    axs['HMCRL_REC'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency
    axs['HMCRL_REC'].set_xlabel(' ', size=14)
    axs['HMCRL_REC'].set_ylabel('Reps', size=8)
    axs['HMCRL_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['HMCRL_REC'].set_ylim([0, 120])

    # Set font size for major and minor ticks
    axs['HMCRL_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['HMCRL_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['HMCRL_REC'].tick_params(axis='y', which='major', labelsize=6) 

    # Set major ticks and thick lines to be placed on the first of every month
    axs['HMCRL_REC'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['HMCRL_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['HMCRL_REC'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)

    axs['HMCRL_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['HMCRL_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['HMCRL_REC'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    axs['HMCRL_REC'].bar(dates - pd.Timedelta(hours=10), data["Weighted Hammer Curls Average reps all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['HMCRL_REC'].bar(dates, data["Weighted Hammer Curls Max reps all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['HMCRL_REC'].bar(dates + pd.Timedelta(hours=10), data["Weighted Hammer Curls Sum reps all sets"], alpha=1, color="gray", width=bar_width, label="Amount")



    # Initialize dictionaries to keep track of the maximum values for each metric
    max_values = {
        "Weighted Hammer Curls Average reps all sets": -float('inf'),
        "Weighted Hammer Curls Max reps all sets": -float('inf'),
        "Weighted Hammer Curls Sum reps all sets": -float('inf'),
        "Weighted Hammer Curls Average score all sets": -float('inf'),
        "Weighted Hammer Curls Max score all sets": -float('inf'),
        "Weighted Hammer Curls Sum score all sets": -float('inf')
    }

    # Iterate over the metrics and add the annotations
    for reps_metric, score_metric, offset in zip(
        ["Weighted Hammer Curls Average reps all sets", "Weighted Hammer Curls Max reps all sets", "Weighted Hammer Curls Sum reps all sets"],
        ["Weighted Hammer Curls Average score all sets", "Weighted Hammer Curls Max score all sets", "Weighted Hammer Curls Sum score all sets"],
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

    axs['HMCRL_REC'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3) 


    # Statistics Plot
    # Reshape the data using pd.melt
    sets_columns = ["Weighted Hammer Curls set 1 reps", "Weighted Hammer Curls set 2 reps", "Weighted Hammer Curls set 3 reps"]
    hmcrl_all_sets = data[sets_columns].melt(var_name='Set', value_name='Reps').dropna()

    # Clean up the 'Set' labels
    hmcrl_all_sets['Set'] = hmcrl_all_sets['Set'].str.replace('Weighted Hammer Curls set ', 'Set ')

    # Add a constant column for x-axis grouping
    hmcrl_all_sets['All Sets'] = 'All Sets'
    
    set_hue_palette = {'Set 1 reps': 'limegreen', 'Set 2 reps': 'dodgerblue', 'Set 3 reps': 'darkviolet'}


    axs['HMCRL_BX'].set_title(f"Hammer Curls Stats", size=7)
    axs['HMCRL_BX'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['HMCRL_BX'].set_xlabel(' ', size=8)
    axs['HMCRL_BX'].yaxis.set_label_position("right")
    axs['HMCRL_BX'].set_ylabel('Reps', size=8, labelpad=5)
    # axs['HMCRL_BX'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['HMCRL_BX'].set_ylim([0, 30])

    
    # Set font size for major and minor ticks
    axs['HMCRL_BX'].tick_params(axis='x', which='major', labelsize=6, rotation=360)  
    axs['HMCRL_BX'].tick_params(axis='x', which='minor', labelsize=6) 
    axs['HMCRL_BX'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)

    # Set major ticks and thick lines to be placed on the first of every month
    # axs['HMCRL_BX'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)  
    # axs['HMCRL_BX'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    # boxplot all sets
    sns.boxplot(data=hmcrl_all_sets, x='All Sets', y='Reps', ax=axs['HMCRL_BX'], color="lightgrey") 

    # Swarmplot with dodge
    sns.swarmplot(
        data=hmcrl_all_sets,
        x='All Sets',
        y='Reps',
        hue='Set',
        palette=set_hue_palette,
        dodge=True,    # Automatically separates points by 'Set'
        size=3,
        ax=axs['HMCRL_BX']
    )

    axs['HMCRL_BX'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=1, handletextpad=0.01, columnspacing=0.5)


    # THE RECORDS PLOT
    axs['HMCRL_RECS'].set_title(f"Hammer Curls Records", size=7)
    axs['HMCRL_RECS'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['HMCRL_RECS'].set_xlabel(' ', size=8)
    axs['HMCRL_RECS'].yaxis.set_label_position("right")
    axs['HMCRL_RECS'].set_ylabel('Records', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['HMCRL_RECS'].tick_params(axis='x', which='major', labelsize=6, rotation=45)
    axs['HMCRL_RECS'].tick_params(axis='x', which='minor', labelsize=6)
    axs['HMCRL_RECS'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['HMCRL_RECS'].set_ylim([0, 8])

    # Define the exercise-specific categories for Liegestütz
    categories = ['Weighted Hammer Curls Sum record broken', 'Weighted Hammer Curls Max record broken', 'Weighted Hammer Curls Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Liegestütz category

    # Define horizontal offsets for each category
    offset = 0.15  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['HMCRL_RECS'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['HMCRL_RECS'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['HMCRL_RECS'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['HMCRL_RECS'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=45)

    # Add grid
    axs['HMCRL_RECS'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['HMCRL_RECS'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.3)

    return fig




def turmrud_plot(data, monthly_stats_data, start_date, current_date):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['TRMRD_REC', 'TRMRD_REC', 'TRMRD_REC', 'TRMRD_REC', 'TRMRD_REC', 'TRMRD_RECS'],
                                ['TRMRD', 'TRMRD', 'TRMRD', 'TRMRD', 'TRMRD', 'TRMRD_BX'],
                                ['TRMRD', 'TRMRD', 'TRMRD', 'TRMRD', 'TRMRD', 'TRMRD_BX'],
                                ],
                                figsize=(10, 5))
    
    plt.subplots_adjust(wspace=.2, hspace=.8, top=0.85)
    fig.suptitle(f'''Turm Rudern''', size=10, y=1)
    fig.patch.set_alpha(0.5)
    
    # Create an axes for the image in the upper left corner
    image_ax = fig.add_axes([0.07, 0.91, 0.25, 0.09], anchor='NW')  # [left, bottom, width, height]
    # Hide the axes frame and display the image in the axes
    image_ax.axis('off')
    image_ax.imshow(tmrd_pic, alpha=0.5)



    axs['TRMRD'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency
    axs['TRMRD'].set_title(f"Progress Turm Rudern", size=7)
    axs['TRMRD'].set_xlabel(' ', size=14)
    axs['TRMRD'].set_ylabel('Reps', size=8)
    axs['TRMRD'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['TRMRD'].set_ylim([0, 70])

    # Set font size for major and minor ticks
    axs['TRMRD'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['TRMRD'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['TRMRD'].tick_params(axis='y', which='major', labelsize=6) 

    # Set major ticks and thick lines to be placed on the first of every month
    axs['TRMRD'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['TRMRD'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['TRMRD'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5) 

    axs['TRMRD'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['TRMRD'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['TRMRD'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.3
    dates = data.index

    # weighscoring bar
    axs['TRMRD'].bar(dates - pd.Timedelta(hours=10), data["Weightscore diff Turm Rudern set 1 reps"], alpha=0.3, width=bar_width, color="red", label="weightscoring")
    axs['TRMRD'].bar(dates, data["Weightscore diff Turm Rudern set 2 reps"], alpha=0.3, width=bar_width, color="red")
    axs['TRMRD'].bar(dates + pd.Timedelta(hours=10), data["Weightscore diff Turm Rudern set 3 reps"], alpha=0.3, color="red", width=bar_width)

    # Now plot the regular set bars on top of the weightscore bars using the `bottom` parameter
    axs['TRMRD'].bar(dates - pd.Timedelta(hours=10), data["Weighted Turm Rudern set 1 reps"], alpha=1, width=bar_width, color="limegreen", label="Set 1", 
                    bottom=data["Weightscore diff Turm Rudern set 1 reps"])  # Stacked on weightscore bars
    axs['TRMRD'].bar(dates, data["Weighted Turm Rudern set 2 reps"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2", 
                    bottom=data["Weightscore diff Turm Rudern set 2 reps"])  # Stacked on weightscore bars
    axs['TRMRD'].bar(dates + pd.Timedelta(hours=10), data["Weighted Turm Rudern set 3 reps"], alpha=1, color="darkviolet", width=bar_width, label="Set 3", 
                    bottom=data["Weightscore diff Turm Rudern set 3 reps"])  # Stacked on weightscore bars


    # Adjust the text labels to be placed at the top of the combined bars (reps + weightscore)
    for set_name, score_name, offset in zip(["Weighted Turm Rudern set 1 reps", "Weighted Turm Rudern set 2 reps", "Weighted Turm Rudern set 3 reps"],
                                            ["Weightscore diff Turm Rudern set 1 reps", "Weightscore diff Turm Rudern set 2 reps", "Weightscore diff Turm Rudern set 3 reps"],
                                            [-pd.Timedelta(hours=16), pd.Timedelta(0), pd.Timedelta(hours=16)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            score_value = data[score_name].loc[date]  # Get weightscore value for the same date
            combined_value = value + score_value  # Combine reps + weightscore to determine text height
            if not pd.isna(value):
                axs['TRMRD'].text(date + offset, combined_value + 1.5, f"{round(value)}", va='center', ha='center', fontsize=5, color='black')  # Text remains reps but height is adjusted
    
    for set_name, offset in zip(["Weighted Turm Rudern set 1 band", "Weighted Turm Rudern set 2 band", "Weighted Turm Rudern set 3 band"], [-pd.Timedelta(hours=16), pd.Timedelta(0), pd.Timedelta(hours=16)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['TRMRD'].text(date + offset, value/10 + 3, f"{round(value)}", va='center', ha='center', fontsize=4.5, color='black') 
    
    for set_name, offset in zip(["Weighted Turm Rudern set 1 distance", "Weighted Turm Rudern set 2 distance", "Weighted Turm Rudern set 3 distance"], [-pd.Timedelta(hours=16), pd.Timedelta(0), pd.Timedelta(hours=16)]):
        for date, value in data[set_name].loc[start_date:current_date].items():
            if not pd.isna(value):
                axs['TRMRD'].text(date + offset, value/6 + 1, f"{value}", va='center', ha='center', fontsize=4, color='black')


    # # Moving Average Plot
    # moving_average_plot(ax=axs['TRMRD'], data=data, name="Weighted Turm Rudern Average reps all sets", window=3)
    # Moving Average Plot scored
    moving_average_plot(ax=axs['TRMRD'], data=data, name="Weighted Turm Rudern Average score all sets", window=3)

    axs['TRMRD'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=4)






    axs['TRMRD_REC'].set_title(f"Records Turm Rudern", size=7)
    axs['TRMRD_REC'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency
    axs['TRMRD_REC'].set_xlabel(' ', size=14)
    axs['TRMRD_REC'].set_ylabel('Reps', size=8)
    axs['TRMRD_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['TRMRD_REC'].set_ylim([0, 100])

    # Set font size for major and minor ticks
    axs['TRMRD_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['TRMRD_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['TRMRD_REC'].tick_params(axis='y', which='major', labelsize=6) 

    # Set major ticks and thick lines to be placed on the first of every month
    axs['TRMRD_REC'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['TRMRD_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['TRMRD_REC'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5) 

    axs['TRMRD_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['TRMRD_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['TRMRD_REC'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    axs['TRMRD_REC'].bar(dates - pd.Timedelta(hours=10), data["Weighted Turm Rudern Average reps all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['TRMRD_REC'].bar(dates, data["Weighted Turm Rudern Max reps all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['TRMRD_REC'].bar(dates + pd.Timedelta(hours=10), data["Weighted Turm Rudern Sum reps all sets"], alpha=1, color="gray", width=bar_width, label="Amount")



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

    axs['TRMRD_REC'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3)


    # Statistics Plot
    # Reshape the data using pd.melt
    sets_columns = ["Weighted Turm Rudern set 1 reps", "Weighted Turm Rudern set 2 reps", "Weighted Turm Rudern set 3 reps"]
    trmrd_all_sets = data[sets_columns].melt(var_name='Set', value_name='Reps').dropna()

    # Clean up the 'Set' labels
    trmrd_all_sets['Set'] = trmrd_all_sets['Set'].str.replace('Weighted Turm Rudern set ', 'Set ')

    # Add a constant column for x-axis grouping
    trmrd_all_sets['All Sets'] = 'All Sets'
    
    set_hue_palette = {'Set 1 reps': 'limegreen', 'Set 2 reps': 'dodgerblue', 'Set 3 reps': 'darkviolet'}


    axs['TRMRD_BX'].set_title(f"Turm Rudern Stats", size=7)
    axs['TRMRD_BX'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['TRMRD_BX'].set_xlabel(' ', size=8)
    axs['TRMRD_BX'].yaxis.set_label_position("right")
    axs['TRMRD_BX'].set_ylabel('Reps', size=8, labelpad=5)
    # axs['TRMRD_BX'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['TRMRD_BX'].set_ylim([0, 40])

    
    # Set font size for major and minor ticks
    axs['TRMRD_BX'].tick_params(axis='x', which='major', labelsize=6, rotation=360)  
    axs['TRMRD_BX'].tick_params(axis='x', which='minor', labelsize=6) 
    axs['TRMRD_BX'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)

    # Set major ticks and thick lines to be placed on the first of every month
    # axs['TRMRD_BX'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)  
    # axs['TRMRD_BX'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    # boxplot all sets
    sns.boxplot(data=trmrd_all_sets, x='All Sets', y='Reps', ax=axs['TRMRD_BX'], color="lightgrey") 

    # Swarmplot with dodge
    sns.swarmplot(
        data=trmrd_all_sets,
        x='All Sets',
        y='Reps',
        hue='Set',
        palette=set_hue_palette,
        dodge=True,    # Automatically separates points by 'Set'
        size=3,
        ax=axs['TRMRD_BX']
    )

    axs['TRMRD_BX'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=1, handletextpad=0.01, columnspacing=0.5)


    # THE RECORDS PLOT
    axs['TRMRD_RECS'].set_title(f"Turm Rudern Records", size=7)
    axs['TRMRD_RECS'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['TRMRD_RECS'].set_xlabel(' ', size=8)
    axs['TRMRD_RECS'].yaxis.set_label_position("right")
    axs['TRMRD_RECS'].set_ylabel('Records', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['TRMRD_RECS'].tick_params(axis='x', which='major', labelsize=6, rotation=45)
    axs['TRMRD_RECS'].tick_params(axis='x', which='minor', labelsize=6)
    axs['TRMRD_RECS'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['TRMRD_RECS'].set_ylim([0, 8])

    # Define the exercise-specific categories for Liegestütz
    categories = ['Weighted Turm Rudern Sum record broken', 'Weighted Turm Rudern Max record broken', 'Weighted Turm Rudern Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Liegestütz category

    # Define horizontal offsets for each category
    offset = 0.15  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['TRMRD_RECS'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['TRMRD_RECS'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['TRMRD_RECS'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['TRMRD_RECS'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=45)

    # Add grid
    axs['TRMRD_RECS'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['TRMRD_RECS'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.3)

    return fig





def turmzg_plot(data, monthly_stats_data, start_date, current_date):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['TRMZG_REC', 'TRMZG_REC', 'TRMZG_REC','TRMZG_REC', 'TRMZG_REC', 'TRMZG_RECS'],
                                ['TRMZG', 'TRMZG', 'TRMZG', 'TRMZG', 'TRMZG', 'TRMZG_BX'],
                                ['TRMZG', 'TRMZG', 'TRMZG', 'TRMZG', 'TRMZG', 'TRMZG_BX'],
                                ],
                                figsize=(10, 5))
    
    plt.subplots_adjust(wspace=.2, hspace=.8, top=0.85)
    fig.suptitle(f'''Turm Zug''', size=10, y=1)
    fig.patch.set_alpha(0.5)
    
    # Create an axes for the image in the upper left corner
    image_ax = fig.add_axes([0.07, 0.91, 0.25, 0.09], anchor='NW')  # [left, bottom, width, height]
    # Hide the axes frame and display the image in the axes
    image_ax.axis('off')
    image_ax.imshow(tmzg_pic, alpha=0.5)

    axs['TRMZG'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency
    axs['TRMZG'].set_title(f"Progress Turm Zug", size=7)
    axs['TRMZG'].set_xlabel(' ', size=14)
    axs['TRMZG'].set_ylabel('Reps', size=8)
    axs['TRMZG'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['TRMZG'].set_ylim([0, 40])

    # Set font size for major and minor ticks
    axs['TRMZG'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['TRMZG'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['TRMZG'].tick_params(axis='y', which='major', labelsize=6) 

    # Set major ticks and thick lines to be placed on the first of every month
    axs['TRMZG'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['TRMZG'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['TRMZG'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5) 

    axs['TRMZG'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['TRMZG'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['TRMZG'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

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

    # Moving Average Plot
    moving_average_plot(ax=axs['TRMZG'], data=data, name="Weighted Turm Zug Average reps all sets", window=3)

    axs['TRMZG'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3)


    axs['TRMZG_REC'].set_title(f"Records Turm Zug", size=7)
    axs['TRMZG_REC'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency
    axs['TRMZG_REC'].set_xlabel(' ', size=14)
    axs['TRMZG_REC'].set_ylabel('Reps', size=8)
    axs['TRMZG_REC'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['TRMZG_REC'].set_ylim([0, 100])

    # Set font size for major and minor ticks
    axs['TRMZG_REC'].tick_params(axis='x', which='major', labelsize=5, rotation=45)  
    axs['TRMZG_REC'].tick_params(axis='x', which='minor', labelsize=5, rotation=45)
    axs['TRMZG_REC'].tick_params(axis='y', which='major', labelsize=6) 

    # Set major ticks and thick lines to be placed on the first of every month
    axs['TRMZG_REC'].xaxis.set_major_locator(mdates.MonthLocator())  
    axs['TRMZG_REC'].xaxis.set_major_formatter(mdates.DateFormatter('''%a %d.%m''')) 
    axs['TRMZG_REC'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5) 

    axs['TRMZG_REC'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=()))
    axs['TRMZG_REC'].xaxis.set_minor_formatter(mdates.DateFormatter('''%a %d.%m''')) # \n %a'
    axs['TRMZG_REC'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    axs['TRMZG_REC'].bar(dates - pd.Timedelta(hours=10), data["Weighted Turm Zug Average reps all sets"], alpha=1, width=bar_width, color="green", label="Average")
    axs['TRMZG_REC'].bar(dates, data["Weighted Turm Zug Max reps all sets"], alpha=1, width=bar_width, color="gold", label="Max")
    axs['TRMZG_REC'].bar(dates + pd.Timedelta(hours=10), data["Weighted Turm Zug Sum reps all sets"], alpha=1, color="gray", width=bar_width, label="Amount")


    # Initialize dictionaries to keep track of the maximum values for each metric
    max_values = {
        "Weighted Turm Zug Average reps all sets": -float('inf'),
        "Weighted Turm Zug Max reps all sets": -float('inf'),
        "Weighted Turm Zug Sum reps all sets": -float('inf'),
        "Weighted Turm Zug Average score all sets": -float('inf'),
        "Weighted Turm Zug Max score all sets": -float('inf'),
        "Weighted Turm Zug Sum score all sets": -float('inf')
    }

    # Iterate over the metrics and add the annotations
    for reps_metric, score_metric, offset in zip(
        ["Weighted Turm Zug Average reps all sets", "Weighted Turm Zug Max reps all sets", "Weighted Turm Zug Sum reps all sets"],
        ["Weighted Turm Zug Average score all sets", "Weighted Turm Zug Max score all sets", "Weighted Turm Zug Sum score all sets"],
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
                    axs['TRMZG_REC'].text(date + offset, reps_value + 0.5, f"{round(reps_value)}",
                                        va='center', ha='center', fontsize=4, color='black',
                                        bbox=dict(facecolor='green', alpha=0.3, edgecolor='none', pad=0.15))
                else:
                    # Regular annotation for reps
                    axs['TRMZG_REC'].text(date + offset, reps_value + 0.5, f"{round(reps_value)}",
                                        va='center', ha='center', fontsize=4, color='black')

                # Now, annotate the score above the reps annotation
                # Adjust the y-position by adding an additional offset
                score_y = reps_value + 10  # Adjust this value as needed to position the score annotation above
                if not pd.isna(score_value) and score_value != 0:
                    # Check for new record in score
                    if score_value > max_values[score_metric]:
                        max_values[score_metric] = score_value
                        # Highlight the record for score
                        axs['TRMZG_REC'].text(date + offset, score_y, f"{round(score_value)}",
                                            va='center', ha='center', fontsize=4, color='black',
                                            bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none', pad=0.15))
                    else:
                        # Regular annotation for score
                        axs['TRMZG_REC'].text(date + offset, score_y, f"{round(score_value)}",
                                            va='center', ha='center', fontsize=4, color='black')
    
    axs['TRMZG_REC'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=3)



    # Statistics Plot
    # Reshape the data using pd.melt
    sets_columns = ["Weighted Turm Zug set 1 reps", "Weighted Turm Zug set 2 reps", "Weighted Turm Zug set 3 reps"]
    trmzg_all_sets = data[sets_columns].melt(var_name='Set', value_name='Reps').dropna()

    # Clean up the 'Set' labels
    trmzg_all_sets['Set'] = trmzg_all_sets['Set'].str.replace('Weighted Turm Zug set ', 'Set ')

    # Add a constant column for x-axis grouping
    trmzg_all_sets['All Sets'] = 'All Sets'
    
    set_hue_palette = {'Set 1 reps': 'limegreen', 'Set 2 reps': 'dodgerblue', 'Set 3 reps': 'darkviolet'}


    axs['TRMZG_BX'].set_title(f"Turm Zug Stats", size=7)
    axs['TRMZG_BX'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['TRMZG_BX'].set_xlabel(' ', size=8)
    axs['TRMZG_BX'].yaxis.set_label_position("right")
    axs['TRMZG_BX'].set_ylabel('Reps', size=8, labelpad=5)
    # axs['TRMZG_BX'].set_xlim([pd.to_datetime(start_date), pd.to_datetime(current_date)]), 
    axs['TRMZG_BX'].set_ylim([0, 35])

    
    # Set font size for major and minor ticks
    axs['TRMZG_BX'].tick_params(axis='x', which='major', labelsize=6, rotation=360)  
    axs['TRMZG_BX'].tick_params(axis='x', which='minor', labelsize=6) 
    axs['TRMZG_BX'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)

    # Set major ticks and thick lines to be placed on the first of every month
    # axs['TRMZG_BX'].grid(visible=True, which='major', color='black', axis='x', linestyle='--', linewidth=0.5)  
    # axs['TRMZG_BX'].grid(visible=True, which='minor', color='gray', axis='x', linestyle='--', linewidth=0.3)

    # boxplot all sets
    sns.boxplot(data=trmzg_all_sets, x='All Sets', y='Reps', ax=axs['TRMZG_BX'], color="lightgrey") 

    # Swarmplot with dodge
    sns.swarmplot(
        data=trmzg_all_sets,
        x='All Sets',
        y='Reps',
        hue='Set',
        palette=set_hue_palette,
        dodge=True,    # Automatically separates points by 'Set'
        size=3,
        ax=axs['TRMZG_BX']
    )

    axs['TRMZG_BX'].legend(loc='upper right', borderaxespad=0.1, fontsize=5, ncol=1, handletextpad=0.01, columnspacing=0.5)


    # THE RECORDS PLOT
    axs['TRMZG_RECS'].set_title(f"Turm Zug Records", size=7)
    axs['TRMZG_RECS'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['TRMZG_RECS'].set_xlabel(' ', size=8)
    axs['TRMZG_RECS'].yaxis.set_label_position("right")
    axs['TRMZG_RECS'].set_ylabel('Records', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['TRMZG_RECS'].tick_params(axis='x', which='major', labelsize=6, rotation=45)
    axs['TRMZG_RECS'].tick_params(axis='x', which='minor', labelsize=6)
    axs['TRMZG_RECS'].tick_params(axis='y', labelright=True, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['TRMZG_RECS'].set_ylim([0, 8])

    # Define the exercise-specific categories for Liegestütz
    categories = ['Weighted Turm Zug Sum record broken', 'Weighted Turm Zug Max record broken', 'Weighted Turm Zug Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Liegestütz category

    # Define horizontal offsets for each category
    offset = 0.15  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['TRMZG_RECS'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['TRMZG_RECS'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['TRMZG_RECS'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['TRMZG_RECS'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=45)

    # Add grid
    axs['TRMZG_RECS'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['TRMZG_RECS'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.3)
    

    return fig




def rec_overview_plot(data, monthly_stats_data):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic(
                                [['PUSH_PIC', 'PUSH', 'PUSH', 'PUSH', 'PUSH', 'PUSH_SUM', 'PUSH_SUM'],
                                ['KNBG_PIC', 'KNBG', 'KNBG', 'KNBG', 'KNBG', 'KNBG_SUM', 'KNBG_SUM'],
                                ['PLNK_PIC', 'PLNK', 'PLNK', 'PLNK', 'PLNK', 'PLNK_SUM', 'PLNK_SUM'],
                                ['HMCRL_PIC', 'HMCRL', 'HMCRL', 'HMCRL', 'HMCRL', 'HMCRL_SUM', 'HMCRL_SUM'],
                                ['TMRD_PIC', 'TMRD', 'TMRD', 'TMRD', 'TMRD', 'TMRD_SUM', 'TMRD_SUM'],
                                ['TMZG_PIC', 'TMZG', 'TMZG', 'TMZG', 'TMZG', 'TRMZG_SUM', 'TRMZG_SUM'],
                                ['.', 'MNTHS', 'MNTHS', 'MNTHS', 'MNTHS', 'MNTHS_ALL_SUM', 'MNTHS_ALL_SUM'],
                                ['.', 'MNTHS', 'MNTHS', 'MNTHS', 'MNTHS', 'MNTHS_ALL_SUM', 'MNTHS_ALL_SUM']],
                                figsize=(10, 5)
                                )
    fig.patch.set_alpha(0.5)
    fig.suptitle(f'''Records overview''', size=12, fontweight='bold', color="white")
    # title.set_alpha(0.5)

    plt.subplots_adjust(wspace=.2, hspace=.2)

    # Moving the PIC Plots closer to the main record plot
    pic_keys = ['PUSH_PIC', 'KNBG_PIC', 'PLNK_PIC', 'HMCRL_PIC', 'TMRD_PIC', 'TMZG_PIC']
    for key in pic_keys:
        # Get the current position of the subplot
        pos = axs[key].get_position()
        # Adjust the width (decrease it to make space smaller on the right)
        axs[key].set_position([pos.x0, pos.y0, pos.width * 1.5, pos.height])

    

    # THE RECORDS PLOT
    axs['PUSH'].set_title(f" ", size=7)
    axs['PUSH'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['PUSH'].set_xlabel(' ', size=8)
    axs['PUSH'].yaxis.set_label_position("right")
    axs['PUSH'].set_ylabel(' ', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['PUSH'].tick_params(axis='x', labeltop=True, labelbottom=False, which='major', labelsize=6, rotation=0)
    axs['PUSH'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['PUSH'].set_ylim([0, 8])


    # Define the exercise-specific categories for Liegestütz
    categories = ['Liegestütz Sum record broken', 'Liegestütz Max record broken', 'Liegestütz Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Liegestütz category

    # Define horizontal offsets for each category
    offset = 0.1  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months


    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['PUSH'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['PUSH'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['PUSH'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['PUSH'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=0)

    # Add grid
    axs['PUSH'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['PUSH'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)

    custom_labels = ['Sum Records', 'Max Records', 'Average Records']
    axs['PUSH'].legend(labels=custom_labels, loc='upper right', fontsize=4.7, borderaxespad=0.3, 
                       handletextpad=0.01, columnspacing=0.8, ncol=3)
 





    # THE RECORDS PLOT KNIEBEUGE
    axs['KNBG'].set_title(f" ", size=7)
    axs['KNBG'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['KNBG'].set_xlabel(' ', size=8)
    axs['KNBG'].yaxis.set_label_position("right")
    axs['KNBG'].set_ylabel(' ', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['KNBG'].tick_params(axis='x', which='both', labelbottom=False)
    axs['KNBG'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['KNBG'].set_ylim([0, 8])

    # Define the exercise-specific categories for Kniebeugen
    categories = ['Kniebeugen Sum record broken', 'Kniebeugen Max record broken', 'Kniebeugen Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Kniebeugen category

    # Define horizontal offsets for each category
    offset = 0.1  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['KNBG'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['KNBG'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['KNBG'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['KNBG'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=0)

    # Add grid
    axs['KNBG'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['KNBG'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)



    # THE RECORDS PLOT PLANKE
    axs['PLNK'].set_title(f" ", size=7)
    axs['PLNK'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['PLNK'].set_xlabel(' ', size=8)
    axs['PLNK'].yaxis.set_label_position("right")
    axs['PLNK'].set_ylabel(' ', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['PLNK'].tick_params(axis='x', which='both', labelbottom=False)
    axs['PLNK'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['PLNK'].set_ylim([0, 8])

    # Define the exercise-specific categories for Planke
    categories = ['Planke Sum record broken', 'Planke Max record broken', 'Planke Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Planke category

    # Define horizontal offsets for each category
    offset = 0.1  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['PLNK'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['PLNK'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['PLNK'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['PLNK'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=0)

    # Add grid
    axs['PLNK'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['PLNK'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)




    # THE RECORDS PLOT Hammercurls
    axs['HMCRL'].set_title(f" ", size=7)
    axs['HMCRL'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['HMCRL'].set_xlabel(' ', size=8)
    axs['HMCRL'].yaxis.set_label_position("right")
    axs['HMCRL'].set_ylabel(' ', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['HMCRL'].tick_params(axis='x', which='both', labelbottom=False)
    axs['HMCRL'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['HMCRL'].set_ylim([0, 8])

    # Define the exercise-specific categories for Hammercurls
    categories = ['Weighted Hammer Curls Sum record broken', 'Weighted Hammer Curls Max record broken', 'Weighted Hammer Curls Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Hammercurls category

    # Define horizontal offsets for each category
    offset = 0.1  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['HMCRL'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['HMCRL'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['HMCRL'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['HMCRL'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=0)

    # Add grid
    axs['HMCRL'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['HMCRL'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)




    # THE RECORDS PLOT Turm Rudern
    axs['TMRD'].set_title(f" ", size=7)
    axs['TMRD'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['TMRD'].set_xlabel(' ', size=8)
    axs['TMRD'].yaxis.set_label_position("right")
    axs['TMRD'].set_ylabel(' ', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['TMRD'].tick_params(axis='x', which='both', labelbottom=False)
    axs['TMRD'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['TMRD'].set_ylim([0, 8])

    # Define the exercise-specific categories for Turm Rudern
    categories = ['Weighted Turm Rudern Sum record broken', 'Weighted Turm Rudern Max record broken', 'Weighted Turm Rudern Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Turm Rudern category

    # Define horizontal offsets for each category
    offset = 0.1  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['TMRD'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['TMRD'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['TMRD'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['TMRD'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=0)
    # Add grid
    axs['TMRD'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['TMRD'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)



    # THE RECORDS PLOT Turmzug
    axs['TMZG'].set_title(f" ", size=7)
    axs['TMZG'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['TMZG'].set_xlabel(' ', size=8)
    axs['TMZG'].yaxis.set_label_position("right")

    # # Set font size for major and minor ticks
    axs['TMZG'].tick_params(axis='x', which='both', labelbottom=False)
    axs['TMZG'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['TMZG'].set_ylim([0, 8])

    # Define the exercise-specific categories for Turmzug
    categories = ['Weighted Turm Zug Sum record broken', 'Weighted Turm Zug Max record broken', 'Weighted Turm Zug Average record broken']
    category_colors = ['grey', 'gold', 'green']  # Assign colors for each Turmzug category

    # Define horizontal offsets for each category
    offset = 0.1  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
        # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the dots for the current category
                axs['TMZG'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['TMZG'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)

    # Set major ticks for months
    axs['TMZG'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['TMZG'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=0)

    # Add grid
    axs['TMZG'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['TMZG'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)


    
    # THE RECORDS OVERVIEW MONTHLY PLOT
    axs['MNTHS'].set_title(f" ", size=7)
    axs['MNTHS'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['MNTHS'].set_xlabel(' ', size=8)
    axs['MNTHS'].yaxis.set_label_position("right")
    # axs['MNTHS'].set_ylabel('Monthly Records', size=8, labelpad=5)

    # # Set font size for major and minor ticks
    axs['MNTHS'].tick_params(axis='x', which='major', labelsize=6, rotation=0)
    axs['MNTHS'].tick_params(axis='x', which='minor', labelsize=6)
    axs['MNTHS'].tick_params(axis='y', labelright=False, labelleft=True, which='major', labelsize=6, grid_alpha=0.3)
    axs['MNTHS'].set_ylim([0, 22])

    # Define the exercise-specific categories for monthly plot
    categories = ['Total Sum records broken', 'Total Max records broken', 'Total Average records broken', "Training Day"]
    category_colors = ['grey', 'gold', 'green', "blue"]  # Assign colors for each monthly plot category

    # Define horizontal offsets for each category
    offset = 0.1  # How much space between each category within a month
    base_x_offset = np.arange(len(monthly_stats_data.index))  # X positions for months

    for i, month in enumerate(monthly_stats_data.index):
    # For each category (Sum, Max, Average for Liegestütz)
        for j, category in enumerate(categories):
            # Get the value for the category (how many dots to draw)
            value = monthly_stats_data.loc[month, category]
            
            # Draw dots (circles) vertically stacked for the current category
            y_positions = np.arange(1, value + 1)  # Vertically stack dots for the given count
            
            # Calculate x_positions by adding a unique offset for each category per month
            x_positions = np.full(len(y_positions), base_x_offset[i] + j * offset)  # Horizontally offset categories

            if value > 0:
                # Plot the regular dots for the current category
                axs['MNTHS'].scatter(x_positions, y_positions, color=category_colors[j],
                                    label=category if i == 0 else "", s=10)
                
                # Plot the larger empty dot ("o" symbol) on top of the stack
                # Position the empty dot at one unit above the highest dot
                axs['MNTHS'].scatter(base_x_offset[i] + j * offset, value + 2.5, 
                                    facecolors='none', edgecolors=category_colors[j],
                                    label="", s=70, marker='o')  # Larger size for the empty "o" symbol
                
                # Write the number of dots (value) inside the larger empty dot
                axs['MNTHS'].text(base_x_offset[i] + j * offset, value + 2.5, str(value), 
                                ha='center', va='center', fontsize=5, color="black") #color=category_colors[j]

            else:
                # Plot a marker (e.g., a small line) to indicate zero records
                axs['MNTHS'].scatter(base_x_offset[i] + j * offset, 1, facecolors='none', color=category_colors[j],
                                    marker='o', s=15)


    # Set major ticks for months
    axs['MNTHS'].set_xticks(base_x_offset + 0.1)  # Center the labels between the 3 bars
    axs['MNTHS'].set_xticklabels(monthly_stats_data.index.astype(str), rotation=0)

    # Add grid
    axs['MNTHS'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['MNTHS'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)
    



    #########PLOTS FOR EXERSICE ALL SUM RECS###################
    
    #sum_recs_of_all_exers = [sum_rec for monthly_stats_data[categories].sum()]

    max_recsum_of_all_exersices = find_max_recsum_of_all_exersices(monthly_stats_data)

    # def find_max_recsum_of_all_exersices():

    #     all_exersices_list = ['Liegestütz Average record broken', 'Liegestütz Max record broken', 'Liegestütz Sum record broken',
    #                       'Kniebeugen Average record broken', 'Kniebeugen Max record broken', 'Kniebeugen Sum record broken',
    #                       'Planke Average record broken', 'Planke Max record broken', 'Planke Sum record broken',
    #                       'Weighted Hammer Curls Average record broken', 'Weighted Hammer Curls Max record broken', 'Weighted Hammer Curls Sum record broken',
    #                       'Weighted Turm Rudern Average record broken', 'Weighted Turm Rudern Max record broken', 'Weighted Turm Rudern Sum record broken',
    #                       'Weighted Turm Zug Average record broken', 'Weighted Turm Zug Max record broken', 'Weighted Turm Zug Sum record broken'
    #                       ]
        
    #     recsum_of_all_exers = []
    #     for exersice in all_exersices_list:
    #         exersice_sum = monthly_stats_data[exersice].sum()
    #         recsum_of_all_exers.append(exersice_sum)
    #         max_recsum = recsum_of_all_exers.max()
    #     return max_recsum


    

    # THE RECORDS SUM EXERSICE PUSH UP
    axs['PUSH_SUM'].set_title(f" ", size=7)
    axs['PUSH_SUM'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['PUSH_SUM'].set_xlabel(' ', size=8)
    axs['PUSH_SUM'].yaxis.set_label_position("right")

    # # Set font size for major and minor ticks
    axs['PUSH_SUM'].tick_params(axis='x', which='both', labelbottom=False)
    axs['PUSH_SUM'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['PUSH_SUM'].set_ylim([0, 6])
    axs['PUSH_SUM'].set_xlim([0, max_recsum_of_all_exersices*2])

    # Define only the specified categories
    categories = ['Liegestütz Average record broken', 'Liegestütz Max record broken', 'Liegestütz Sum record broken']
    category_colors = ['grey', 'gold', 'green']  # Define colors for the three categories

    # Calculate the total sum across the three months for each specified category
    totals = monthly_stats_data[categories].sum()
    y_positions = [1.5, 3, 4.5]  # Custom positions for the bars
    bar_height = 1.1  # Adjust this value to change the bar thickness

    # Plot a single horizontal bar for each specified category with the total sums
    # y_positions = np.arange(len(categories))
    axs['PUSH_SUM'].barh(y=y_positions, width=totals, height=bar_height, color=category_colors, tick_label=['Average', 'Max', 'Sum'])

    # Add grid
    axs['PUSH_SUM'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['PUSH_SUM'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)




    # THE RECORDS SUM EXERSICE KNIEBEUGEN
    axs['KNBG_SUM'].set_title(f" ", size=7)
    axs['KNBG_SUM'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['KNBG_SUM'].set_xlabel(' ', size=8)
    axs['KNBG_SUM'].yaxis.set_label_position("right")

    # # Set font size for major and minor ticks
    axs['KNBG_SUM'].tick_params(axis='x', which='both', labelbottom=False)
    axs['KNBG_SUM'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['KNBG_SUM'].set_ylim([0, 6])
    axs['KNBG_SUM'].set_xlim([0, max_recsum_of_all_exersices*2])

    # Define only the specified categories
    categories = ['Kniebeugen Average record broken', 'Kniebeugen Max record broken', 'Kniebeugen Sum record broken']
    category_colors = ['grey', 'gold', 'green']  # Define colors for the three categories

    # Calculate the total sum across the three months for each specified category
    totals = monthly_stats_data[categories].sum()
    y_positions = [1.5, 3, 4.5]  # Custom positions for the bars
    bar_height = 1.1  # Adjust this value to change the bar thickness

    # Plot a single horizontal bar for each specified category with the total sums
    # y_positions = np.arange(len(categories))
    axs['KNBG_SUM'].barh(y=y_positions, width=totals, height=bar_height, color=category_colors, tick_label=['Average', 'Max', 'Sum'])

    # Add grid
    axs['KNBG_SUM'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['KNBG_SUM'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)




    # THE RECORDS SUM EXERSICE PLANKE
    axs['PLNK_SUM'].set_title(f" ", size=7)
    axs['PLNK_SUM'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['PLNK_SUM'].set_xlabel(' ', size=8)
    axs['PLNK_SUM'].yaxis.set_label_position("right")

    # # Set font size for major and minor ticks
    axs['PLNK_SUM'].tick_params(axis='x', which='both', labelbottom=False)
    axs['PLNK_SUM'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['PLNK_SUM'].set_ylim([0, 6])
    axs['PLNK_SUM'].set_xlim([0, max_recsum_of_all_exersices*2])


    # Define only the specified categories
    categories = ['Planke Average record broken', 'Planke Max record broken', 'Planke Sum record broken']
    category_colors = ['grey', 'gold', 'green']  # Define colors for the three categories

    # Calculate the total sum across the three months for each specified category
    totals = monthly_stats_data[categories].sum()
    y_positions = [1.5, 3, 4.5]  # Custom positions for the bars
    bar_height = 1.1  # Adjust this value to change the bar thickness

    # Plot a single horizontal bar for each specified category with the total sums
    # y_positions = np.arange(len(categories))
    axs['PLNK_SUM'].barh(y=y_positions, width=totals, height=bar_height, color=category_colors, tick_label=['Average', 'Max', 'Sum'])

    # Add grid
    axs['PLNK_SUM'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['PLNK_SUM'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)



    # THE RECORDS SUM EXERSICE HAMMERCURLS
    axs['HMCRL_SUM'].set_title(f" ", size=7)
    axs['HMCRL_SUM'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['HMCRL_SUM'].set_xlabel(' ', size=8)
    axs['HMCRL_SUM'].yaxis.set_label_position("right")

    # # Set font size for major and minor ticks
    axs['HMCRL_SUM'].tick_params(axis='x', which='both', labelbottom=False)
    axs['HMCRL_SUM'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['HMCRL_SUM'].set_ylim([0, 6])
    axs['HMCRL_SUM'].set_xlim([0, max_recsum_of_all_exersices*2])


    # Define only the specified categories
    categories = ['Weighted Hammer Curls Average record broken', 'Weighted Hammer Curls Max record broken', 'Weighted Hammer Curls Sum record broken']
    category_colors = ['grey', 'gold', 'green']  # Define colors for the three categories

    # Calculate the total sum across the three months for each specified category
    totals = monthly_stats_data[categories].sum()

    y_positions = [1.5, 3, 4.5]  # Custom positions for the bars
    bar_height = 1.1  # Adjust this value to change the bar thickness

    # Plot a single horizontal bar for each specified category with the total sums
    # y_positions = np.arange(len(categories))
    axs['HMCRL_SUM'].barh(y=y_positions, width=totals, height=bar_height, color=category_colors, tick_label=['Average', 'Max', 'Sum'])

    # Add grid
    axs['HMCRL_SUM'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['HMCRL_SUM'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)





    # THE RECORDS SUM EXERSICE TRURMRUDERN
    axs['TMRD_SUM'].set_title(f" ", size=7)
    axs['TMRD_SUM'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['TMRD_SUM'].set_xlabel(' ', size=8)
    axs['TMRD_SUM'].yaxis.set_label_position("right")

    # # Set font size for major and minor ticks
    axs['TMRD_SUM'].tick_params(axis='x', which='both', labelbottom=False)
    axs['TMRD_SUM'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['TMRD_SUM'].set_ylim([0, 6])
    axs['TMRD_SUM'].set_xlim([0, max_recsum_of_all_exersices*2])

    # Define only the specified categories
    categories = ['Weighted Turm Rudern Average record broken', 'Weighted Turm Rudern Max record broken', 'Weighted Turm Rudern Sum record broken']
    category_colors = ['grey', 'gold', 'green']  # Define colors for the three categories

    # Calculate the total sum across the three months for each specified category
    totals = monthly_stats_data[categories].sum()

    y_positions = [1.5, 3, 4.5]  # Custom positions for the bars
    bar_height = 1.1  # Adjust this value to change the bar thickness

    # Plot a single horizontal bar for each specified category with the total sums
    # y_positions = np.arange(len(categories))
    axs['TMRD_SUM'].barh(y=y_positions, width=totals, height=bar_height, color=category_colors, tick_label=['Average', 'Max', 'Sum'])

    # Add grid
    axs['TMRD_SUM'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['TMRD_SUM'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)




    # THE RECORDS SUM EXERSICE TRURMRUDERN
    axs['TRMZG_SUM'].set_title(f" ", size=7)
    axs['TRMZG_SUM'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['TRMZG_SUM'].set_xlabel(' ', size=8)
    axs['TRMZG_SUM'].yaxis.set_label_position("right")

    # # Set font size for major and minor ticks
    axs['TRMZG_SUM'].tick_params(axis='x', which='both', labelbottom=False)
    axs['TRMZG_SUM'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['TRMZG_SUM'].set_ylim([0, 6])
    axs['TRMZG_SUM'].set_xlim([0, max_recsum_of_all_exersices*2])

    # Define only the specified categories
    categories = ['Weighted Turm Zug Average record broken', 'Weighted Turm Zug Max record broken', 'Weighted Turm Zug Sum record broken']
    category_colors = ['grey', 'gold', 'green']  # Define colors for the three categories

    # Calculate the total sum across the three months for each specified category
    totals = monthly_stats_data[categories].sum()

    # Plot a single horizontal bar for each specified category with the total sums
    y_positions = [1.5, 3, 4.5]  # Custom positions for the bars
    bar_height = 1.1  # Adjust this value to change the bar thickness

    # Plot a single horizontal bar for each specified category with the total sums
    # y_positions = np.arange(len(categories))
    axs['TRMZG_SUM'].barh(y=y_positions, width=totals, height=bar_height, color=category_colors, tick_label=['Average', 'Max', 'Sum'])

    # Add grid
    axs['TRMZG_SUM'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['TRMZG_SUM'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)




    # THE RECORDS SUM EXERSICE TRURMRUDERN
    axs['MNTHS_ALL_SUM'].set_title(f" ", size=7)
    axs['MNTHS_ALL_SUM'].set_facecolor((1, 1, 1, 0.5))  # Set the axes background to white with 50% transparency

    axs['MNTHS_ALL_SUM'].set_xlabel(' ', size=8)
    axs['MNTHS_ALL_SUM'].yaxis.set_label_position("right")

    # # Set font size for major and minor ticks
    axs['MNTHS_ALL_SUM'].tick_params(axis='x', which='both', labelbottom=False)
    axs['MNTHS_ALL_SUM'].tick_params(axis='y', labelright=False, labelleft=False, which='major', labelsize=6, grid_alpha=0.3)
    axs['MNTHS_ALL_SUM'].set_ylim([0, 7.5])
    axs['MNTHS_ALL_SUM'].set_xlim([0, 50])


    # Define only the specified categories
    categories = ['Total Sum records broken', 'Total Max records broken', 'Total Average records broken', "Training Day"]
    category_colors = ['grey', 'gold', 'green', "blue"]  # Define colors for the three categories

    # Calculate the total sum across the three months for each specified category
    totals = monthly_stats_data[categories].sum()

    # Plot a single horizontal bar for each specified category with the total sums
    y_positions = [1.5, 3, 4.5, 6]  # Custom positions for the bars
    bar_height = 1.2  # Adjust this value to change the bar thickness

    # Plot a single horizontal bar for each specified category with the total sums
    # y_positions = np.arange(len(categories))
    axs['MNTHS_ALL_SUM'].barh(y=y_positions, width=totals, height=bar_height, color=category_colors, tick_label=['Average', 'Max', 'Sum', "Days"])

    # Add grid
    axs['MNTHS_ALL_SUM'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    axs['MNTHS_ALL_SUM'].grid(visible=True, which='major', axis='x', linestyle='-', linewidth=0.3, alpha=0.9)






    # PIC PUSH UPS
    # Add grid
    axs['PUSH_PIC'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    # Clear the current plot for PUSH UPS
    axs['PUSH_PIC'].cla()
    # Display the image in the plot
    axs['PUSH_PIC'].imshow(push_pic)
    # Remove axis labels and ticks (optional, if you want the image alone)
    axs['PUSH_PIC'].axis('off')  # This removes the axis


    # PIC PUSH UPS
    # Add grid
    axs['KNBG_PIC'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    # Clear the current plot for 'TMZG'
    axs['KNBG_PIC'].cla()
    # Display the image in the plot
    axs['KNBG_PIC'].imshow(knbg_pic)
    # Remove axis labels and ticks (optional, if you want the image alone)
    axs['KNBG_PIC'].axis('off')  # This removes the axis


    # PIC PLANKE  
    # Add grid
    axs['PLNK_PIC'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    # Clear the current plot for 'TMZG'
    axs['PLNK_PIC'].cla()
    # Display the image in the plot
    axs['PLNK_PIC'].imshow(plnk_pic)
    # Remove axis labels and ticks (optional, if you want the image alone)
    axs['PLNK_PIC'].axis('off')  # This removes the axis


    # PIC HAMMERCURL
    # Add grid
    axs['HMCRL_PIC'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    # Clear the current plot for 'TMZG'
    axs['HMCRL_PIC'].cla()
    # Display the image in the plot
    axs['HMCRL_PIC'].imshow(hmcrl_pic)
    # Remove axis labels and ticks (optional, if you want the image alone)
    axs['HMCRL_PIC'].axis('off')  # This removes the axis


    # PIC TURM RUDERN 
    # Add grid
    axs['TMRD_PIC'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    # Clear the current plot for 'TMZG'
    axs['TMRD_PIC'].cla()
    # Display the image in the plot
    axs['TMRD_PIC'].imshow(tmrd_pic)
    # Remove axis labels and ticks 
    axs['TMRD_PIC'].axis('off')  


    # PIC TURM ZUG 
    # Add grid
    axs['TMZG_PIC'].grid(visible=True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.3)
    # Clear the current plot for 'TMZG'
    axs['TMZG_PIC'].cla()
    # Display the image in the plot
    axs['TMZG_PIC'].imshow(tmzg_pic)
    # Remove axis labels and ticks 
    axs['TMZG_PIC'].axis('off') 

    return fig



