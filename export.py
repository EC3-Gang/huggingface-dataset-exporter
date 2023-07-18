# Required Libraries
import argparse
from datasets import load_dataset
import json

# Initialize the ArgParse Parser
parser = argparse.ArgumentParser(description='Export a selected Hugging Face dataset as JSON.')

# Add all of your arguments
parser.add_argument('-d', '--dataset', required=True, help='Name of the Hugging Face dataset to load.')
parser.add_argument('-f', '--fields', required=True, help='Fields you would like to include in the export (comma separated).')
parser.add_argument('-o', '--output', required=True, help='Name of the output JSON file.')
parser.add_argument('-s', '--subset', required=False, default='train', help='Subset of the dataset to export (default: %(default)s).')
parser.add_argument('-l', '--lines', required=False, default=False, type=bool, help='Whether or not to export the dataset as JSONLINES')

# Parse the arguments
args = parser.parse_args()

# Load the dataset
dataset = load_dataset(args.dataset)

# Clean and split input fields string into a list
selected_fields = [field.strip() for field in args.fields.split(',')]

# Ensure that user-entered fields exist in the dataset
wrong_fields = [field for field in selected_fields if field not in dataset[args.subset].features.keys()]

if wrong_fields:
    raise ValueError(f"Fields {wrong_fields} don't exist in the dataset.")
else:
    json_export = []

    # Filter dataset for selected fields and export to JSON
    selected_dataset = dataset[args.subset]
    for data in selected_dataset:
        export_data = {field:data[field] for field in selected_fields if field in data}
        json_export.append(export_data)
    if args.lines:
        with open(f'{args.output}.jsonl', 'w') as json_file:
            json.dump(json_export, json_file, lines=True)
            print(f"Dataset exported successfully as '{args.output}.jsonl'")

    else:
        with open(f'{args.output}.json', 'w') as json_file:
            json.dump(json_export, json_file)
            print(f"Dataset exported successfully as '{args.output}.json'")

    
