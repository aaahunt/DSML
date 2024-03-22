import os
import shutil
import zipfile

cwd = os.getcwd()
data_dir = os.path.join(cwd, "data")
raw_dir = os.path.join(data_dir, "raw")

def move_from_zip():
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(raw_dir, exist_ok=True)

    file_index = 1
    for filename in os.listdir(cwd): 
        if filename.startswith('Acceleration') and filename.endswith('.zip'):

            zip_file_path = os.path.join(cwd, filename)
            
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                if 'Raw Data.csv' in zip_ref.namelist():
                    with zip_ref.open('Raw Data.csv') as raw_data:
                        content = raw_data.read()
                        new_file_path = os.path.join(data_dir, f"{file_index}.csv")
                        
                        with open(new_file_path, 'wb') as new_file:
                            new_file.write(content)
                file_index += 1
            
            print(f"Extracted {filename} to {data_dir}")        
            shutil.move(zip_file_path, raw_dir)

move_from_zip()