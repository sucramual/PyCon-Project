# ui_components.py
"""UI component rendering functions"""
import streamlit as st
from config import MODELS

def render_header():
    """Render application header and description"""
    st.title("廣東話LLM擂台大決鬥")
    st.markdown("""
        究竟Large Language Model識唔識講廣東話呢？識嘅話佢又係唔係9up呢？
        我地準備幾個模型，分別係 **`GPT-4o`**, **`{model1}`**, **`{model2}`**, **`{model3}`** ，你又試下估下邊個答案係邊個model答？
    """)

def render_metrics():
    """Render metrics showing success rate and total rounds"""
    cols = st.columns(2)
    
    # Calculate success rate
    total_correct = sum(st.session_state.scores.values())
    total_guesses = st.session_state.total_attempts * len(MODELS)  # 4 guesses per round
    success_rate = (total_correct / total_guesses * 100) if total_guesses > 0 else 0
    
    # Color the percentage based on value
    color = "green" if success_rate >= 50 else "red"
    
    # Left column: Success Rate with colored percentage
    with cols[0]:
        st.markdown(
            f"""
            ### 成功率
            <div style="font-size: 30px">
            {total_correct}/{total_guesses} (<span style="color: {color}">{success_rate:.1f}%</span>)
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Right column: Total Rounds
    with cols[1]:
        st.markdown(
            f"""
            ### 回合
            <div style="font-size: 30px">
            {st.session_state.total_attempts}
            <div>
            """,
            unsafe_allow_html=True
        )

def render_answer_sections(models: list, answers: dict) -> list:
    """
    Render answer sections side by side using columns.
    
    Args:
        models (list): List of model names
        answers (dict): Dictionary mapping models to their answers
    
    Returns:
        list: List of user selections for each model
    """

    # Create equal-width columns for side-by-side display
    cols = st.columns(len(models))
    user_selections = []
    
    # Render each answer in its own column
    for idx, (col, model) in enumerate(zip(cols, models)):
        with col:
            st.subheader(f"模型 {idx + 1}")
            
            # Answer text area
            st.text_area(
                "Answer",
                answers[model],
                height=200,
                key=f"answer_{idx}",
                label_visibility="collapsed",
                disabled=True
            )
            
            # Replace radio with selectbox
            selection = st.selectbox(
                "選擇",
                ["請揀個模型..."] + MODELS,  # Add default option
                key=f"selection_{idx}",
                disabled=st.session_state.submitted,
            )
            user_selections.append(selection)
            
            # Show result if submitted
            if st.session_state.submitted:
                if model == selection:
                    st.success(f"你答啱喇! 呢個係{model}。")
                else:
                    st.error(f"哎吖，應該係{model}至啱！")
    
    return user_selections

def render_control_buttons():
    """Render submit and reset buttons"""
    col1, col3 = st.columns([10, 1])
    
    with col1:
        if st.button(
            "Reset",
            type="secondary",
            disabled=not st.session_state.submitted
        ):
            st.session_state.submitted = False
            st.rerun()
            
    with col3:
        return st.button(
            "Submit",
            type="primary",
            disabled=st.session_state.submitted
        )