import os
import shutil

GESTURES_TO_KEEP = {
    'fist', 
    'like', 
    'no_gesture', 
    'palm'
}

DATA_PATH = "data"

print("Starting Cleanup Script")

if not os.path.isdir(DATA_PATH):
    print(f"Error: Data directory not found at '{DATA_PATH}'. Exiting.")
else:
    # Loop through each split directory (train, val, test)
    for split_name in os.listdir(DATA_PATH):
        split_dir_path = os.path.join(DATA_PATH, split_name)
        
        if os.path.isdir(split_dir_path):
            print(f"\nProcessing directory: {split_dir_path}")
            
            # Loop through each gesture folder in the split directory
            for gesture_name in os.listdir(split_dir_path):
                gesture_folder_path = os.path.join(split_dir_path, gesture_name)
                
                # Check if the folder is actually a directory and NOT in our keep list
                if os.path.isdir(gesture_folder_path) and gesture_name not in GESTURES_TO_KEEP:
                    try:
                        print(f"  - Deleting unwanted folder: {gesture_folder_path}")
                        shutil.rmtree(gesture_folder_path)
                    except OSError as e:
                        print(f"  - Error deleting {gesture_folder_path} : {e.strerror}")

print("\n--- Cleanup Complete ---")
