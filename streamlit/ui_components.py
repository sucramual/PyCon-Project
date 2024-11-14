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
    
    styles = """
        <style>
            .metrics-container {
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 15px;
            }
            .success-high {
                background-color: rgba(144, 238, 144, 0.3);  /* light green with 0.3 opacity */
            }
            .success-low {
                background-color: rgba(255, 182, 193, 0.3);  /* light red with 0.3 opacity */
            }
            .metric-value {
                font-size: 30px;
                font-weight: 500;
            }
            .metric-title {
                margin-bottom: 8px;
                font-size: 1.17em;
                font-weight: bold;
            }
        </style>
    """

    # Color the percentage based on value
    color = "green" if success_rate >= 50 else "red"
    
    # Left column: Success Rate with colored percentage
    with cols[0]:
        st.markdown(
            f"""
            <h3>成功率</h3>
                <div style="font-size: 30px">
                {total_correct}/{total_guesses} (<span style="color: {color}">{success_rate:.1f}%</span>)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Right column: Total Rounds
    with cols[1]:
        st.markdown(
            f"""
            <h3>回合</h3>
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

    # Reset selections when new question is selected
    if st.session_state.get('current_question') != st.session_state.get('last_question'):
        for idx in range(len(models)):
            if f'selection_{idx}' in st.session_state:
                st.session_state[f'selection_{idx}'] = "請揀個模型..."  # Reset to default
        st.session_state['last_question'] = st.session_state.get('current_question')
    
    # Render each answer in its own column
    for idx, (col, model) in enumerate(zip(cols, models)):
            with col:
                st.subheader(f"模型 {idx + 1}")
                
                with st.container():
                    st.markdown("""
                        <div style='background-color: white; 
                            padding: 1rem; 
                            border-radius: 0.5rem; 
                            border: 1px solid #ddd;
                            min-height: 350px;'>
                            {}
                        </div>
                    """.format(answers[model]), unsafe_allow_html=True)
                
                selection = st.selectbox(
                    "選擇",
                    ["請揀個模型..."] + MODELS,
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