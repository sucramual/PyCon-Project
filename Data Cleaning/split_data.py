import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from pathlib import Path

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

def process_data():
    # Read the original CSV
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parent 
    file_path = parent_dir / 'restaurants_qa.csv'
    df = pd.read_csv(file_path)
    
    # Add ID column
    df['id'] = range(1, len(df) + 1)
    
    # Reorder columns to put ID first
    df = df[['id', 'question', 'answer']]
    
    # Split data into training (80%) and testing (20%)
    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=RANDOM_SEED,
        shuffle=True
    )

    # Create test questions only dataframe
    test_questions_df = test_df[['id', 'question']]

    # Sort all dataframes by id and reset index
    train_df = train_df.sort_values('id')
    test_df = test_df.sort_values('id')
    test_questions_df = test_questions_df.sort_values('id')

    # Save files
    train_df.to_csv(parent_dir/'train.csv', index=False)
    test_df.to_csv(parent_dir/'test_with_answers.csv', index=False)
    test_questions_df.to_csv(parent_dir/'test_questions.csv', index=False)
    
    # Print statistics
    print(f"Total records: {len(df)}")
    print(f"Training records: {len(train_df)}")
    print(f"Testing records: {len(test_df)}")

if __name__ == "__main__":
    process_data()