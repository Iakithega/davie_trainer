import pandas as pd
import numpy as np


# # Function to split a single value
# def split_value(value):
#         if pd.isna(value):
#             return pd.NA, pd.NA
#         parts = str(value).split('|')
#         if len(parts) != 2:
#             return pd.NA, pd.NA
#         try:
#             weight = float(parts[0])
#             reps = int(parts[1])
#             return weight, reps
#         except ValueError:
#             return pd.NA, pd.NA

# def weight_reps_exctracter(df):
#     # Identify weighted exercise columns
#     weighted_columns = [col for col in df.columns if col.startswith('Weighted')]

#     # Process each weighted column
#     for col in weighted_columns:

#         if not col.startswith('Weighted Turm Rudern'):
            
#             weight_col = f"{col} weight"
#             reps_col = f"{col} reps"

#             # Split the column
#             df[[weight_col, reps_col]] = df[col].apply(split_value).apply(pd.Series)
            
#             # Ensure correct data types
#             df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
#             df[reps_col] = pd.to_numeric(df[reps_col], errors='coerce', downcast='integer')

#         elif col.startswith('Weighted Turm Rudern'):
#             band_col = f"{col} band"
#             weight_col = f"{col} weight"
#             reps_col = f"{col} reps"
            
#             # Split the column
#             df[[band_col, weight_col, reps_col]] = df[col].apply(split_value).apply(pd.Series)

#             # Ensure correct data types
#             df[band_col] = pd.to_numeric(df[band_col], errors='coerce')
#             df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
#             df[reps_col] = pd.to_numeric(df[reps_col], errors='coerce', downcast='integer')           
    
#     return df


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
            band_col = f"{col} band"
            weight_col = f"{col} weight"
            reps_col = f"{col} reps"

            # Split the column (expecting 3 parts for this exercise)
            df[[band_col, weight_col, reps_col]] = df[col].apply(lambda x: split_value(x, 3)).apply(pd.Series)

            # Ensure correct data types
            df[band_col] = pd.to_numeric(df[band_col], errors='coerce')
            df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
            df[reps_col] = pd.to_numeric(df[reps_col], errors='coerce', downcast='integer')           
    
    return df

    


