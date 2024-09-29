import pandas as pd
import numpy as np
import re




def split_value(value, expected_parts=2):
    if pd.isna(value):
        return [pd.NA] * expected_parts
    
    # Replace comma with dot for decimal handling
    value = str(value).replace(',', '.')
    
    parts = value.split('|')
    
    if len(parts) != expected_parts:
        return [pd.NA] * expected_parts
    
    try:
        # Convert to appropriate types (float for weight, int for reps)
        if expected_parts == 2:
            weight = float(parts[0])
            reps = int(parts[1])
            return weight, reps
        elif expected_parts == 3:
            band_weight = float(parts[0])
            weight = float(parts[1])
            reps = int(parts[2])
            return band_weight, weight, reps
    except ValueError:
        return [pd.NA] * expected_parts


def weight_reps_exctracter(df):
    # Identify weighted exercise columns
    weighted_columns = [col for col in df.columns if col.startswith('Weighted')]

    # Process each weighted column
    for col in weighted_columns:

        if not col.startswith('Weighted Turm Rudern'):
            weight_col = f"{col} weight"
            reps_col = f"{col} reps"

            # Split the column (expecting 2 parts)
            df[[weight_col, reps_col]] = df[col].apply(split_value).apply(pd.Series)

            # Ensure correct data types
            df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
            df[reps_col] = pd.to_numeric(df[reps_col], errors='coerce', downcast='integer')

        elif col.startswith('Weighted Turm Rudern'):
            band_col = f"{col} distance"
            weight_col = f"{col} band"
            reps_col = f"{col} reps"

            # Split the column (expecting 3 parts for this exercise)
            df[[band_col, weight_col, reps_col]] = df[col].apply(lambda x: split_value(x, 3)).apply(pd.Series)

            # Ensure correct data types
            df[band_col] = pd.to_numeric(df[band_col], errors='coerce')
            df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
            df[reps_col] = pd.to_numeric(df[reps_col], errors='coerce', downcast='integer')           
    
    return df

    
def calc_sets_overview_no_weights(df):
    liegestuetze_columns = df.filter(regex="Liegestütz").columns
    df['Liegestütz Average all sets'] = df[liegestuetze_columns].mean(axis=1, skipna=True)
    df['Liegestütz Max all sets'] = df[liegestuetze_columns].max(axis=1, skipna=True)
    df['Liegestütz Sum all sets'] = df[liegestuetze_columns].sum(axis=1, skipna=True)

    # Calculate the average reps for Planke
    planke_columns = df.filter(regex="Planke").columns
    df['Planke Average all sets'] = df[planke_columns].mean(axis=1, skipna=True)
    df['Planke Max all sets'] = df[planke_columns].max(axis=1, skipna=True)
    df['Planke Sum all sets'] = df[planke_columns].sum(axis=1, skipna=True)

    # Calculate the average reps for Kniebeuge
    kniebeuge_columns = df.filter(regex="Kniebeugen").columns
    df['Kniebeugen Average all sets'] = df[kniebeuge_columns].mean(axis=1, skipna=True)
    df['Kniebeugen Max all sets'] = df[kniebeuge_columns].max(axis=1, skipna=True)
    df['Kniebeugen Sum all sets'] = df[kniebeuge_columns].sum(axis=1, skipna=True)
    
    return df


def calc_sets_overview_with_weights(df, weight_factor=2):
    # calculations and columns for weighted hammer curls
    hammer_reps_columns = df.filter(regex="Weighted Hammer Curls.*reps").columns
    hammer_weight_columns = df.filter(regex="Weighted Hammer Curls.*weight").columns

    # Calculate average, max, and sum for the reps
    df['Weighted Hammer Curls Average reps all sets'] = df[hammer_reps_columns].mean(axis=1, skipna=True)
    df['Weighted Hammer Curls Max reps all sets'] = df[hammer_reps_columns].max(axis=1, skipna=True)
    df['Weighted Hammer Curls Sum reps all sets'] = df[hammer_reps_columns].sum(axis=1, skipna=True)    

    # calculations and columns for weighted Turm Zug
    trmzg_reps_columns = df.filter(regex="Turm Zug.*reps").columns
    trmzg_weight_columns = df.filter(regex="Turm Zug.*weight").columns

    # Calculate average, max, and sum for the reps
    df['Weighted Turm Zug Average reps all sets'] = df[trmzg_reps_columns].mean(axis=1, skipna=True)
    df['Weighted Turm Zug Max reps all sets'] = df[trmzg_reps_columns].max(axis=1, skipna=True)
    df['Weighted Turm Zug Sum reps all sets'] = df[trmzg_reps_columns].sum(axis=1, skipna=True)    



  
    return df
    


def compute_hammer_curls_scores(df):
    # List of sets for 'Weighted Hammer Curls'
    sets = [1, 2, 3, 4]
    
    for set_num in sets:
        # Define the column names for weight and reps
        weight_col = f'Weighted Hammer Curls set {set_num} weight'
        reps_col = f'Weighted Hammer Curls set {set_num} reps'
        
        # Check if both columns exist in the dataframe
        if weight_col in df.columns and reps_col in df.columns:
            # Convert weight and reps columns to numeric, handling errors
            df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
            df[reps_col] = pd.to_numeric(df[reps_col], errors='coerce')
            
            # Compute the new score column using your formula
            score_col = f'Weighted Hammer Curls set {set_num} score'
            df[score_col] = df[reps_col] * 2 ** (df[weight_col] - 2)
        else:
            print(f"Columns for set {set_num} are missing in the dataframe.")
    
    return df

def calc_hammer_curls_score_overview(df):
    score_columns = df.filter(regex=r"Weighted Hammer Curls set \d+ score").columns
    df['Weighted Hammer Curls Average score all sets'] = df[score_columns].mean(axis=1, skipna=True)
    df['Weighted Hammer Curls Max score all sets'] = df[score_columns].max(axis=1, skipna=True)
    df['Weighted Hammer Curls Sum score all sets'] = df[score_columns].sum(axis=1, skipna=True)
    return df


def compute_trmrd_scores(df):
    # List of sets for 'Weighted Turm Rudern'
    sets = [1, 2, 3, 4]
    
    for set_num in sets:
        # Define the column names for weight and reps
        reps_col = f'Weighted Turm Rudern set {set_num} reps'
        band_col = f'Weighted Turm Rudern set {set_num} band'
        distance_col = f'Weighted Turm Rudern set {set_num} distance'
        
        # Check if both columns exist in the dataframe
        if reps_col in df.columns and band_col in df.columns and distance_col in df.columns: 
            # Convert weight and reps columns to numeric, handling errors
            df[reps_col] = pd.to_numeric(df[reps_col], errors='coerce')
            df[band_col] = pd.to_numeric(df[band_col], errors='coerce')
            df[distance_col] = pd.to_numeric(df[distance_col], errors='coerce')
            
            # Compute the new score column using your formula
            score_col = f'Weighted Turm Rudern set {set_num} score'
            df[score_col] = df[reps_col] * df[distance_col]**1.5
        else:
            print(f"Columns for set {set_num} are missing in the dataframe.")
    
    return df

def calc_trmrd_score_overview(df):
    score_columns = df.filter(regex=r"Weighted Turm Rudern set \d+ score").columns
    df['Weighted Turm Rudern Average score all sets'] = df[score_columns].mean(axis=1, skipna=True)
    df['Weighted Turm Rudern Max score all sets'] = df[score_columns].max(axis=1, skipna=True)
    df['Weighted Turm Rudern Sum score all sets'] = df[score_columns].sum(axis=1, skipna=True)
    return df

def calc_sets_overview_with_weights_dstanced(df, weight_factor=1):
    # calculations and columns for weighted hammer curls
    trmrd_reps_columns = df.filter(regex="Weighted Turm Rudern.*reps").columns
    trmrd_distance_columns = df.filter(regex="Weighted Turm Rudern.*distance").columns
    trmrd_weight_columns = df.filter(regex="Weighted Turm Rudern.*weight").columns

    # Calculate average, max, and sum for the reps
    df['Weighted Turm Rudern Average reps all sets'] = df[trmrd_reps_columns].mean(axis=1, skipna=True)
    df['Weighted Turm Rudern Max reps all sets'] = df[trmrd_reps_columns].max(axis=1, skipna=True)
    df['Weighted Turm Rudern Sum reps all sets'] = df[trmrd_reps_columns].sum(axis=1, skipna=True)    

    return df


def compute_trmzg_scores(df):
    # List of sets for 'Weighted Turm Zug'
    sets = [1, 2, 3, 4]
    
    for set_num in sets:
        # Define the column names for weight and reps
        weight_col = f'Weighted Turm Zug set {set_num} weight'
        reps_col = f'Weighted Turm Zug set {set_num} reps'
        
        # Check if both columns exist in the dataframe
        if weight_col in df.columns and reps_col in df.columns:
            # Convert weight and reps columns to numeric, handling errors
            df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
            df[reps_col] = pd.to_numeric(df[reps_col], errors='coerce')
            
            # Compute the new score column using your formula
            score_col = f'Weighted Turm Zug set {set_num} score'
            df[score_col] = df[reps_col] * 2 ** (df[weight_col] - 30)
        else:
            print(f"Columns for set {set_num} are missing in the dataframe.")
    
    return df

def calc_trmzg_score_overview(df):
    score_columns = df.filter(regex=r"Weighted Turm Zug set \d+ score").columns
    df['Weighted Turm Zug Average score all sets'] = df[score_columns].mean(axis=1, skipna=True)
    df['Weighted Turm Zug Max score all sets'] = df[score_columns].max(axis=1, skipna=True)
    df['Weighted Turm Zug Sum score all sets'] = df[score_columns].sum(axis=1, skipna=True)
    return df


def complete_data_wrangeling(initial_data):

    # extract weights and reps and band strength
    data = weight_reps_exctracter(initial_data)

    # calculate no weight averages, max and sum for liegestütze, planke and kniebeugen
    data = calc_sets_overview_no_weights(data)

    # calculate no weight averages, max and sum for weighted Hammer Curls, and Turm Zug
    data = calc_sets_overview_with_weights(data)

    # implements weight factored score column for hammer curls
    data = compute_hammer_curls_scores(data)
    data = calc_hammer_curls_score_overview(data)

    # implements weight factored score column for Turm Rudern
    data = compute_trmrd_scores(data)
    data = calc_trmrd_score_overview(data)

    # implements weight factored score column for Turm Zug
    data = compute_trmzg_scores(data)
    data = calc_trmzg_score_overview(data)

    # calculate no weight averages, max and sum for distanced Turm Rudern
    data = calc_sets_overview_with_weights_dstanced(data)

    return data