"""Session state management"""
import streamlit as st
from config import INITIAL_STATE, MODELS

def initialize_session_state():
    """Initialize or reset session state variables"""
    for key, value in INITIAL_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value

def update_scores(correct_models: list, user_selections: list):
    """Update scores based on user selections"""
    st.session_state.total_attempts += 1
    
    for model, selection in zip(correct_models, user_selections):
        if model == selection:
            st.session_state.scores[model] += 1

def reset_submission_state():
    """Reset submission state"""
    st.session_state.submitted = False
    