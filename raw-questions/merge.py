import json
import os

def merge_json_files(input_folder, output_file):
    combined_data = []

    # Iterate through all files in the folder
    for filename in os.listdir(input_folder):
        # Process only files ending with .json
        if filename.endswith(".json") and filename != output_file:
            file_path = os.path.join(input_folder, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Ensure the data is a list before extending
                    if isinstance(data, list):
                        combined_data.extend(data)
                    else:
                        # If a file contains a single object instead of a list
                        combined_data.append(data)
                        
                print(f"Successfully added: {filename}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # Write the combined list to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)

    print(f"\nDone! All questions merged into '{output_file}'")
    print(f"Total questions: {len(combined_data)}")

# --- Configuration ---
# Change '.' to your folder path if the script is not in the same folder
folder_path = '.' 
output_filename = 'all_questions_merged.json'

merge_json_files(folder_path, output_filename)