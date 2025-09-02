import os
import shutil
import json

BASE_PATH = "."
SORTED_DATA_PATH = os.path.join(BASE_PATH, "data")
ANNOTATIONS_PATH = os.path.join(BASE_PATH, "annotations")
TEMP_IMAGES_PATH = os.path.join(BASE_PATH, "temp_images")

files_moved_count = 0
print("Starting the sorting process...")

for split in ["train", "val", "test"]:
    split_annotations_dir = os.path.join(ANNOTATIONS_PATH, "annotations", split)
    print(f"\nProcessing '{split}' split...")
    
    if not os.path.exists(split_annotations_dir):
        print(f"  - WARNING: Directory not found: {split_annotations_dir}. Skipping.")
        continue

    json_files = [f for f in os.listdir(split_annotations_dir) if f.endswith('.json')]
    
    for json_file in json_files:
        gesture_name = os.path.splitext(json_file)[0]
        final_dest_folder = os.path.join(SORTED_DATA_PATH, split, gesture_name)
        os.makedirs(final_dest_folder, exist_ok=True)
        
        with open(os.path.join(split_annotations_dir, json_file), 'r') as f:
            annotations = json.load(f)

        for image_id in annotations:
            # Add the .jpg file extension to the image ID to create the full filename
            image_filename = f"{image_id}.jpg"            
            source_image_path = ""
            if gesture_name == 'no_gesture':
                # Use the new filename variable to build the path
                source_image_path = os.path.join(TEMP_IMAGES_PATH, image_filename)
            else:
                # Use the new filename variable to build the path
                source_image_path = os.path.join(TEMP_IMAGES_PATH, gesture_name, image_filename)

            dest_image_path = os.path.join(final_dest_folder, image_filename)

            if os.path.exists(source_image_path):
                shutil.move(source_image_path, dest_image_path)
                files_moved_count += 1
            # else:
            #     print(f"  - WARNING: Source image not found at {source_image_path}")
            #     pass

print(f"\n✅ Sorting complete! Total files moved: {files_moved_count}")

print("\nInitiating cleanup phase...")

if files_moved_count > 0:
    print(f"Cleanup condition met ({files_moved_count} files were moved). Deleting temporary folders.")
    if os.path.exists(TEMP_IMAGES_PATH):
        shutil.rmtree(TEMP_IMAGES_PATH)
    if os.path.exists(ANNOTATIONS_PATH):
        shutil.rmtree(ANNOTATIONS_PATH)
    print("✅ Cleanup finished.")
else:
    print("❌ WARNING: Cleanup condition not met. No files were moved during sorting.")
    print("      The temporary folders will NOT be deleted for debugging.")
