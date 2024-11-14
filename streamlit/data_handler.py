# data_handler.py
"""Data loading and processing functions"""
import pandas as pd
import streamlit as st
from typing import Tuple, Dict
from pathlib import Path

def path(file):
    return Path(__file__).resolve().parent.parent / 'data' / 'q_and_a' / file

@st.cache_data
def load_data() -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Load questions and model answers from CSV files.
    Uses st.cache_data to prevent reloading on every rerun.
    """
    try:
        questions_df = pd.read_csv(path("testset_questions_only.csv"))
        model_answers = {
            'GPT-4o': pd.read_csv(path("gpt4o.csv")),
            'Model-1': pd.read_csv(path("sm_1_qa.csv")),
            'Model-2': pd.read_csv(path("sm_2_qa.csv")),
            'Model-3': pd.read_csv(path("sm_3_qa.csv"))
        }
        return questions_df, model_answers
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

def get_answers_for_question(
    question_idx: int,
    model_answers: Dict[str, pd.DataFrame]
) -> Dict[str, str]:
    """
    Retrieve answers from all models for a specific question.
    """
    return {
        model: df.loc[question_idx, 'Answers']
        for model, df in model_answers.items()
    }
