
import json
import random

# Load bug reports
def load_bug_reports(file_path):
    with open(file_path, 'r') as file:
        bug_reports = {}
        for line in file:
            try:
                report = json.loads(line)
                bug_reports[report['key']] = report
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        return bug_reports

# Load duplicates and group with originals
def group_reports_with_duplicates(file_path, bug_reports):
    grouped_reports = {}
    with open(file_path, 'r') as file:
        for line in file:
            try:
                duplicate_data = json.loads(line)
                original_key = duplicate_data['key']
                duplicates = duplicate_data['duplicateBugs']
                if original_key not in grouped_reports:
                    grouped_reports[original_key] = [original_key] + duplicates
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return grouped_reports

# Split data into training and testing sets
def split_data(bug_reports, grouped_reports, split_ratio=0.8):
    all_keys = list(bug_reports.keys())
    random.shuffle(all_keys)
    
    train_set, test_set = [], []
    used_keys = set()

    for key in all_keys:
        if key in used_keys:
            continue

        if random.random() < split_ratio:  # Add to training set
            train_set.append(bug_reports[key])
            used_keys.add(key)
            if key in grouped_reports:
                for dup_key in grouped_reports[key]:
                    if dup_key in bug_reports:
                        train_set.append(bug_reports[dup_key])
                        used_keys.add(dup_key)
        else:  # Add to testing set
            test_set.append(bug_reports[key])
            used_keys.add(key)
            if key in grouped_reports:
                for dup_key in grouped_reports[key]:
                    if dup_key in bug_reports:
                        test_set.append(bug_reports[dup_key])
                        used_keys.add(dup_key)

    return train_set, test_set

# Save to JSON
def save_to_json(data, file_path):
    with open(file_path, 'w') as file:
        for report in data:
            json.dump(report, file)
            file.write('\n')

# File paths
bug_reports_file = '/home/aalmuhana/Desktop/replication_package/0_data/0_bug report collection/corpus and queries/accumulo/bug-reports.json'
duplicates_file = '/home/aalmuhana/Desktop/replication_package/0_data/0_bug report collection/corpus and queries/accumulo/dup-bug-report-queries.json'


# Load data
bug_reports = load_bug_reports(bug_reports_file)
grouped_reports = group_reports_with_duplicates(duplicates_file, bug_reports)

# Split data
train_reports, test_reports = split_data(bug_reports, grouped_reports)

# Save split data
save_to_json(train_reports, '/home/aalmuhana/Desktop/replication_package/outputs/Splitted_Bug_Reports_20_80/accumulo_primary_80_reports.json')
save_to_json(test_reports, '/home/aalmuhana/Desktop/replication_package/outputs/Splitted_Bug_Reports_20_80/accumulo_secondary_20_reports.json')



