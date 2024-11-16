import json
import file_source

def add_districts(data):
    # Known districts in Hong Kong
    known_districts = [
        "中環", "灣仔", "銅鑼灣", "尖沙咀", "西環", "上環", 
        "深水埗", "紅磡", "土瓜灣", "大角咀", "旺角", "油麻地",
        "佐敦", "北角", "太子", "天后", "西營盤", "筲箕灣",
        "黃大仙", "觀塘", "屯門", "元朗", "大圍", "西貢"
    ]
    
    def extract_district(address):
        # Try exact match at start of address
        for district in known_districts:
            if address.startswith(district):
                return district
        return "其他"  # Default if no match found
    
    # Add district to each restaurant
    for restaurant in data:
        restaurant["地區"] = extract_district(restaurant["地址"])
    
    return data

def main():
    # Read the original JSON file
    with open(file_source.restaurants(), 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add districts
    updated_data = add_districts(data)
    
    # Save to new file
    with open(file_source.restaurants_d_js(), 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)
    
    # Print some statistics
    districts = {}
    for restaurant in updated_data:
        district = restaurant["地區"]
        districts[district] = districts.get(district, 0) + 1
    
    print("\nDistrict distribution:")
    for district, count in sorted(districts.items()):
        print(f"{district}: {count} restaurants")

if __name__ == "__main__":
    main()