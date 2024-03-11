import os
import shutil
import zipfile

collect_from_dir = os.getcwd()
extract_to_directory = os.path.join(collect_from_dir, "data")
raw_dir = os.path.join(extract_to_directory, "raw_data")

os.makedirs(extract_to_directory, exist_ok=True)
os.makedirs(raw_dir, exist_ok=True)

file_index = 1
for filename in os.listdir(collect_from_dir): 
    if filename.startswith('Acceleration') and filename.endswith('.zip'):

        zip_file_path = os.path.join(collect_from_dir, filename)
        
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            if 'Raw Data.csv' in zip_ref.namelist():
                with zip_ref.open('Raw Data.csv') as raw_data:
                    content = raw_data.read()
                    new_file_path = os.path.join(extract_to_directory, f"{file_index}.csv")
                    
                    with open(new_file_path, 'wb') as new_file:
                        new_file.write(content)
            file_index += 1
        
        print(f"Extracted {filename} to {extract_to_directory}")        
        shutil.move(zip_file_path, raw_dir)
        