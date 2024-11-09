from pathlib import Path

def restaurants():
    current_dir = Path(__file__).resolve().parent
    json_path = current_dir.parent / 'data' / 'restaurants.json'
    return json_path

def restaurants_d_js():
    current_dir = Path(__file__).resolve().parent
    json_path = current_dir.parent / 'data' / 'restaurants_d.json'
    return json_path

def qa_csv():
    current_dir = Path(__file__).resolve().parent
    csv_path = current_dir.parent / 'data' / 'restaurants_qa.csv'
    return csv_path