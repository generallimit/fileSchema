### File Schema Discovery V ###
---
This Python script scans the input directory for *txt* or *csv* files, discovers their schema, and organizes them based on their schema.

#### How it works:
1. **Setup Directories**:
   - The script defines an input directory (`moved_files/documents/`) where the files to be processed are located.
   - An output directory (`moved_files/parsed/`) is defined where the processed files will be moved.

2. **Ensure Output Directory Exists**:
   - The script ensures that the output directory exists, creating it if necessary.

3. **Schema Generation**:
   - For each file in the input directory, the script reads the file into a pandas DataFrame using a pipe (`|`) delimiter.
   - It generates a schema from the DataFrame, which is a dictionary mapping each column name to its data type.

4. **Schema Management**:
   - The script checks if the generated schema already exists in the `schema_map` dictionary.
   - If the schema exists, it retrieves the corresponding schema version.
   - If the schema does not exist, it assigns a new version (`V1`, `V2`, etc. As well, the schema can be hashed for unique values) and saves the schema as a JSON file in the output directory.

5. **File Organization**:
   - The script moves the file to a subdirectory in the output directory named after the schema version.

6. **Error Handling**:
   - If an error occurs while processing a file, the script prints an error message and continues processing the next file.
