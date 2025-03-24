import os
import pandas as pd
import json
import shutil

# Define directories
input_dir = "fileSchema/moved_files/documents/"
output_dir = "fileSchema/moved_files/documents/parsed/"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Dictionary to store schema versions
schema_map = {}

def get_schema(df):
    """Generate schema from DataFrame."""
    schema = {col: str(df[col].dtype) for col in df.columns}
    return schema

def load_existing_schemas():
    """Load existing schemas from the output directory."""
    existing_schemas = {}
    for filename in os.listdir(output_dir):
        if filename.endswith(".json"):
            try:
                version = filename.split(".")[0]
                file_path = os.path.join(output_dir, filename)
                with open(file_path, "r") as f:
                    schema = json.load(f)
                    existing_schemas[version] = schema
            except Exception as e:
                print(f"Error loading schema from {filename}: {e}")
    return existing_schemas

# Load existing schemas
schema_map = load_existing_schemas()

# Determine the next schema version if needed
if schema_map:
    last_version = max(int(v.replace("V", "")) for v in schema_map.keys() if v.startswith("V"))
    next_version_number = last_version + 1
else:
    next_version_number = 1

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
                schema_version = f"V{next_version_number}"
                schema_map[schema_version] = schema
                schema_file = os.path.join(output_dir, f"{schema_version}.json")
                with open(schema_file, "w") as f:
                    json.dump(schema, f, indent=4)
                next_version_number +=1
            
            # Move file to corresponding folder
            schema_folder = os.path.join(output_dir, schema_version)
            os.makedirs(schema_folder, exist_ok=True)
            shutil.copy2(file_path, os.path.join(schema_folder, filename))
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Processing complete.")
