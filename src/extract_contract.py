import json
import os

# Paths
file_path = "data/cuad/train_separate_questions.json"
output_dir = "data/cuad"
output_file = os.path.join(output_dir, "contracts.txt")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Open JSON file and extract contracts
contract_count = 0

with open(file_path, "r") as file, open(output_file, "w", encoding="utf-8") as out_file:
    data = json.load(file)  # Load JSON

    if "data" in data and isinstance(data["data"], list):
        for entry in data["data"]:  # Iterate over contracts
            if "paragraphs" in entry and isinstance(entry["paragraphs"], list):
                for paragraph in entry["paragraphs"]:  # Iterate over paragraphs
                    if "qas" in paragraph and isinstance(paragraph["qas"], list):
                        for qa in paragraph["qas"]:  # Iterate over Q&A pairs
                            if "answers" in qa and isinstance(qa["answers"], list):
                                for answer in qa["answers"]:  # Extract contract text
                                    if "text" in answer:
                                        contract_text = answer["text"]
                                        out_file.write(contract_text + "\n\n")
                                        contract_count += 1

print(f"Extracted {contract_count} contract sections and saved them to '{output_file}'.")
