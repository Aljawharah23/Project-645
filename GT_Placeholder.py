import json

# Read bug report data
bug_report_data = []
with open('/home/aalmuhana/Desktop/replication_package/0_data/0_bug report collection/corpus and queries/accumulo/bug-reports.json', 'r') as bug_reports_json:
    for line in bug_reports_json:
        bug_data = json.loads(line.strip())
        key = bug_data['key']
        bug_report_data.append(key)

# Read ground truth data
ground_truth_dict = {}
with open('/home/aalmuhana/Desktop/replication_package/0_data/0_bug report collection/corpus and queries/accumulo/dup-bug-report-queries.json', 'r') as ground_truth_json:
    for line in ground_truth_json:
        ground_truth = json.loads(line.strip())
        key = ground_truth['key']
        duplicates = ground_truth['duplicateBugs']
        if duplicates:
            ground_truth_dict[key] = duplicates

# Create the output file
output_file_path = '/home/aalmuhana/Desktop/replication_package/outputs/GT_for_Placeholders/accumulo_GT_for_placeholders.json'

# Format bug report data with duplicates
formatted_bug_data = {}
for key in bug_report_data:
    duplicates = ground_truth_dict.get(key, [])
    formatted_bug_data[key] = duplicates

# Write the formatted data to the output file
with open(output_file_path, 'w') as output_json_file:
    json.dump(formatted_bug_data, output_json_file, indent=4)

print(f"Formatted data saved as JSON object to {output_file_path}")
