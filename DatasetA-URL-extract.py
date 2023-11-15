import pandas as pd
import requests
import re
from urllib3.exceptions import LocationParseError


# Function to find URLs in a text
def find_urls(text):
    if not isinstance(text, str):
        return []
    url_pattern = re.compile(r'https?://[^\s\[\],;()<>]+(?:\.\w{2,})+')
    return url_pattern.findall(text)


# Function to check if a URL is valid and categorize it
def categorize_url(url):
    try:
        response = requests.get(url, stream=True, timeout=10)
        content_type = response.headers.get('Content-Type', '')

        if 'image' in content_type:
            return 'image'
        elif 'video' in content_type:
            return 'video'
        else:
            return 'other working'  # Other working URLs
    except (requests.RequestException, LocationParseError):
        return 'not working'  # Not working URLs

# Function to process bug reports for a system
def process_bug_reports_for_system(system_name, base_input_path, base_output_path):
    file_path = f'{base_input_path}/N_bug_reports_{system_name}.xlsx'
    output_path = f'{base_output_path}/URL_BRs_{system_name}.xlsx'

    df = pd.read_excel(file_path)
    df['Image URLs'] = ''
    df['Video URLs'] = ''
    df['Other Working URLs'] = ''
    df['Not Working URLs'] = ''
    df['Total URLs'] = 0

    category_counts = {'image': 0, 'video': 0, 'other working': 0, 'not working': 0, 'total_bug_reports': 0}

    for index, row in df.iterrows():
        description = row.get('description', '')
        urls = find_urls(description)

        url_counts = {'image': [], 'video': [], 'other working': [], 'not working': []}

        for url in urls:
            category = categorize_url(url)
            url_counts[category].append(url)
            category_counts[category] += 1

        df.at[index, 'Image URLs'] = '\n'.join(url_counts['image'])
        df.at[index, 'Video URLs'] = '\n'.join(url_counts['video'])
        df.at[index, 'Other Working URLs'] = '\n'.join(url_counts['other working'])
        df.at[index, 'Not Working URLs'] = '\n'.join(url_counts['not working'])
        df.at[index, 'Total URLs'] = len(urls)

        category_counts['total_bug_reports'] += 1  # Counting total bug reports

    df.to_excel(output_path, index=False)
    return category_counts

# Base paths for input and output directories
base_input_path = '/home/aalmuhana/Documents/replication_package/Bug-reports-Output/'
base_output_path = '/home/aalmuhana/Documents/replication_package/Bug-reports-Output/'

# List of system names to be processed
systems = [ 'accumulo',  'ambari', 'amq', 'cassandra', 'cb',  'continuum', 'drill', 'groovy', 'hadoop', 'hbase', 'hive', 'eclipse', 'mng', 'mozilla', 'myfaces', 
 'pdfbox', 'openoffice', 'wicket', 'ww' #,'spark'
          ]  

# Process bug reports for each system and print summary
for system in systems:
    counts = process_bug_reports_for_system(system, base_input_path, base_output_path)
    print(f"Processed {system} successfully.")
    print(f"Total Bug Reports: {counts['total_bug_reports']}")
    print(f"Total Image URLs: {counts['image']}")
    print(f"Total Video URLs: {counts['video']}")
    print(f"Total Other Working URLs: {counts['other working']}")
    print(f"Total Not Working URLs: {counts['not working']}")
