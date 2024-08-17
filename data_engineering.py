import pandas as pd
import numpy as np

def weight_reps_exctracter(df):
    # Function to split a single value
    def split_value(value):
        if pd.isna(value):
            return pd.NA, pd.NA
        parts = str(value).split('|')
        if len(parts) != 2:
            return pd.NA, pd.NA
        try:
            weight = float(parts[0])
            reps = int(parts[1])
            return weight, reps
        except ValueError:
            return pd.NA, pd.NA

    # Identify weighted exercise columns
    weighted_columns = [col for col in df.columns if col.startswith('Weighted')]

    # Process each weighted column
    for col in weighted_columns:
        # Split the column
        weight_col = f"{col} - Weight"
        reps_col = f"{col} - Reps"
        
        df[[weight_col, reps_col]] = df[col].apply(split_value).apply(pd.Series)
        
        # Ensure correct data types
        df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
        df[reps_col] = pd.to_numeric(df[reps_col], errors='coerce', downcast='integer')
    
    return df



    


