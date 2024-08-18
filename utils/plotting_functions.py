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




def pushup_plot(data):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['LGSTZ', 'LGSTZ', 'LGSTZ','LGSTZ_REC'],
                                ],
                                figsize=(11, 3))

    plt.subplots_adjust(wspace=.2)
    plt.subplots_adjust(hspace=.6)

    # fig.suptitle(f'''Training''', size=18)

    axs['LGSTZ'].set_title(f"Progress Liegestütz", size=14)
    axs['LGSTZ'].set_xlabel(' ', size=14)
    axs['LGSTZ'].set_ylabel('Value', size=12)
    axs['LGSTZ'].set_xlim([pd.to_datetime("2024.08.10"), pd.to_datetime("2024.08.20")]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['LGSTZ'].tick_params(axis='x', labelsize=7, rotation=45)  
    axs['LGSTZ'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

    axs['LGSTZ'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['LGSTZ'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
    axs['LGSTZ'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['LGSTZ'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['LGSTZ'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
    axs['LGSTZ'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.2
    dates = data.index

    axs['LGSTZ'].bar(dates - pd.Timedelta(hours=4), data["Liegestütz set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['LGSTZ'].bar(dates, data["Liegestütz set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['LGSTZ'].bar(dates + pd.Timedelta(hours=4), data["Liegestütz set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")

    return fig


def plk_plot(data):

    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['PLK', 'PLK', 'PLK', 'PLK_REC'],
                                ],
                                figsize=(11, 3))
    plt.subplots_adjust(wspace=.2)
    plt.subplots_adjust(hspace=.6)

    # fig.suptitle(f'''Training''', size=18)

    axs['PLK'].set_title(f"Progress Planke", size=14)
    axs['PLK'].set_xlabel(' ', size=14)
    axs['PLK'].set_ylabel('Value', size=12)
    axs['PLK'].set_xlim([pd.to_datetime("2024.08.10"), pd.to_datetime("2024.08.20")]), 
    # axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['PLK'].tick_params(axis='x', labelsize=7, rotation=45)  
    axs['PLK'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

    axs['PLK'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['PLK'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
    axs['PLK'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['PLK'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['PLK'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
    axs['PLK'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    # Plotting the three sets next to each other
    bar_width = 0.2
    dates = data.index

    axs['PLK'].bar(dates - pd.Timedelta(hours=4), data["Planke set 1"], alpha=1, width=bar_width, color="limegreen", label="Set 1")
    axs['PLK'].bar(dates, data["Planke set 2"], alpha=1, width=bar_width, color="dodgerblue", label="Set 2")
    axs['PLK'].bar(dates + pd.Timedelta(hours=4), data["Planke set 3"], alpha=1, color="darkviolet", width=bar_width, label="Set 3")

    return fig
































def plot_scatter_color_categories(df, name, ax, markersize=8):
    """Plots scatter points with color categories based on value ranges."""
    for i, (x, y) in enumerate(zip(df.index, df[name])):
        # if 1 <= y <= 3:
        #     color_dot = "green"
        # elif 3.1 <= y <= 4:
        #     color_dot= "#FFCC00" # "yellow"
        # elif 4.1 <= y <= 6:
        #     color_dot = "orange"
        # elif 6.1 <= y <= 7:
        #     color_dot = "#E71D24" # rose
        # elif 7.1 <= y <= 10:
        #     color_dot = "#B6010E" # darkred
        # else:  
        #     continue 

        ######## ADJUST 4 FOR YELLOW - ADJUST COLORS

        if 0 <= y <= 1:
            color_dot = "#01FFAA"     
        elif 1.1 <= y <= 2:
            color_dot = "#007C03"
        elif 2.1 <= y <= 3:
            color_dot = "#19AF01"
        elif 3.1 <= y <= 4:
            color_dot = "#23FE01"
        elif 4.1 <= y <= 5:
            color_dot = "#E4FE00"
        elif 5.1 <= y <= 6:
            color_dot = "#FFB703"
        elif 6.1 <= y <= 7:
            color_dot = "#FE8A00"
        elif 7.1 <= y <= 8:
            color_dot = "#FF2E01"
        elif 8.1 <= y <= 9:
            color_dot = "#CC4637"
        elif 9.1 <= y <= 10:
            color_dot = "#A3231A"
        elif 10.1 <= y <= 11:
            color_dot = "#670001"
        else:
            color_dot = "grey"  

        # Assign markers based on the name
        if name == "Trock mor dig":
            marker = '*'  
            markersize = 14
        elif name == "Trockenheit mittelwert":
            markersize = 10
            marker = '.'  
        elif name == "Trock ab dig":
            markersize = 7
            marker = 'o' 

        ax.plot(x, y, marker=marker, color=color_dot, markersize=markersize, linestyle='none')



def plot_pregabalin(ax, df, name, date_start, date_end):
    sns.lineplot(data=df[name]*0.02, label= f"{name.title()}", linestyle='--', linewidth=1, ax=ax) # color='black'
    ax.scatter(df.index, df[name]*0.02, color='grey', s=15)
    for date, value in df[name].loc[date_start:date_end].items():
        if not pd.isna(value):   
            ax.text(date, (value*0.02)+0.15, f"{round(value)}", va='bottom', ha='center', fontsize=9)


def plot_schmerz(ax, df, name, date_start, date_end):
    # Bar plot for Schmerz (using original date index)
    colors = ['blue' if y >= 9 and y <= 10 else 'blue' for y in df[name]]  # Colors for day/night
    ax.bar(df.loc[date_start:date_end].index, df.loc[date_start:date_end][name]*0.25, color=colors, width=0.6, label= f"{name.title()}", zorder=5)

    # Scatter plot and text labels on top of the bars
    scatter_colors = []
    for value in df[name].loc[date_start:date_end]:
        if not pd.isna(value):
            if 0 <= value <= 1:
                scatter_colors.append('green')
            elif 2 <= value <= 3:
                scatter_colors.append('yellow')
            elif 4 <= value <= 5:
                scatter_colors.append('orange')
            elif 6 <= value <= 7:
                scatter_colors.append('red')
            else:  # 8 <= value <= 10
                scatter_colors.append('darkred')
        else:
            scatter_colors.append('grey')

    ax.scatter(df.loc[date_start:date_end].index, df.loc[date_start:date_end][name]*0.25, color=scatter_colors, label='Quantity', s=25, zorder=10)
    for date, value in df[name].loc[date_start:date_end].items():
        if not pd.isna(value):
            ax.text(date, value*0.25 + 0.15, f"{round(value)}", va='bottom', ha='center', fontsize=9)


def plot_trockenheit(ax, df, name, date_start, date_end):
    # Assign specific colors for the lineplots and create lineplots
    if name == "Trock ab dig":
        color_line = "blue" 
    elif name == "Trock mor dig":
        color_line = "green"
    elif name == "Trockenheit mittelwert":
        color_line = "grey"
    sns.lineplot(data=df[name], label= f"{name.title()}", linestyle='-', linewidth=1.5, color=color_line, ax=ax)

    




def plot_changes(ax, df, date_start, date_end):
    ax.axhspan(9.25, 11.25, facecolor='lightblue', alpha=0.5)  # Light blue band
    ax.axhspan(11.25, 13.25, facecolor='blue', alpha=0.5)     # Blue band

    for date in pd.date_range(date_start, date_end):
        if (df["Umschwenker"] == "Verbesserung Tag").loc[date].any():
            ax.annotate("D +", xy=(date, 9.5), xytext=(date, 9.4 + 1), size=8, 
                        arrowprops=dict(arrowstyle="-|>,head_width=1,head_length=1",
                                        facecolor="lightblue", edgecolor="green", linewidth=3),
                        ha='center')

        if (df["Umschwenker"] == "Verbesserung Nacht").loc[date].any():
            ax.annotate("N +", xy=(date, 11.5), xytext=(date, 11.4 + 1), size=8, 
                        arrowprops=dict(arrowstyle="-|>,head_width=1,head_length=1",
                                        facecolor="blue", edgecolor="green", linewidth=3),
                        ha='center')
        
        if (df["Umschwenker"] == "Verschlechterung Tag").loc[date].any():
            ax.annotate("D -", xy=(date, 9.7 + 1), xytext=(date, 9.5), size=8, 
            arrowprops=dict(arrowstyle="-|>,head_width=1,head_length=1",
                            facecolor="lightblue", edgecolor="red", linewidth=3),
                            ha='center')

        if (df["Umschwenker"] == "Verschlechterung Nacht").loc[date].any():
            ax.annotate("N -", xy=(date, 11.7 + 1), xytext=(date, 11.5), size=8, 
            arrowprops=dict(arrowstyle="-|>,head_width=1,head_length=1",
                            facecolor="blue", edgecolor="red", linewidth=3),
                            ha='center')



def plot_if_eaten(ax, df, ingredient_columns, date_start, date_end):  

    ingredient_map = lade_ingridient_map("utils/map_ingredients_plot.json")

    # Add the horizontal line
    y_min, y_max = ax.get_ylim()
    y_55_percent = y_min + (y_max - y_min) * 0.55
    ax.axhline(y=y_55_percent, color='gray', linestyle='--', linewidth=1)

    for date in pd.date_range(date_start, date_end):
        y_offset = y_min  # Reset y_offset for each date iteration
        y_offset_special = y_55_percent  # Separate y_offset for specified ingredients

        for ingredient in ingredient_columns:
            if (df[ingredient] >= 1).loc[date].any():
                abbr = ingredient_map.get(ingredient, {}).get("abbreviation", ingredient)  # Get abbreviation or default to full name
                color = ingredient_map.get(ingredient, {}).get("color", "lightblue")  # Get color or default to lightblue
                boxstyle = ingredient_map.get(ingredient, {}).get("boxstyle", "round")  # Get boxstyle or default to "round"  

                if ingredient in ["Fisch dig", "Brot ind Teig, Gluten dig", "Milchprodukte dig", "Eier dig", "Fleisch dig", "Zucker dig"]:
                    current_y_offset = y_offset_special  # Use special y_offset for these ingredients
                    y_offset_special += 0.7  # Increment special y_offset for next ingredient
                else:
                    current_y_offset = y_offset  # Use normal y_offset for other ingredients

                ax.annotate(abbr, xy=(date, current_y_offset), xytext=(date, current_y_offset + 1), size=7, 
                            bbox=dict(boxstyle=boxstyle, fc=color, ec="black"),
                            arrowprops=None, ha='center')

                if ingredient in ["Fisch dig", "Brot ind Teig, Gluten dig", "Milchprodukte dig", "Eier dig", "Fleisch dig", "Zucker dig"]:
                    value = int(df[ingredient].loc[date])  # Get the integer value
                    x_values = [date + pd.DateOffset(hours=-6 + (i * 5)) for i in range(value)]  # Horizontal spacing
                    y_values = [current_y_offset + 1.42] * value  # Adjust y-value according to special y_offset
                    ax.scatter(x_values, y_values, marker='o', s=10, color=color)

                if ingredient not in ["Fisch dig", "Brot ind Teig, Gluten dig", "Milchprodukte dig", "Eier dig", "Fleisch dig", "Zucker dig"]:
                    y_offset += 0.7  # Increment normal y_offset for next ingredient


def create_a_plot(df, selected_names, date_start, date_end, number_of_days, show_changes=True):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['1', '1', '1'],
                                ['1', '1', '1'],
                                ['2', '2', '2'],
                                ['2', '2', '2'],
                                ],
                                figsize=(20, 9))

    plt.subplots_adjust(wspace=.2)
    plt.subplots_adjust(hspace=.6)

    fig.suptitle(f'''RHELIZER''', size=15)

    axs['1'].set_title(f"Measurements over {number_of_days} days", size=13)
    axs['1'].set_xlabel(' ', size=14)
    axs['1'].set_ylabel('Value', size=12)
    axs['1'].set_xlim([pd.to_datetime(date_start), pd.to_datetime(date_end)]), 
    axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['1'].tick_params(axis='x', labelsize=7, rotation=45)  
    axs['1'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

    axs['1'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['1'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
    axs['1'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['1'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['1'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
    axs['1'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)


    for name in selected_names:
        # moving_average_plot(ax=axs["1"], df=df, name=name, date_start=date_start, date_end=date_end, window=4)

        # # low_threshold = df[name].quantile(0.4)
        # # high_threshold = df[name].quantile(0.9)
        # std_dev = df[name].std()
        # mean = df[name].mean()
        # median = df[name].quantile(0.5)
        # low_threshold = mean - 0.5*std_dev
        # high_threshold = mean + 0.4*std_dev

        # axs['1'].axhline(y=low_threshold, color='g', linestyle='dashed', linewidth=1, label='low_threshold')
        # axs['1'].axhline(y=high_threshold, color='r', linestyle='dashed', linewidth=1, label='high_threshold')
        # # axs['1'].axhline(y=mean, color='grey', linestyle='dashed', linewidth=1, label='mean')
        # # axs['1'].axhline(y=median, color='grey', linestyle='dashed', linewidth=1, label='median')


        if name == "Pregabalin":
            plot_pregabalin(ax=axs["1"], df=df, name=name, date_start=date_start, date_end=date_end)
  
        elif name in ["Trock mor dig", "Trock ab dig", "Trockenheit mittelwert"]:
            # create a scatterplot with categories and trockenheit plot
            plot_scatter_color_categories(df=df, name=name, ax=axs['1']) 
            plot_trockenheit(ax=axs["1"], df=df, name=name, date_start=date_start, date_end=date_end)
        
        elif name == "Schmerz dig":
            plot_schmerz(ax=axs["1"], df=df, name=name, date_start=date_start, date_end=date_end)
    
        else:
            # create different lineplots
            sns.lineplot(data=df[name], label= f"{name.title()}", linestyle='--', linewidth=1, ax=axs['1'])
    if show_changes == True:
        plot_changes(axs['1'], df=df, date_start=pd.to_datetime(date_start), date_end=pd.to_datetime(date_end))


    ##########################################################
    # strating or events function(())
    # HOM Start 25.04
    # IF Start 18.04
    # board with toggles for parameter and co


    ###############################################

    axs['2'].set_title(f"Ingredients over {number_of_days} days", size=13) 
    axs['2'].set_xlabel('', size=14)
    axs['2'].set_ylabel('Ingredient', size=12)
    axs['2'].set_xlim([pd.to_datetime(date_start), pd.to_datetime(date_end)]), 
    axs['2'].set_ylim([0, 10])

    # Set font size for major and minor ticks
    axs['2'].tick_params(axis='x', labelsize=7, rotation=45)  
    axs['2'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

    axs['2'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['2'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
    axs['2'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['2'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['2'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
    axs['2'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)

    plot_if_eaten(axs['2'], df, ingredient_columns=["Reis", "Weißer Reis", "Roter Reis", "Vollkorn Reis", "Konjac Nudeln",
                                                    "Quinoa", "Buchweizen", "Amaranth", "Hirse", 
                                                    "Kartoffeln", "Haferflocken", 
                                                    "Salat", "Grünkohl", "Kohl", "Gemüse", "Oliven", "Spargel", "Suppe", "Süßkartoffeln",
                                                    "Veganes Protein", "Bohnen", "Erbsen", "Kichererbsen", "Kichererbsennudeln", "Erbsennudeln", "Nüsse",
                                                    "Brot ind Teig, Gluten dig", "Milchprodukte dig",
                                                    "Fisch dig", "Fleisch dig", "Eier dig", "Zucker dig"], 
                                                    date_start=pd.to_datetime(date_start), date_end=pd.to_datetime(date_end)) 
    
    axs['1'].legend(loc='upper right', 
                    frameon=True,
                    facecolor='lightgrey',
                    edgecolor='white', 
                    fontsize=8.5) 

    return fig


############################################################################################################################
#SECOND PLOT - Cycle Plot
############################################################################################################################

def get_colors_for_ma_plot(y):
    if 0 <= y <= 1:
        return "#01FFAA"
    elif 1.01 <= y <= 4.4:
        return "#19AF01"
    elif 4.41 <= y <= 6:
        return "#FFB703"
    elif 6.01 <= y <= 10:
        return "#FF2E01"
    else:
        return "grey"

    # if 0 <= y <= 1:
    #     return "#01FFAA"
    # elif 1.01 <= y <= 2:
    #     return "#007C03"
    # elif 2.01 <= y <= 3:
    #     return "#19AF01"
    # elif 3.01 <= y <= 4:
    #     return "#23FE01"
    # elif 4.01 <= y <= 5:
    #     return "#E4FE00"
    # elif 5.01 <= y <= 6:
    #     return "#FFB703"
    # elif 6.01 <= y <= 7:
    #     return "#FE8A00"
    # elif 7.01 <= y <= 8:
    #     return "#FF2E01"
    # elif 8.01 <= y <= 9:
    #     return "#CC4637"
    # elif 9.01 <= y <= 10:
    #     return "#A3231A"
    # elif 10.01 <= y <= 11:
    #     return "#670001"
    # else:
    #     return "grey"




def moving_average_plot(ax, df, name, date_start, date_end, window=3, color_gradient=False):
    df[f'{name} moving_avg {window}'] = df[name].rolling(window=window).mean()

    if color_gradient == False:
        sns.lineplot(data=df[f'{name} moving_avg {window}'], label= f"{window}D MA {name.title()}", linestyle='-', linewidth=2, ax=ax)
        sns.lineplot(data=df[name], label= f"{name.title()}", linestyle='--', linewidth=0.5, ax=ax)  
        
        for i, (x, y) in enumerate(zip(df.index, df[f'{name} moving_avg {window}'])):

            if 0 <= y <= 1:
                color_dot = "#01FFAA "     
            elif 1.01 <= y <= 2:
                color_dot = "#007C03"
            elif 2.01 <= y <= 3:
                color_dot = "#19AF01"
            elif 3.01 <= y <= 4:
                color_dot = "#23FE01"
            elif 4.01 <= y <= 5:
                color_dot = "#E4FE00"
            elif 5.01 <= y <= 6:
                color_dot = "#FFB703"
            elif 6.01 <= y <= 7:
                color_dot = "#FE8A00"
            elif 7.01 <= y <= 8:
                color_dot = "#FF2E01"
            elif 8.01 <= y <= 9:
                color_dot = "#CC4637"
            elif 9.01 <= y <= 10:
                color_dot = "#A3231A"
            elif 10.01 <= y <= 11:
                color_dot = "#670001"
            else:
                color_dot = "grey"  

            ax.scatter(x, y, color=color_dot, s=30)
    
    else:
    
        sns.lineplot(data=df[name], label=f"{name.title()}", linestyle='--', linewidth=0.5, ax=ax) 
        df['numeric_index'] = pd.to_numeric(df.index)

        # Minimum number of segments per day (adjust as needed)
        min_segments_per_day = 10

        for i in range(len(df) - 1):
            x0, x1 = df['numeric_index'].iloc[i], df['numeric_index'].iloc[i + 1]
            y0, y1 = df[f'{name} moving_avg {window}'].iloc[i], df[f'{name} moving_avg {window}'].iloc[i + 1]

            if pd.isna(y0) or pd.isna(y1):
                continue

            days_diff = (pd.to_datetime(x1) - pd.to_datetime(x0)).days 
            num_segments = max(1, int(np.ceil(days_diff * min_segments_per_day))) 

            x_values_numeric = np.linspace(x0, x1, num_segments + 1)
            y_values = np.linspace(y0, y1, num_segments + 1)
            x_values = pd.to_datetime(x_values_numeric)

            for j in range(num_segments):
                # Farbzuweisung für die Fläche unter dem Graphen
                color = get_colors_for_ma_plot(y_values[j])
                ax.fill_between(x_values[j:j+2], y_values[j:j+2], 0, color=color, alpha=0.6)
                # Plotten der Linie des gleitenden Durchschnitts
                ax.plot(x_values[j:j+2], y_values[j:j+2], color=color, linewidth=1.5, linestyle='-') 




def create_comparable_plot(df, selected_names, date_start, date_end, number_of_days, window=3, show_changes=False, color_gradient=False):
    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['1', '1', '1'],
                                ['1', '1', '1'],
                                ['2', '2', '2'],
                                ['2', '2', '2'],
                                ],
                                figsize=(20, 9))

    plt.subplots_adjust(wspace=.2)
    plt.subplots_adjust(hspace=.6)

    fig.suptitle(f'''COMP''', size=20)

    axs['1'].set_title(f"Measurements over {number_of_days} days", size=13)
    axs['1'].set_xlabel(' ', size=14)
    axs['1'].set_ylabel('Value', size=12)
    axs['1'].set_xlim([pd.to_datetime(date_start), pd.to_datetime(date_end)]), 
    axs['1'].set_ylim([0, 14])

    # Set font size for major and minor ticks
    axs['1'].tick_params(axis='x', labelsize=7, rotation=45)  
    axs['1'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

    axs['1'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['1'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
    axs['1'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['1'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['1'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
    axs['1'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)


    for name in selected_names:
        if name == "Pregabalin":
            plot_pregabalin(ax=axs["1"], df=df, name=name, date_start=date_start, date_end=date_end)
  
        elif name in ["Trock mor dig", "Trock ab dig", "Trockenheit mittelwert"]:
            # create a scatterplot with categories and trockenheit plot
            plot_scatter_color_categories(df=df, name=name, ax=axs['1']) 
            plot_trockenheit(ax=axs["1"], df=df, name=name, date_start=date_start, date_end=date_end)
        
        elif name == "Schmerz dig":
            plot_schmerz(ax=axs["1"], df=df, name=name, date_start=date_start, date_end=date_end)
    
        else:
            # create different lineplots
            sns.lineplot(data=df[name], label= f"{name.title()}", linestyle='--', linewidth=1, ax=axs['1'])
    
    if show_changes == True:
        plot_changes(axs['1'], df=df, date_start=pd.to_datetime(date_start), date_end=pd.to_datetime(date_end))

    axs['1'].legend(loc='upper right', 
                        frameon=True,
                        facecolor='lightgrey',
                        edgecolor='white', 
                        fontsize=8.5) 



    axs['2'].set_title(f"{window}-D Moving Average of last {number_of_days} days", size=13) 
    axs['2'].set_xlabel('', size=14)
    axs['2'].set_ylabel('Ingredient', size=12)
    axs['2'].set_xlim([pd.to_datetime(date_start), pd.to_datetime(date_end)]), 
    axs['2'].set_ylim([0, 10])

    # Set font size for major and minor ticks
    axs['2'].tick_params(axis='x', labelsize=7, rotation=45)  
    axs['2'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

    axs['2'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['2'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
    axs['2'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['2'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['2'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
    axs['2'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)



    
    # Calculate Moving Average (e.g., 7-day)
    for name in selected_names:
        moving_average_plot(ax=axs["2"], df=df, name=name, date_start=date_start, date_end=date_end, window=window, color_gradient=color_gradient)

    axs['2'].legend(loc='upper right', 
                        frameon=True,
                        facecolor='lightgrey',
                        edgecolor='white', 
                        fontsize=8.5) 

    return fig





def create_medication_plot(df, selected_names, date_start, date_end, number_of_days, show_changes=True):

    medication_color_map = lade_medication_color_map("utils\map_medication_colors.json")

    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplot_mosaic([
                                ['1', '1', '1'],
                                ['1', '1', '1'],
                                ['2', '2', '2'],
                                ['2', '2', '2'],
                                ],
                                figsize=(20, 9))

    plt.subplots_adjust(wspace=.2)
    plt.subplots_adjust(hspace=.6)

    fig.suptitle(f'''RHELIZER''', size=15)

    axs['1'].set_title(f"Midication over {number_of_days} days", size=13)
    axs['1'].set_xlabel(' ', size=14)
    axs['1'].set_ylabel('Value', size=12)
    axs['1'].set_xlim([pd.to_datetime(date_start), pd.to_datetime(date_end)]), 
    axs['1'].set_ylim([0, 10])

    # Set font size for major and minor ticks
    axs['1'].tick_params(axis='x', labelsize=7, rotation=45)  
    axs['1'].tick_params(axis='x', which='minor', labelsize=7, rotation=45) 

    axs['1'].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(TU, WE, TH, FR, SA, SU)))
    axs['1'].xaxis.set_major_formatter(mdates.DateFormatter('''%d.%m'''))
    axs['1'].grid(visible=True, which='major', color='grey', axis='x', linestyle='--', linewidth=0.3)

    axs['1'].xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(MO)))
    axs['1'].xaxis.set_minor_formatter(mdates.DateFormatter('''%d.%m''')) # \n %a'
    axs['1'].grid(visible=True, which='minor', color='black', axis='x', linestyle='--', linewidth=0.3)


    bottom = None
    for name in selected_names:
        # if name == "Pregabalin":
        #     sns.lineplot(data=df[name]*0.02, label= f"{name.title()}", linestyle='--', linewidth=1, ax=axs['1']) # color='black'
        #     axs["1"].scatter(df.index, df[name]*0.02, color='grey', s=15)
        #     for date, value in df[name].loc[date_start:date_end].items():
        #         if not pd.isna(value):   
        #             axs["1"].text(date, (value*0.02)+0.15, f"{round(value)}", va='bottom', ha='center', fontsize=9)
  
        if name in ["Trock mor dig", "Trock ab dig", "Trockenheit mittelwert"]:
            # create a scatterplot with categories and trockenheit plot
            plot_scatter_color_categories(df=df, name=name, ax=axs['1']) 
            plot_trockenheit(ax=axs["1"], df=df, name=name, date_start=date_start, date_end=date_end)
        
        elif name == "Schmerz dig":
            plot_schmerz(ax=axs["1"], df=df, name=name, date_start=date_start, date_end=date_end)

        

        else:
            name_normalized = f"{name}_normalized"

            bar_width = 0.5  # Adjust the bar width as needed
            # Plot stacked bars
            if bottom is None:
                bottom = df[name_normalized]
                axs['1'].bar(df.index, df[name_normalized], label=f"{name_normalized.title()}", 
                            color=medication_color_map[name]["color"], alpha=1, width=bar_width)
            else:
                axs['1'].bar(df.index, df[name_normalized], label=f"{name_normalized.title()}", 
                            color=medication_color_map[name]["color"], alpha=1, width=bar_width, bottom=bottom)
                bottom += df[name_normalized]  # Update the bottom for the next medication

    if show_changes == True:
        plot_changes(axs['1'], df=df, date_start=pd.to_datetime(date_start), date_end=pd.to_datetime(date_end))

    
    axs['1'].legend(loc='upper right', 
                    frameon=True,
                    facecolor='lightgrey',
                    edgecolor='white', 
                    fontsize=8.5) 

    return fig










def show_date_range_picker(plot_title):
    today = datetime.today() 
    min_date = pd.to_datetime('2024-02-07')               
    end_date = today

    start_date, end_date = date_range_picker(title=f"Select a date range for {plot_title}", 
                                            default_start=today - timedelta(days=85), 
                                            default_end=today, 
                                            min_date=min_date)
    
    number_of_days = end_date - start_date
    
    return start_date, end_date, number_of_days

