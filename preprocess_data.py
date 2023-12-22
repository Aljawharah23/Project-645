import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import json

# Download required NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize the lemmatizer and stopwords list
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove special characters and line breaks
    text = re.sub(r'\W', ' ', text)   
    text = re.sub(r'\s+', ' ', text)  

    # Tokenize and remove stopwords
    words = text.split()
    words = [word for word in words if word not in stop_words]

    # Lemmatize each word
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

    # Re-join words into a single string
    cleaned_text = ' '.join(lemmatized_words)

    return cleaned_text
def read_json_objects(file_path):
    bug_reports = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                report = json.loads(line)
                bug_reports.append(report)
            except json.JSONDecodeError as e:
                print(f"Error reading JSON from line: {e}")
    return bug_reports
def preprocess_and_save(file_path, output_file_path):
    bug_reports = read_json_objects(file_path)
    preprocessed_reports = []

    for report in bug_reports:
        title = report.get('title', '')
        description = report.get('description', '')
        combined_text = title + ' ' + description
        preprocessed_text = preprocess_text(combined_text)
        preprocessed_reports.append({
            "key": report["key"],
            "text": preprocessed_text
        })

    # Saving the preprocessed data
    with open(output_file_path, 'w') as outfile:
      for report in preprocessed_reports:
          json.dump(report, outfile)
          outfile.write('\n')  



# Paths to original data files
file_path_80 = '/home/aalmuhana/Desktop/replication_package/outputs/Splitted_Bug_Reports_20_80/accumulo_primary_80_reports.json'
file_path_20 = '/home/aalmuhana/Desktop/replication_package/outputs/Splitted_Bug_Reports_20_80/accumulo_secondary_20_reports.json'
#file_path_GT=  '/home/aalmuhana/Desktop/replication_package/0_data/0_bug report collection/corpus and queries/accumulo/dup-bug-report-queries.json'

output_file_path_80 = '/home/aalmuhana/Desktop/replication_package/outputs/Preprocessed_Splitted_Bug-report/accumulo_preprocessed_80_data.json'
output_file_path_20 = '/home/aalmuhana/Desktop/replication_package/outputs/Preprocessed_Splitted_Bug-report/accumulo_preprocessed_20_data.json'
#output_file_path_GT= '/home/aalmuhana/Desktop/replication_package/outputs/Preprocessed_Splitted_Bug-report/Accumulo_preprocessed_GT_data.json'


preprocess_and_save(file_path_80, output_file_path_80)
preprocess_and_save(file_path_20, output_file_path_20)
#preprocess_and_save(file_path_GT, output_file_path_GT)
