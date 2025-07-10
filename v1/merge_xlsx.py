import os
import pandas as pd

# Folder containing the Excel files
folder_path = '/Users/berkay.akin/Desktop/sba/class-scheduler/'

# List to hold dataframes
dfs = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(folder_path, filename)
        # Read the Excel file
        df = pd.read_excel(file_path)
        dfs.append(df)

# Concatenate all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

# Save the merged dataframe to a new Excel file
merged_df.to_excel(os.path.join(folder_path, 'merged_output.xlsx'), index=False)