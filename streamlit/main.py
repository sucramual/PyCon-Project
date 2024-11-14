# main.py
"""Main application file"""
import streamlit as st
import random
from config import PAGE_CONFIG
from data_handler import load_data, get_answers_for_question
from state_manager import initialize_session_state, update_scores, reset_submission_state
from ui_components import (
    render_header,
    render_metrics,
    render_answer_sections,
    render_control_buttons
)

def main():    
    # Configure page
    st.set_page_config(**PAGE_CONFIG)
    
    # Initialize session state
    initialize_session_state()
    
    # Load data
    questions_df, model_answers = load_data()
    if questions_df is None or model_answers is None:
        return
    
    # Render UI components
    render_header()
    render_metrics()
    
    # Add some spacing
    st.markdown("---")
    
    # Question selection
    selected_question = st.selectbox(
        "喺下面揀條問題:",
        questions_df['question'].tolist(),
        index=None,
        placeholder="Choose a question..."
    )
    
    if selected_question:        
        # Get answers for selected question
        question_idx = questions_df[questions_df['question'] == selected_question].index[0]
        answers = get_answers_for_question(question_idx, model_answers)

        # Initialize shuffled order when question is selected        
        if 'current_order' not in st.session_state or st.session_state.current_question != selected_question:
            st.session_state.current_order = list(answers.keys())
            random.shuffle(st.session_state.current_order)
            st.session_state.current_question = selected_question
            st.session_state.submitted = False

        # Randomly assign positions to answers
        models = st.session_state.current_order
        
        # Add some spacing
        st.markdown("---")
        
        # Render answer sections and collect user selections
        user_selections = render_answer_sections(models, answers)
        
        # Add some spacing
        st.markdown("---")
        
        # Handle submit/reset buttons
        if render_control_buttons():
            st.session_state.submitted = True
            update_scores(models, user_selections)
            st.rerun()

    # Add footer with some spacing
    st.markdown("""
        <div style='color: #666; padding: 0px;'>
        Demo Made For PyCon 2024 | © 2024
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()