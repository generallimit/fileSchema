import os
import pandas as pd
import json
import hashlib
import shutil

# Define directories
input_dir = "moved_files/documents/"
output_dir = "moved_files/parsed/"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Dictionary to store schema hashes
schema_map = {}

def get_schema(df):
    """Generate schema from DataFrame."""
    schema = {col: str(df[col].dtype) for col in df.columns}
    return schema

def hash_schema(schema):
    """Generate a hash for the schema to uniquely identify it."""
    return hashlib.md5(json.dumps(schema, sort_keys=True).encode()).hexdigest()

# Process files
for filename in os.listdir(input_dir):
    if filename.endswith(".txt") or filename.endswith(".csv"):
        file_path = os.path.join(input_dir, filename)
        
        try:
            # Read pipe-delimited file
            df = pd.read_csv(file_path, delimiter="|", nrows=0, encoding="latin-1")
            
            # Get schema and hash
            schema = get_schema(df)
            schema_hash = hash_schema(schema)
            
            # Define schema JSON file
            schema_file = os.path.join(output_dir, f"{schema_hash}.json")
            
            # Save schema if new
            if schema_hash not in schema_map:
                schema_map[schema_hash] = schema
                with open(schema_file, "w") as f:
                    json.dump(schema, f, indent=4)
            
            # Move file to corresponding folder
            schema_folder = os.path.join(output_dir, schema_hash)
            os.makedirs(schema_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(schema_folder, filename))
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Processing complete.")
