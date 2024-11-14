import json
import pandas as pd
from pathlib import Path
from typing import List, Dict
from pathlib import Path

def read_jsonl(file_path: str) -> List[Dict]:
    """Read JSONL file and return list of dictionaries"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def transform_data(data: List[Dict]) -> pd.DataFrame:
    """Transform data to match target CSV format"""
    transformed = []
    for item in data:
        transformed.append({
            'id': item['id'],
            'question': extract_question(item['prompt']),
            'Answers': item['prediction'],
        })
    return pd.DataFrame(transformed)

def extract_question(prompt: str) -> str:
    """Extract the core question from the prompt"""
    # Split by first occurrence of 'Restaurant' if it exists
    parts = prompt.split('Restaurant 1:')
    base_prompt = parts[0].strip()
    
    # Extract the question part between the description request
    if '請你提供' in base_prompt:
        # Extract the restaurant name and type
        start_idx = base_prompt.find('請你提供')
        end_idx = base_prompt.find('用廣東話回答')
        if end_idx == -1:  # If not found, take until the end
            end_idx = len(base_prompt)
        
        question_text = base_prompt[start_idx:end_idx].strip()
        # Convert to English format matching target CSV
        restaurant_info = question_text.split(',')
        if len(restaurant_info) >= 2:
            restaurant_name = restaurant_info[0].split(':')[-1].strip()
            restaurant_type = restaurant_info[1].split('這是一間')[-1].split("餐廳")[0].strip()
            return f"你可唔可以俾個有關{restaurant_name}嘅解釋我？佢係間{restaurant_type}嚟。"
    
    return base_prompt  # Fallback to returning the original prompt

def main():
    # Input and output paths
    input_files = [
        "qwen25-3B-finetuned-sample-output.jsonl",
        "Qwen25-05B_sample_output.jsonl",
        "Qwen25-15B_sample_output.jsonl"
    ]

    for input_file in input_files:
        output_file = Path(__file__).resolve().parent.parent / 'q_and_a' / f"{input_file.split('_')[0]}.csv"
        
        # Read and transform data
        data = read_jsonl(input_file)
        df = transform_data(data)
        
        # Save to CSV with UTF-8-SIG encoding to handle Chinese characters
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Successfully converted {len(df)} records to {output_file}")

if __name__ == "__main__":
    main()