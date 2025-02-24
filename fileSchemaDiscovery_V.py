import os
import pandas as pd
import json
import shutil

# Define directories
input_dir = "moved_files/documents/"
output_dir = "moved_files/parsed/"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Dictionary to store schema versions
schema_map = {}
schema_version = 1

def get_schema(df):
    """Generate schema from DataFrame."""
    schema = {col: str(df[col].dtype) for col in df.columns}
    return schema

# Process files
for filename in os.listdir(input_dir):
    if filename.endswith(".txt") or filename.endswith(".csv"):
        file_path = os.path.join(input_dir, filename)
        
        try:
            # Read pipe-delimited file
            df = pd.read_csv(file_path, delimiter="|", nrows=0, encoding="latin-1")
            
            # Get schema
            schema = get_schema(df)
            
            # Check if schema already exists
            schema_exists = False
            for version, existing_schema in schema_map.items():
                if existing_schema == schema:
                    schema_exists = True
                    schema_version = version
                    break
            
            if not schema_exists:
                schema_version = f"V{len(schema_map) + 1}"
                schema_map[schema_version] = schema
                schema_file = os.path.join(output_dir, f"{schema_version}.json")
                with open(schema_file, "w") as f:
                    json.dump(schema, f, indent=4)
            
            # Move file to corresponding folder
            schema_folder = os.path.join(output_dir, schema_version)
            os.makedirs(schema_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(schema_folder, filename))
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Processing complete.")
