

import json
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.spatial.distance import cosine

# Function to load data from a JSON file
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to load and combine positive and negative pairs
def load_and_combine_pairs(positive_pairs_path, negative_pairs_path):
    positive_pairs = load_data(positive_pairs_path)
    negative_pairs = load_data(negative_pairs_path)
    return positive_pairs + negative_pairs

# Function to evaluate the model and save results
def evaluate_model(model, pairs, reports_dict, pair_results_file, metrics_results_file):
    predictions, labels = [], []

    with open(pair_results_file, 'w') as pair_file:
        for pair in pairs:
            key1, key2, text1, text2 = pair
            embedding1 = model.encode(text1, convert_to_tensor=True)
            embedding2 = model.encode(text2, convert_to_tensor=True)

            # Calculate cosine similarity
            cosine_score = 1 - cosine(embedding1.cpu().numpy(), embedding2.cpu().numpy())

            # Determine if this is a duplicate or not
            is_duplicate = key2 in reports_dict.get(key1, [])
            label = 1 if is_duplicate else 0

            predictions.append(cosine_score)
            labels.append(label)

            pair_file.write(f"Pair: ({key1}, {key2}), Cosine Score: {cosine_score}, Label: {label}\n")

    accuracy = accuracy_score(labels, [1 if x > 0.5 else 0 for x in predictions])
    precision = precision_score(labels, [1 if x > 0.5 else 0 for x in predictions])
    recall = recall_score(labels, [1 if x > 0.5 else 0 for x in predictions])
    f1 = f1_score(labels, [1 if x > 0.5 else 0 for x in predictions])

    # Save metrics results to a file
    with open(metrics_results_file, 'w') as metrics_file:
        metrics_file.write(f"Accuracy: {accuracy}\n")
        metrics_file.write(f"Precision: {precision}\n")
        metrics_file.write(f"Recall: {recall}\n")
        metrics_file.write(f"F1 Score: {f1}\n")

    return accuracy, precision, recall, f1

# Load the fine-tuned model

model = SentenceTransformer('/home/aalmuhana/Desktop/replication_package/outputs/Fine_Tune_Models/accumulo_fine_tuned_model')

# Load test pairs (positive and negative)
test_pairs = load_and_combine_pairs('/home/aalmuhana/Desktop/replication_package/outputs/Postive-Negative-pairs/accumulo_positive_pairs.json', 
                                    '/home/aalmuhana/Desktop/replication_package/outputs/Postive-Negative-pairs/accumulo_negative_pairs.json')

# Load your mapping of bug reports to their duplicates
duplicates_mapping = load_data('/home/aalmuhana/Desktop/replication_package/outputs/GT_for_Placeholders/accumulo_GT_for_placeholders.json')


# Files to save results
pair_results_file =  '/home/aalmuhana/Desktop/replication_package/outputs/Fine_Tuned_NP_output/accumulo_pair_results.txt'

metrics_results_file = '/home/aalmuhana/Desktop/replication_package/outputs/Fine_Tuned_NP_output/accumulo_metrics_results.txt'

# Evaluate the model and save results
accuracy, precision, recall, f1 = evaluate_model(model, test_pairs, duplicates_mapping, pair_results_file, metrics_results_file)
print(f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")










