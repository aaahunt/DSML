import os
import re

cwd = os.getcwd()
data_dir = os.path.join(cwd, "data")
raw_dir = os.path.join(data_dir, "raw")
        
def rename_files(folder, file_regex, prefix):

        gesture_folder = os.path.join(data_dir, folder)

        for filename in os.listdir(gesture_folder):
            file_path = os.path.join(gesture_folder, filename)

            if (re.search(file_regex, filename)):
                new_filename = prefix + filename[-5:]
                new_file_path = os.path.join(gesture_folder, new_filename)
                os.rename(file_path, new_file_path)
                print(f"Renamed {filename} to {new_filename}")

for folder in ['circle', 'come', 'go', 'wave']:
    rename_files(folder, r'^\d+\.csv$', 'shreeya_') ## ^\d+\.csv$ matches any filename that starts with one or more digits and ends with .csv