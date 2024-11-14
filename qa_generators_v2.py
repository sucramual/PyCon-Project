import json
import pandas as pd
from data_cleaning.split_data import split_data_sklearn


# To deprioritise used restaurants to ensure diversity
used_restaurants = set()

def get_similar_restaurants(
        train_df: pd.DataFrame,
        cuisine: str,
        target_restaurants: str,
        used_restaurants: set,
        num_examples: int = 2,
        iteration: int = 0,
        based_random_state: int = 42
):
    cuisine_df = train_df[train_df['菜式'] == cuisine].copy()
    cuisine_df = cuisine_df[cuisine_df["餐廳名稱"] != target_restaurants]

    if len(cuisine_df) == 0:
        return [] 

    cuisine_df['priority'] = cuisine_df["餐廳名稱"].apply(lambda x: 0 if x in used_restaurants else 1)
    random_state = iteration + based_random_state
    cuisine_df = cuisine_df.sample(frac=1, random_state=random_state)

    return cuisine_df.head(num_examples)[['餐廳名稱','描述']].to_dict('records')

def generate_context(
    train_df: pd.DataFrame,
    restaurant: pd.Series,
    used_restaurants: set,
    iteration: int = 0,
    random_state: int = 42
) -> str:
    
    similar_restaurants = get_similar_restaurants(
        train_df=train_df,
        cuisine=restaurant["菜式"],
        target_restaurants=restaurant["餐廳名稱"],
        used_restaurants=used_restaurants,
        iteration = iteration,
        based_random_state = random_state
    )

    used_restaurants.update(r["餐廳名稱"] for r in similar_restaurants)

    # Context Generation
    contex_parts = []
    for i, similar in enumerate(similar_restaurants):
        if similar["描述"]:
            contex_parts.append(
                f"Restaurant {i+1}: {similar['餐廳名稱']} // Description: {similar['描述']}"
            )
        
    return contex_parts

def retrieve_qa_pairs(
    train_df: pd.DataFrame,
    restaurant: pd.Series,
    used_restaurants: set,
    iteration: int = 0,
    random_state: int = 42
):
    """
    Look up similar pairs and based on given restaurant details

    Return: Tuple[Str, Str]
    """
    
    # Create qa pair
    context = generate_context(
        train_df=train_df,
        restaurant=restaurant,
        used_restaurants=used_restaurants,
        iteration=iteration,
        random_state=random_state
    )
    
    # Split context into examples if they exist
    example_1 = context[0] if len(context) > 0 else ""
    example_2 = context[1] if len(context) > 1 else ""

    return (example_1, example_2) 

def generate_qa_pairs(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame = None,
    random_state: int = 42,
    training_mode:str = "train",
    ):
    qa_pairs = []
    cuisine_iterations = {}
    if training_mode == "train":
        test_df = train_df

    for _, restaurant in test_df.iterrows():

        # Skip generating the row if description is empty
        if len(restaurant['描述']) == 0:
            continue
        cuisine = restaurant['菜式']
        area = restaurant["地區"]
        iteration = cuisine_iterations.get(cuisine, 0)
        
        example_1, example_2 = retrieve_qa_pairs(
            train_df=train_df,
            restaurant=restaurant,
            used_restaurants=used_restaurants,
            iteration=iteration,
            random_state=random_state
        )

        qa_pair = {
            'question': f"請你提供這個在於香港{area}的餐廳的描述: {restaurant['餐廳名稱']}, 這是一間{restaurant['菜式']}餐廳。",
            'example_1': example_1,
            'example_2': example_2,
            'answer': restaurant['描述']
        }

        qa_pairs.append(qa_pair)
        cuisine_iterations[cuisine] = iteration + 1

    return qa_pairs



if __name__ == "__main__":

    # Load Raw Files 
    df = pd.read_json("data/restaurants_d.json")
    df['菜式'] = df['菜式'].apply(lambda x: x.replace("時尚",""))
    train_df, test_df = split_data_sklearn(df)

    # Generate QA pairs for training data
    train_qa_pairs = generate_qa_pairs(train_df, training_mode="train")
    print(f"Number of training data:{len(train_qa_pairs)}")
    train_output_df = pd.DataFrame(train_qa_pairs)
    train_output_df.to_csv(
        'resto_new_train.csv',
        index=True,
        encoding='utf-8-sig'
    )

    # Generate QA Pairs for test data
    test_qa_pairs = generate_qa_pairs(train_df,test_df, training_mode="test")
    print(f"Number of training data:{len(test_qa_pairs)}")
    test_qa = pd.DataFrame(test_qa_pairs)
    test_qa.to_csv(
        'resto_new_test.csv',
        index=True,
        encoding="utf-8-sig"
    )

    # Print example
    print("\n=== Example QA Pair ===")
    example = train_qa_pairs[0]
    print(f"\nQuestion: {example['question']}")
    print(f"\nExample 1: {example['example_1']}")
    print(f"\nExample 2: {example['example_2']}")
    print(f"\nAnswer: {example['answer']}")