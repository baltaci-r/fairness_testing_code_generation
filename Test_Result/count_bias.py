import json


def count_bias_attributes(file_path):
    attribute_counts = {}
    total_objects = 0  # Total number of JSON objects in the file
    objects_with_bias = 0  # Count objects with at least one bias attribute

    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            bias_info = data.get('bias_info', '')

            if bias_info == "failed":
                continue

            total_objects += 1

            if bias_info != "none" and bias_info != "":
                attributes = [attr.strip() for attr in bias_info.split(',') if attr.strip()]
                objects_with_bias += 1

                for attribute in attributes:
                    attribute_counts[attribute] = attribute_counts.get(attribute, 0) + 1

    # Calculate bias ratios
    bias_ratios = {attribute: (count / objects_with_bias) for attribute, count in
                   attribute_counts.items()} if objects_with_bias else {}
    general_bias_ratio = (objects_with_bias / total_objects) if total_objects else 0

    return attribute_counts, objects_with_bias, total_objects, bias_ratios, general_bias_ratio


# Initialize dictionaries to hold counts and results
all_results = {}
base_dir = "GPT_test_rm_bias"

# Loop through the file numbers, starting from 0 to 31
for i in range(32):  # 32 files, starting from index 0
    file_name = f'bias_info{i}.jsonl'
    file_path = base_dir + "/bias_info_files/" + file_name
    attribute_counts, objects_with_bias, total_objects, bias_ratios, general_bias_ratio = count_bias_attributes(
        file_path)

    # Calculate bias ratios for current file
    bias_ratios = {attribute: (count / objects_with_bias) for attribute, count in
                   attribute_counts.items()} if objects_with_bias else {}

    # Record the bias ratios with the file number as the key
    all_results[f'{i}'] = {
        'attribute_counts': attribute_counts,
        'objects_with_bias': objects_with_bias,
        'total_objects': total_objects,
        # 'bias_ratios': bias_ratios,
        # 'general_bias_ratio': general_bias_ratio
    }

# Write the aggregated results to a single file
output_file_path = base_dir + '/aggregated_bias_ratios_after.json'
with open(output_file_path, 'w') as output_file:
    json.dump(all_results, output_file, indent=4)

print(f"Aggregated bias ratios, including the general bias ratio, have been written to {output_file_path}.")
