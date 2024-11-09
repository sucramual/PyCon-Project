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

# Method 1: Using scikit-learn (Recommended)
def split_data_sklearn(df, test_size=0.2, random_state=42):
    """
    Split a DataFrame into train and test sets using scikit-learn.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame to split
    test_size : float, default=0.2
        Proportion of the dataset to include in the test split
    random_state : int, default=42
        Random seed for reproducibility
        
    Returns:
    --------
    train_df : pandas.DataFrame
        Training dataset
    test_df : pandas.DataFrame
        Test dataset
    """
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state
    )
    
    # Reset indices for both datasets
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)
    
    print(f"Training set size: {len(train_df)} ({(1-test_size)*100}%)")
    print(f"Test set size: {len(test_df)} ({test_size*100}%)")
    
    return train_df, test_df

if __name__ == "__main__":
    process_data()