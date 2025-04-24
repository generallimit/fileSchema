import os
import json
import shutil
import csv
from lxml import etree
from difflib import unified_diff

input_dir = "path/to/xml_files"
output_dir = "path/to/output_dir"
os.makedirs(output_dir, exist_ok=True)

schema_versions = []
schema_labels = {}
file_version_map = []

def extract_schema(element, prefix=""):
    schema = set()
    for child in element:
        tag_path = f"{prefix}{child.tag}"
        schema.add(tag_path)
        if child.attrib:
            for attr in child.attrib:
                schema.add(f"{tag_path}[@{attr}]")
        schema.update(extract_schema(child, prefix=tag_path + "/"))
    return schema

def get_schema_from_xml(file_path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()
    children = list(root)
    base = children[0] if children else root
    return sorted(extract_schema(base))

def schema_to_key(schema_list):
    return json.dumps(schema_list, sort_keys=True)

# Main processing loop
for filename in os.listdir(input_dir):
    if filename.endswith(".xml"):
        file_path = os.path.join(input_dir, filename)

        try:
            schema = get_schema_from_xml(file_path)
            schema_key = schema_to_key(schema)

            if schema_key not in schema_labels:
                version_label = f"V{len(schema_versions)+1}"
                schema_versions.append(schema)
                schema_labels[schema_key] = version_label

                # Save schema to JSON
                schema_file = os.path.join(output_dir, f"{version_label}.json")
                with open(schema_file, "w") as f:
                    json.dump(schema, f, indent=2)

            version = schema_labels[schema_key]
            version_folder = os.path.join(output_dir, version)
            os.makedirs(version_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(version_folder, filename))

            # Track file mapping
            file_version_map.append((filename, version))

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Save CSV summary
csv_file = os.path.join(output_dir, "file_version_summary.csv")
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Filename", "SchemaVersion"])
    writer.writerows(file_version_map)

# Save schema diffs
diffs_file = os.path.join(output_dir, "schema_diff_summary.txt")
with open(diffs_file, "w") as f:
    for i, schema_a in enumerate(schema_versions):
        version_a = f"V{i+1}"
        for j in range(i+1, len(schema_versions)):
            schema_b = schema_versions[j]
            version_b = f"V{j+1}"
            diff = list(unified_diff(schema_a, schema_b, fromfile=version_a, tofile=version_b, lineterm=''))
            if diff:
                f.write(f"--- Diff between {version_a} and {version_b} ---\n")
                f.write("\n".join(diff))
                f.write("\n\n")

print("Processing Complete: Files organized, CSV summary written, schema diffs saved.")
