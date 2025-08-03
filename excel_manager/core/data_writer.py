import pandas as pd

def write_dataframe_to_file(df_combined, resoconto_path):
    df_combined.to_excel(resoconto_path, index=False)
