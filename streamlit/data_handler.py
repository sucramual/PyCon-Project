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
        questions_df = pd.read_csv(path("testset_questions_chinese.csv"))
        model_answers = {
            'GPT-4o': pd.read_csv(path("gpt4o.csv")),
            'Qwen25-3B': pd.read_csv(path("Qwen25-3B.csv")),
            'Qwen25-0.5B': pd.read_csv(path("Qwen25-05B.csv")),
            'Qwen25-1.5B': pd.read_csv(path("Qwen25-15B.csv"))
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
