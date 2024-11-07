import json
import pandas as pd
import random
from collections import defaultdict
from typing import List, Dict, Optional
from pathlib import Path

class RestaurantManager:
    def __init__(self, restaurants: List[Dict]):
        self.restaurants = restaurants

        # Index for faster lookup
        self.district_cuisine_index = defaultdict(lambda: defaultdict(list))
        self.district_index = defaultdict(list)
        self.cuisine_index = defaultdict(list)
        self._build_indexes()
    
    def _build_indexes(self) -> None:
        """Build search indexes for restaurants"""
        for restaurant in self.restaurants:
            district = restaurant["地區"]
            cuisine = restaurant["菜式"]
            
            # Index by district and cuisine
            self.district_cuisine_index[district][cuisine].append(restaurant)
            # Index by district
            self.district_index[district].append(restaurant)
            # Index by cuisine
            self.cuisine_index[cuisine].append(restaurant)
    
    def format_restaurant_info(self, restaurant: Dict) -> str:
        """Format restaurant information for display"""
        stars = "米芝蓮一星" if restaurant["米芝蓮星星"] == 1 else \
                "米芝蓮二星" if restaurant["米芝蓮星星"] == 2 else \
                "米芝蓮三星" if restaurant["米芝蓮星星"] == 3 else \
                restaurant["推介"] if restaurant["推介"] != "No Distinction" else ""
        
        price = restaurant["價錢"]
        name = restaurant["餐廳名稱"]
        
        star_info = f"（{stars}）" if stars else ""
        price_info = f"（{price}）" if price else ""
        
        return f"{name}{star_info}{price_info}"

    def get_restaurants_by_district_cuisine(self, district: str, cuisine: str) -> List[Dict]:
        """Get restaurants in a district with specific cuisine"""
        return self.district_cuisine_index[district][cuisine]

    def get_restaurants_by_district(self, district: str) -> List[Dict]:
        """Get all restaurants in a district"""
        return self.district_index[district]

    def create_recommendation(self, restaurant: Dict) -> Dict:
        """Create a formatted recommendation for a restaurant."""
        return {
            'cuisine_type': restaurant['菜式'],
            'question': f'我想食{restaurant["菜式"]}，你有冇邊間推介呀？',
            'answer': f'你可以考慮吓{restaurant["餐廳名稱"]}，呢間餐廳{restaurant["描述"]}',
            'restaurant_name': restaurant['餐廳名稱'],
            'michelin_stars': restaurant['米芝蓮星星'],
            'distinction': restaurant['推介'],
            'price_range': restaurant['價錢'],
            'address': restaurant['地址']
        }

    def get_cuisine_recommendations(self) -> pd.DataFrame:
        """Generate recommendations dataframe from restaurant list."""
        df = pd.DataFrame(self.restaurants)
        recommendations = []
        
        for cuisine_type, group in df.groupby('菜式'):
            # Prioritize starred or Bib Gourmand restaurants
            starred = group[
                (group['米芝蓮星星'] != "No Award") | 
                (group['推介'] == "必比登")
            ]
            
            # If no starred restaurants, use all restaurants
            selection_group = starred if not starred.empty else group
            
            # Randomly select one restaurant
            selected = selection_group.iloc[random.randint(0, len(selection_group)-1)]
            recommendations.append(self.create_recommendation(selected.to_dict()))
        
        return pd.DataFrame(recommendations)

    def generate_location_qa_pairs(self) -> List[Dict]:
        """Generate Q&A pairs for location-based queries"""
        qa_pairs = []
        
        # District + cuisine pairs
        for district in self.district_index.keys():
            for cuisine in set(r["菜式"] for r in self.district_index[district]):
                restaurants = self.get_restaurants_by_district_cuisine(district, cuisine)
                if restaurants:
                    formatted_restaurants = [self.format_restaurant_info(r) for r in restaurants]
                    qa_pairs.append({
                        "question": f"我想去{district}食{cuisine}，可以去邊食呀？",
                        "answer": f"你可以去{('、').join(formatted_restaurants)}"
                    })
        
        # District-only pairs
        for district in self.district_index.keys():
            restaurants = self.get_restaurants_by_district(district)
            if restaurants:
                formatted_restaurants = [self.format_restaurant_info(r) for r in restaurants]
                qa_pairs.append({
                    "question": f"我想去{district}食飯，可以去邊食？",
                    "answer": f"你可以去{('、').join(formatted_restaurants)}"
                })
        
        return qa_pairs

    @classmethod
    def from_json(cls, filepath: str) -> 'RestaurantManager':
        """Create RestaurantManager from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(data)

    def save_recommendations(self, csv_filepath: str, qa_filepath: str) -> None:
        """Save both cuisine recommendations and location QA pairs"""
        # Save cuisine recommendations
        recommendations_df = self.get_cuisine_recommendations()
        recommendations_df.to_csv(csv_filepath, index=False)
        
        # Save location QA pairs
        qa_pairs = self.generate_location_qa_pairs()
        with open(qa_filepath, 'w', encoding='utf-8') as f:
            json.dump(qa_pairs, f, ensure_ascii=False, indent=2)

def main():
    # Create manager from JSON
    current_dir = Path(__file__).resolve().parent
    json_path = current_dir.parent / 'data' / 'restaurants_d.json'
    manager = RestaurantManager.from_json(json_path)
    
    # Generate and save both types of recommendations
    manager.save_recommendations(
        csv_filepath='restaurant_recommendations.csv',
        qa_filepath='restaurant_qa.json'
    )
    
    # Print some statistics
    recommendations_df = manager.get_cuisine_recommendations()
    print(f"\nTotal number of cuisine types: {len(recommendations_df)}")
    
    # Print example cuisine recommendations
    print("\nExample cuisine recommendations (first 3):")
    for _, row in recommendations_df.head(3).iterrows():
        print(f"\nCuisine: {row['cuisine_type']}")
        print(f"Q: {row['question']}")
        print(f"A: {row['answer']}")
        print(f"Restaurant: {row['restaurant_name']}")
        print(f"Michelin Stars: {row['michelin_stars']}")
        print(f"Distinction: {row['distinction']}")
        print(f"Price Range: {row['price_range']}")
        print(f"Address: {row['address']}")
    
    # Print example location recommendations
    print("\nExample location recommendations:")
    central_restaurants = manager.get_restaurants_by_district("中環")
    print("\nRestaurants in 中環:")
    for restaurant in central_restaurants[:3]:  # First 3 only
        print(manager.format_restaurant_info(restaurant))

if __name__ == "__main__":
    main()