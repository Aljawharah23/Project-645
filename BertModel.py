import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the SentenceBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to read multiple JSON objects from a file as strings
def read_json_objects_as_strings(file_path):
    json_strings = []
    with open(file_path, 'r') as file:
        for line in file:
            json_strings.append(line.strip())
    return json_strings

# Read JSON objects as strings
bug_reports = read_json_objects_as_strings('/home/aalmuhana/Desktop/replication_package/outputs/Preprocessed_Splitted_Bug-report/accumulo_preprocessed_20_data.json')
bug_report_ids = []
bug_report_texts = []

# Parse each JSON string and extract 'key' and 'text'
for json_str in bug_reports:
    try:
        report = json.loads(json_str)
        bug_report_ids.append(report["key"])
        bug_report_texts.append(report["text"])
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e} in string: {json_str}")

# Generate embeddings for each combined bug report text
embeddings = model.encode(bug_report_texts)

# Calculate the cosine similarity matrix
sim_matrix = cosine_similarity(embeddings)

# Create a dictionary for each bug report
bug_report_rankings = {
    bug_id: dict(sorted({bug_report_ids[j]: similarities[j] for j in range(len(bug_report_ids)) if i != j}.items(), key=lambda item: item[1], reverse=True))
    for i, bug_id in enumerate(bug_report_ids)
    for similarities in [sim_matrix[i]]
}
def read_ground_truth(file_path):
    with open(file_path, 'r') as gt_file:
        try:
            # Read the entire file as a single JSON object
            ground_truth_data = json.load(gt_file)
            return ground_truth_data
        except json.JSONDecodeError as e:
            print(f"Error parsing file as JSON: {e}")
            return {}

'''' قبل المشكله اوكي
def read_ground_truth(file_path):
    with open(file_path, 'r') as gt_file:
        # Initialize an empty dictionary to hold ground truth data
        ground_truth_data = {}

        for line in gt_file:
            try:
                # Remove any leading/trailing whitespace or commas
                line = line.strip().rstrip(',')

                # Check if the line is not empty
                if line:
                    # Parse the line as JSON and update the ground truth data
                    line_data = json.loads('{' + line + '}')
                    ground_truth_data.update(line_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing line as JSON: {e} in line: {line}")

        return ground_truth_data
'''
# Read ground truth data

ground_truth_data = read_ground_truth('/home/aalmuhana/Desktop/replication_package/outputs/GT_for_Placeholders/accumulo_GT_for_placeholders.json')

# Define evaluation metric functions

def mean_reciprocal_rank(rs):
    rs = (np.asarray(r).nonzero()[0] for r in rs)
    return np.mean([1. / (r[0] + 1) if r.size else 0. for r in rs])

def average_precision(r):
    r = np.asarray(r) != 0
    out = [precision_at_k(r, k + 1) for k in range(r.size) if r[k]]
    if not out:
        return 0.
    return np.mean(out)

def precision_at_k(r, k):
    assert k >= 1
    r = np.asarray(r)[:k] != 0
    return np.mean(r)

def mean_average_precision(rs):
    return np.mean([average_precision(r) for r in rs])

def dcg_at_k(r, k, method=0):
    r = np.asfarray(r)[:k]
    if r.size:
        if method == 0:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        elif method == 1:
            return np.sum(r / np.log2(np.arange(2, r.size + 2)))
    return 0.

'''def ndcg_at_k(r, k, method=0):
    dcg_max = dcg_at_k(sorted(r, reverse=True), k, method)
    if not dcg_max:
        return 0.
    return dcg_at_k(r, k, method) / dcg_max'''
    
def ndcg_at_k(r, k, method=0):
    ndcg_scores = []
    for rel_list in r:
        dcg_max = dcg_at_k(sorted(rel_list, reverse=True), k, method)
        if not dcg_max:
            ndcg_scores.append(0.)
        else:
            dcg_score = dcg_at_k(rel_list, k, method)
            ndcg_scores.append(dcg_score / dcg_max)
    return np.mean(ndcg_scores)


# Prepare the relevance lists for each bug report
k = 5  
relevance_lists = []
for bug_id in bug_report_ids:
    rankings = bug_report_rankings.get(bug_id, {})
    top_k_ranked_ids = list(rankings.keys())[:k]
    relevance_list = [1 if id in ground_truth_data.get(bug_id, []) else 0 for id in top_k_ranked_ids]
    relevance_lists.append(relevance_list)

    # Debugging: Check the length of each sublist
    if len(relevance_list) != k:
        print(f"Relevance list for {bug_id} has a length of {len(relevance_list)}, expected {k}")

# Debugging: Print the relevance lists
print("Relevance Lists:", relevance_lists)

# Calculate evaluation metrics
try:
    mrr = mean_reciprocal_rank(relevance_lists)
    print(f"Mean Reciprocal Rank: {mrr}")
    map_score = mean_average_precision(relevance_lists)
    ndcg = ndcg_at_k(relevance_lists, k)
    
    #print(f"Mean Reciprocal Rank: {mrr}")
    print(f"Mean Average Precision: {map_score}")
    print(f"NDCG@K: {ndcg}")
except Exception as e:
    print(f"Error in calculating metrics: {e}")

# Prepare the text to be saved
evaluation_metrics_text = (
    f"Mean Reciprocal Rank: {mrr}\n"
    f"Mean Average Precision: {map_score}\n"
    f"NDCG@K: {ndcg}\n"
)

#  output file path
evaluation_metrics_output_file_path = '/home/aalmuhana/Desktop/replication_package/outputs/EvaluationMetricsOutput/accumulo_EvaluationMetricsOutput.txt'  

# Save the evaluation metrics to file
with open(evaluation_metrics_output_file_path, 'w') as file:
    file.write(evaluation_metrics_text)

print(f"Evaluation metrics saved to {evaluation_metrics_output_file_path}")




# Prepare the dictionary for JSON output
relevance_dict = {bug_id: relevance_list for bug_id, relevance_list in zip(bug_report_ids, relevance_lists)}

# Manually format the JSON output
relevance_json_parts = []
for bug_id, relevance_list in relevance_dict.items():
    relevance_list_str = ','.join(map(str, relevance_list))
    relevance_json_parts.append(f'"{bug_id}": [{relevance_list_str}]')

formatted_relevance_json = "{\n    " + ",\n    ".join(relevance_json_parts) + "\n}"

#  output file path for relevance lists
relevance_output_file_path = '/home/aalmuhana/Desktop/replication_package/outputs/relevance_lists_output/accumulo_RelevanceLists.json'  # Update file path

# Save the formatted relevance lists to the output file
with open(relevance_output_file_path, 'w') as file:
    file.write(formatted_relevance_json)  # Make sure to use 'formatted_relevance_json' here

print(f"Relevance lists saved to {relevance_output_file_path}")

#  output file path 
output_file_path = '/home/aalmuhana/Desktop/replication_package/outputs/Rankings_lists_output/accumulo_Ranking_output.txt' 

# Save the similarity rankings to the output file
with open(output_file_path, 'w') as file:
    for bug_id, rankings in bug_report_rankings.items():
        file.write(f"Rankings for Bug Report {bug_id}:\n")
        for ranked_bug_id, similarity_score in rankings.items():
            file.write(f"{ranked_bug_id}: {similarity_score}\n")
        file.write("\n")  # Add a new line for readability

print(f"Rankings saved to {output_file_path}")


