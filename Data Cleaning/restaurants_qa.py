import json
from typing import List, Dict
from collections import defaultdict
import file_source
import csv
import re

class RestaurantRecommender:
    def __init__(self, restaurants: List[Dict]):
        self.restaurants = restaurants
        # Create indexes for faster lookup
        self.district_cuisine_index = defaultdict(lambda: defaultdict(list))
        self.district_index = defaultdict(list)
        self.cuisine_index = defaultdict(list)
        
        for restaurant in restaurants:
            district = restaurant["地區"]
            cuisine = restaurant["菜式"]
            name = re.sub(r'\s*\([^)]*\)\s*$', '', restaurant["餐廳名稱"]).strip()
            restaurant["餐廳名稱"] = name

            # Index by district and cuisine
            self.district_cuisine_index[district][cuisine].append(restaurant)
            # Index by district
            self.district_index[district].append(restaurant)
            # Index By cuisine
            self.cuisine_index[cuisine].append(restaurant)

    def format_restaurant_info(self, restaurant: Dict) -> str:
        """Format restaurant information nicely"""
        stars = "米芝蓮一星" if restaurant["米芝蓮星星"] == 1 else \
                "米芝蓮二星" if restaurant["米芝蓮星星"] == 2 else \
                "米芝蓮三星" if restaurant["米芝蓮星星"] == 3 else \
                restaurant["推介"] if restaurant["推介"] != "No Distinction" else ""
        
        price = restaurant["價錢"]
        name = restaurant["餐廳名稱"]
        
        star_info = f"（{stars}）" if stars else ""
        price_info = f"（{price}）" if price else ""
        
        return f"{name}{star_info}{price_info}"
    
    def return_restaurant_name(self, restaurant: Dict) -> str:
        """Return restaurant name"""
        return restaurant["餐廳名稱"]

    def get_district_cuisine_recommendations(self, district: str, cuisine: str) -> str:
        """Generate answer for district + cuisine query"""
        restaurants = self.district_cuisine_index[district][cuisine]
        if not restaurants:
            return f"抱歉，{district}暫時未有{cuisine}推介。"
        
        restaurant_infos = [self.return_restaurant_name(r) for r in restaurants]
        return "、".join(restaurant_infos)

    def get_district_recommendations(self, district: str) -> str:
        """Generate answer for district-only query"""
        restaurants = self.district_index[district]
        if not restaurants:
            return f"抱歉，{district}暫時未有餐廳推介。"
        
        restaurant_infos = [self.return_restaurant_name(r) for r in restaurants]
        return "、".join(restaurant_infos)

    def get_star_cuisine_recommendations(self, stars: str, cuisine: str) -> str:
        """Generate answer for star rating + cuisine query
        Args:
            stars (str): '一星', '兩星', or '三星'
            cuisine (str): Type of cuisine
        """
        # Convert Chinese numbers to digits
        star_map = {'一星': 1, '兩星': 2, '三星': 3}
        star_count = star_map[stars]
        
        # Filter restaurants by stars and cuisine
        matching_restaurants = [
            r for r in self.restaurants 
            if r["米芝蓮星星"] == star_count and r["菜式"] == cuisine
        ]
        
        if not matching_restaurants:
            return f"抱歉，暫時未有{stars}嘅{cuisine}推介。"
        
        restaurant_infos = [self.return_restaurant_name(r) for r in matching_restaurants]
        return "、".join(restaurant_infos)

    def generate_cuisine_recommendations(self) -> List[Dict]:
        """Generate one Q&A pair for each restaurant"""
        qa_pairs = []
        
        # Loop through each restaurant
        for restaurant in self.restaurants:
            cuisine = restaurant["菜式"]
            name = restaurant["餐廳名稱"]
            description = restaurant.get('描述', '').strip()
            description_text = f"，呢間餐廳{description}。" if description else ""
            
            qa_pair = {
                "question": f"我想食{cuisine}，你有冇邊間推介呀？",
                "answer": f"你可以考慮吓{name}{description_text}。"
            }

            qa_pairs.append(qa_pair)
        
        return qa_pairs    
    
    def generate_qa_pairs(self):
        """Generate all possible Q&A pairs"""
        qa_pairs = []
        
        # Generate district + cuisine pairs
        for district in self.district_index.keys():
            for cuisine in set(r["菜式"] for r in self.district_index[district]):
                q = f"我想去{district}食{cuisine}，可以去邊食？"
                a = f"你可以去{self.get_district_cuisine_recommendations(district, cuisine)}。"
                qa_pairs.append({"question": q, "answer": a})
        
        # Generate district-only pairs
        for district in self.district_index.keys():
            q = f"我想去{district}食飯，可以去邊食？"
            a = f"你可以去{self.get_district_recommendations(district)}。"
            qa_pairs.append({"question": q, "answer": a})

        # Generate star rating + cuisine pairs
        star_ratings = ['一星', '兩星', '三星']
        cuisines = set(r["菜式"] for r in self.restaurants)
        for stars in star_ratings:
            for cuisine in cuisines:
                q = f"我想去{stars}嘅{cuisine}，有咩推介呀？"
                a = f"你可以去{self.get_star_cuisine_recommendations(stars, cuisine)}！"
                qa_pairs.append({"question": q, "answer": a})

        # Add individual restaurant recommendations
        cuisine_qa_pairs = self.generate_cuisine_recommendations()
        qa_pairs.extend(cuisine_qa_pairs)

        return qa_pairs
    
def main():
    # Read restaurant data
    with open(file_source.restaurants_d_js(), 'r', encoding='utf-8') as f:
        restaurants = json.load(f)
    
    # Create recommender
    recommender = RestaurantRecommender(restaurants)
    
    # Generate QA pairs
    qa_pairs = recommender.generate_qa_pairs()
    
    # Save to CSV file
    with open(file_source.qa_csv(), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['question', 'answer'])
        writer.writeheader()
        writer.writerows(qa_pairs)

    # Print some examples
    print("\nSample Q&A pairs:")
    for pair in qa_pairs[:1]:
        print(f"\nQ: {pair['question']}")
        print(f"A: {pair['answer']}")

if __name__ == "__main__":
    main()
    
    