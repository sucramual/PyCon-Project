# config.py
"""Configuration settings and constants"""
import streamlit as st

PAGE_CONFIG = {
    "page_title": "廣東話LLM擂台大決鬥",
    "layout": "wide",
    "page_icon":"🀄️"
}

MODELS = ['GPT-4o', 'Qwen25-3B', 'Qwen25-1.5B', 'Qwen25-0.5B']

INITIAL_STATE = {
    'submitted': False,
    'scores': {model: 0 for model in MODELS},
    'total_attempts': 0
}