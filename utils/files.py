from utils.gestures import *

import os
import shutil
import zipfile
import re
import pandas as pd
import math

DATA_DIR = os.path.join(os.getcwd(), "data")

def get_data_from_files(scaler=None, number_of_rows_to_trim=0, test_percentage=0.2):
    """
    Reads data from multiple files and returns a concatenated DataFrame.

    Args:
        scaler (object, optional): Scaler object used to scale the data. Defaults to None.
        number_of_rows_to_trim (int, optional): Number of rows to trim from the beginning and end of each file. Defaults to 0.

    Returns:
        pd.DataFrame: Concatenated DataFrame containing the data from all files.

    """
    training_data = []
    testing_data = []

    for gesture in get_gestures():
        csvs = get_gesture_csvs(gesture)
        num_of_files = len(csvs)
        testing_files = math.ceil(num_of_files * test_percentage)

        for i, file in enumerate(csvs):
            data = pd.read_csv(f'data/{gesture}/{file}')
            data.columns = get_columns()

            data = data.iloc[number_of_rows_to_trim:-number_of_rows_to_trim]

            if scaler:
                scaled_features = scaler.fit_transform(data)
            else:
                scaled_features = data
                
            df = pd.DataFrame(scaled_features, columns=data.columns)
            df['file_number'] = int(i)
            df['gesture'] = str(gesture)

            if i < testing_files:
                testing_data.append(df)
            else:
                training_data.append(df)

    return pd.concat(training_data, ignore_index=True), pd.concat(testing_data, ignore_index=True)

def find_highest_numbered_file(directory, full_path=False):
    """
    Finds the highest numbered file in the given directory.

    Args:
        directory (str): The directory to search for files.
        full_path (bool, optional): Specifies whether to return the full path of the file. 
            Defaults to False.

    Returns:
        str or int: The path of the highest numbered file if `full_path` is True, 
            otherwise the highest number found in the file names.

    """
    highest_number = -1
    file_with_highest_number = None

    for entry in os.scandir(directory):
        if entry.is_file():
            # Find all numbers in the filename
            numbers = re.compile(r'\d+').findall(entry.name)
            if numbers:
                # Convert found strings to integers and get the max
                max_number_in_file = max(map(int, numbers))
                if max_number_in_file > highest_number:
                    highest_number = max_number_in_file
                    file_with_highest_number = entry.path

    return file_with_highest_number if full_path else 1 if highest_number == -1 else highest_number

def process_zip(gesture):
    """
    Process the zip files containing raw data for a specific gesture.

    Parameters:
    gesture (str): The name of the gesture [circle, come, go, wave]

    Returns:
    None
    """

    gesture_dir = os.path.join(DATA_DIR, gesture)
    unprocessed_dir = os.path.join(gesture_dir, "unprocessed")
    processed_dir = os.path.join(gesture_dir, "processed")

    file_index = find_highest_numbered_file(gesture_dir)

    for filename in os.listdir(unprocessed_dir): 
        if filename.endswith('.zip'):

            zip_file_path = os.path.join(unprocessed_dir, filename)
            
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                if 'Raw Data.csv' in zip_ref.namelist():
                    with zip_ref.open('Raw Data.csv') as raw_data:
                        content = raw_data.read()
                        new_file_path = os.path.join(DATA_DIR, gesture, f"{file_index}.csv")
                        
                        with open(new_file_path, 'wb') as new_file:
                            new_file.write(content)
                file_index += 1
            
            
            shutil.move(zip_file_path, processed_dir)

def process_all_zips():
    """
    This function iterates over each gesture in the DATA_DIR directory and checks if there are any unprocessed zip files.
    If there are unprocessed files, it calls the `process_zip` function to extract the files and move them to the processed directory.

    Parameters:
    None

    Returns:
    None
    """
    for gesture in get_gestures():
        if os.path.isdir(os.path.join(DATA_DIR, gesture)):

            if len(os.listdir(os.path.join(DATA_DIR, gesture, "unprocessed"))) > 0:
                process_zip(gesture)
                print(f"Extracted all {gesture} gestures to {os.path.join(DATA_DIR, gesture)}")    
            else:
                print(f"No unprocessed files found for {gesture}")

def get_gesture_csvs(gesture):
      """
      Get all the files for a specific gesture.
      
      Parameters:
      gesture (str): The name of the gesture [circle, come, go, wave]
      
      Returns:
      list: A list of all the files for the specified gesture
      """
      gesture_dir = os.path.join(DATA_DIR, gesture)
      return [file for file in os.listdir(gesture_dir) if file.endswith('.csv')]

