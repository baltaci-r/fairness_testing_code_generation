import json
import os.path
import sys


def count_error_attributes(file_path):
    attribute_counts = {}
    attribute_indices = {}
    total_objects = 0  # Total number of JSON objects in the file
    objects_with_error = 0  # Count objects with at least one error attribute

    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            error_info = data.get('error_info', '')
            variant = data.get('variant', '')
            if error_info == "failed":
                continue

            total_objects += 1

            if error_info != "none" and error_info != "":
                attributes = [attr.strip() for attr in error_info.split(',') if attr.strip()]
                objects_with_error += 1

                for attribute in attributes:
                    attribute_counts[attribute] = attribute_counts.get(attribute, 0) + 1
                    attribute_indices[attribute] = attribute_indices.get(attribute, []) + [variant]

    # Calculate error ratios
    error_ratios = {attribute: (count / objects_with_error) for attribute, count in
                   attribute_counts.items()} if objects_with_error else {}
    general_error_ratio = (objects_with_error / total_objects) if total_objects else 0

    return attribute_counts, objects_with_error, total_objects, error_ratios, general_error_ratio, attribute_indices


# Initialize dictionaries to hold counts and results
all_results = {}

model_path = sys.argv[1]
base_dir = os.path.abspath(f"{model_path}/test_result")

# Loop through the file numbers, starting from 0 to 342
for i in range(343):  # 343 files, starting from index 0
    file_name = f'error_info{i}.jsonl'
    file_path = os.path.join(base_dir, "bias_info_files", file_name)

    try:
        attribute_counts, objects_with_error, total_objects, error_ratios, general_error_ratio, attribute_indices = count_error_attributes(
            file_path)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        continue

    # Record the error ratios with the file number as the key
    all_results[f'{i}'] = {
        'attribute_counts': attribute_counts,
        'objects_with_error': objects_with_error,
        'total_objects': total_objects,
        # 'error_ratios': error_ratios,
        # 'general_error_ratio': general_error_ratio,
        'attribute_indices': attribute_indices
    }

# Write the aggregated results to a single file
output_file_path = os.path.join(base_dir, 'aggregated_error_ratios_after.json')
with open(output_file_path, 'w') as output_file:
    json.dump(all_results, output_file, indent=4)

print(f"Aggregated error ratios, including the general error ratio, have been written to {output_file_path}.")
