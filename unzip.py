import os
import zipfile
import json
import shutil

BASE_PATH = "." 
TEMP_IMAGES_PATH = os.path.join(BASE_PATH, "temp_images")
SORTED_DATA_PATH = os.path.join(BASE_PATH, "data")
ANNOTATIONS_PATH = os.path.join(BASE_PATH, "annotations")

# Create directories inside the current folder
os.makedirs(TEMP_IMAGES_PATH, exist_ok=True)
os.makedirs(SORTED_DATA_PATH, exist_ok=True)
os.makedirs(ANNOTATIONS_PATH, exist_ok=True)

print("Unzipping all downloaded archives...")
all_files_in_dir = os.listdir(BASE_PATH)

for filename in all_files_in_dir:
    if filename.endswith('.zip'):
        print(f"  - Unzipping {filename}...")
        file_path = os.path.join(BASE_PATH, filename)
        
        # Unzip annotations to ANNOTATIONS_PATH
        try: 
            if 'ann_train_val' in filename:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(ANNOTATIONS_PATH)
            else:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(TEMP_IMAGES_PATH)
            os.remove(file_path)
            print(f"    - Deleted {filename} to save space.")
        except zipfile.BadZipFile:
            print(f"❌ WARNING: Could not unzip {filename}. It may be corrupt. Skipping.")
print("Unzipping complete.")
