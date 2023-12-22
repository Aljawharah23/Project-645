import json
import random

# Load Bug Reports
def load_bug_reports(file_path):
    bug_reports = {}
    with open(file_path, 'r') as file:
        for line in file:
            report = json.loads(line.strip())
            key = report['key']
            text = report.get('title', '') + " " + report.get('description', '')
            bug_reports[key] = text
    return bug_reports


# Load Duplicate Bug Reports
def load_duplicates(file_path):
    with open(file_path, 'r') as file:
        duplicates = json.load(file)
    return duplicates


bug_reports = load_bug_reports('/home/aalmuhana/Desktop/replication_package/0_data/0_bug report collection/corpus and queries/accumulo/bug-reports.json')
duplicates = load_duplicates('/home/aalmuhana/Desktop/replication_package/outputs/GT_for_Placeholders/accumulo_GT_for_placeholders.json')

# Create Positive Pairs
positive_pairs = []
for key, dup_keys in duplicates.items():
    for dup_key in dup_keys:
        if key in bug_reports and dup_key in bug_reports:
            positive_pairs.append([key, dup_key, bug_reports[key], bug_reports[dup_key]])

# Create Negative Pairs
negative_pairs = []
all_report_ids = list(bug_reports.keys())
while len(negative_pairs) < len(positive_pairs):
    pair = random.sample(all_report_ids, 2)
    if pair[1] not in duplicates.get(pair[0], []) and pair[0] not in duplicates.get(pair[1], []):
        negative_pairs.append([pair[0], pair[1], bug_reports[pair[0]], bug_reports[pair[1]]])

# Save to JSON
with open('/home/aalmuhana/Desktop/replication_package/outputs/Postive-Negative-pairs/accumulo_positive_pairs.json', 'w') as file:

    json.dump(positive_pairs, file, indent=4)


with open('/home/aalmuhana/Desktop/replication_package/outputs/Postive-Negative-pairs/accumulo_negative_pairs.json', 'w') as file:

    json.dump(negative_pairs, file, indent=4)

print("Positive and negative pairs have been saved.")




