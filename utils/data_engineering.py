import pandas as pd
import numpy as np



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
    df['Hammer Curls Average reps all sets'] = df[hammer_reps_columns].mean(axis=1, skipna=True)
    df['Hammer Curls Max reps all sets'] = df[hammer_reps_columns].max(axis=1, skipna=True)
    df['Hammer Curls Sum reps all sets'] = df[hammer_reps_columns].sum(axis=1, skipna=True)    


    # Multiply the reps by their corresponding weight for each set to give more value to reps with heavier weight
    df['Hammer Curls Weight Factored Sum all sets'] = (df[hammer_reps_columns] * (df[hammer_weight_columns])).sum(axis=1)
    df['Hammer Curls Weight Factored Average all sets'] = (df[hammer_reps_columns] * (df[hammer_weight_columns])).mean(axis=1)
    df['Hammer Curls Weight Factored Max all sets'] = (df[hammer_reps_columns] * (df[hammer_weight_columns])).max(axis=1)


    # calculations and columns for weighted Turm Zug
    trmzg_reps_columns = df.filter(regex="Turm Zug.*reps").columns
    trmzg_weight_columns = df.filter(regex="Turm Zug.*weight").columns

    # Calculate average, max, and sum for the reps
    df['Turm Zug Average reps all sets'] = df[trmzg_reps_columns].mean(axis=1, skipna=True)
    df['Turm Zug Max reps all sets'] = df[trmzg_reps_columns].max(axis=1, skipna=True)
    df['Turm Zug Sum reps all sets'] = df[trmzg_reps_columns].sum(axis=1, skipna=True)    

    # Multiply the reps by their corresponding weight for each set to give more value to reps with heavier weight
    df['Turm Zug Weight Factored Sum all sets'] = (df[trmzg_reps_columns] * (df[trmzg_weight_columns] ** weight_factor)).sum(axis=1)
    df['Turm Zug Weight Factored Average all sets'] = (df[trmzg_reps_columns] * (df[trmzg_weight_columns] ** weight_factor)).mean(axis=1)
    df['Turm Zug Weight Factored Max all sets'] = (df[trmzg_reps_columns] * (df[trmzg_weight_columns] ** weight_factor)).max(axis=1)

  
    return df
    



def calc_sets_overview_with_weights_dstanced(df, weight_factor=1):
    # calculations and columns for weighted hammer curls
    trmrd_reps_columns = df.filter(regex="Weighted Turm Rudern.*reps").columns
    trmrd_distance_columns = df.filter(regex="Weighted Turm Rudern.*distance").columns
    trmrd_weight_columns = df.filter(regex="Weighted Turm Rudern.*weight").columns

    # Calculate average, max, and sum for the reps
    df['Turm Rudern Average reps all sets'] = df[trmrd_reps_columns].mean(axis=1, skipna=True)
    df['Turm Rudern Max reps all sets'] = df[trmrd_reps_columns].max(axis=1, skipna=True)
    df['Turm Rudern Sum reps all sets'] = df[trmrd_reps_columns].sum(axis=1, skipna=True)    

    # Multiply the reps by their corresponding weight for each set to give more value to reps with heavier weight
    df['Turm Rudern Weight Factored Sum all sets'] = (df[trmrd_reps_columns] * df[trmrd_distance_columns] * df[trmrd_weight_columns] * weight_factor).sum(axis=1)
    df['Turm Rudern Weight Factored Average all sets'] = (df[trmrd_reps_columns] * df[trmrd_distance_columns] * df[trmrd_weight_columns] * weight_factor).mean(axis=1)
    df['Turm Rudern Weight Factored Max all sets'] = (df[trmrd_reps_columns] * df[trmrd_distance_columns] * df[trmrd_weight_columns] * weight_factor).max(axis=1)

    return df