import pandas as pd
import numpy as np
import re

# def load_data(file_path):
#     return pd.read_excel(file_path)

# Drop unnecessary columns
def drop_irrelevant_columns(df: pd.DataFrame, columns) -> pd.DataFrame:
    return df.drop(columns=columns, errors='ignore')

# Standardize column names
def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    return df

# Filtering surfing-related attacks
def filter_surfing_attacks(df: pd.DataFrame) -> pd.DataFrame:
    # return df[df['Activity'].str.contains('surf', case=False, na=False)].copy()
    # This matches 'surf', 'surfing', 'surfer', 'windsurf', 'kite-surf', etc., and ignores words like 'surface'
    regex_pattern = r"\bsurf\w*\b"  # \b = word boundary, \w* = zero or more word chars (matches 'surf', 'surfing', etc.)
    surfing_activities = df['Activity'].str.contains(regex_pattern, flags=re.IGNORECASE, na=False, regex=True)
    df_surf = df[surfing_activities].copy().reset_index(drop=True)
    return df_surf

# Standardize 'Country' and 'State'
def clean_country_state(df: pd.DataFrame) -> pd.DataFrame:
    df['Country'] = df['Country'].str.upper().str.strip()
    df['State'] = df['State'].str.title().str.strip()
    return df

# Convert 'Date' from strings (or other formats) to pandas datetime object
# Convert 'Year' to integer, handle missing/invalid as NaN
def clean_date_year(df: pd.DataFrame) -> pd.DataFrame:
    df['Date'] = pd.to_datetime(df['Date'], format="%d %m %Y", errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
    return df

# Standardize 'Sex'
def clean_sex_column(df: pd.DataFrame) -> pd.DataFrame:
    df['Sex'] = df['Sex'].apply(
        lambda x: (
            None if pd.isnull(x)
            else 'M' if str(x).strip().upper() in ['MALE', 'M']
            else 'F' if str(x).strip().upper() in ['FEMALE', 'F']
            else None
        )
    )
    return df

# Standarize values in column Fatal_Y/N using regex
def map_fatal(df: pd.DataFrame) -> pd.DataFrame:
    def clean_fatal_yn(val):
        if pd.isnull(val):
            return 'Unknown'
        val_str = str(val).strip().upper()
        if re.search(r'\bY\b', val_str) or re.search(r'\bF\b', val_str) or re.match(r'Y', val_str):
            return 'Y'
        if re.search(r'\bN\b', val_str) or re.search(r'\bM\b', val_str) or re.match(r'N', val_str):
            return 'N'
        return 'Unknown'
        
    df['Fatal_Y/N'] = df['Fatal_Y/N'].apply(clean_fatal_yn)
    return df

# def map_fatal(df: pd.DataFrame) -> pd.DataFrame:
#     df['Fatal'] = df['Fatal_Y/N'].str.upper().map({'Y': 1, 'N': 0})
#     return df

def main_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_drop = ['Unnamed: 21', 'Unnamed: 22', 'pdf', 'href formula', 'href', 'Case Number', 'Case Number.1', 'original order', 'Source']
    # df = load_data(file_path)
    df = drop_irrelevant_columns(df, columns_to_drop)
    df = standardize_columns(df)
    df = filter_surfing_attacks(df)
    df = clean_country_state(df)
    df = clean_date_year(df)
    df = clean_sex_column(df)
    df = map_fatal(df)
    return df