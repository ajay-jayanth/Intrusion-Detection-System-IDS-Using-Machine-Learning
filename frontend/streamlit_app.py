import streamlit as st
import numpy as np
import sys
sys.path.append('../IDS-engine')
import TreeBased #works, just gives error
import json

result = {}

st.title('Intrusion Detection Application')
run_details = {}

st.header('Model Selection')
model = st.radio('Choose IDS model:', ['Tree-Based IDS', 'MTH IDS', 'LCCDE IDS'], index=None)
run_details['model'] = model

st.header('Training Parameters')
train_proportion = st.select_slider(label='Select the training size percentage (Train/Test Split):', options=[f'{val:.0f}%' for val in np.linspace(50, 95, 10)])
training_parameters = {}

criterion = st.radio('Choose criterion:', ['Gini', 'Entropy'], index=None)
training_parameters['criterion'] = criterion

lr = st.select_slider(label='Select learning rate:', options=[0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 0.9])
training_parameters['learning rate'] = lr

run_details['training parameters'] = training_parameters

model_parameters = {}
if model == 'Tree-Based IDS':
    st.header('Model Hyperparameters')

elif model == 'MTH IDS':
    st.header('Model Hyperparameters')

elif model == 'LCCDE IDS':
    st.header('Model Hyperparameters')
run_details['model parameters'] = model_parameters

st.header('Dataset')
dataset = st.radio('Choose Dataset:', ['Car-Hacking Dataset', 'CICIDS2017 Dataset'], index=None)
dataset = 'CICIDS2017_sample.csv' if dataset == 'CICIDS2017 Dataset' else None
run_details['dataset'] = dataset

with open('run_details.json', 'w') as f:
    json.dump(run_details, f)

st.markdown(
    """
    <style>
    /* Style the page_link button */
    .streamlit-button.stButton>div>div>div {
        color: #0077cc; /* Button text color */
        background-color: transparent; /* Button background color */
        border: none; /* Remove button border */
        padding: 0; /* Remove padding */
        font-weight: normal; /* Set font weight */
        text-decoration: underline; /* Add underline to text */
        cursor: pointer; /* Change cursor on hover */
    }

    /* Style the page_link button on hover */
    .streamlit-button.stButton>div>div>div:hover {
        color: #005299; /* Button text color on hover */
        text-decoration: underline; /* Add underline to text on hover */
    }

    /* Disable button ripple effect */
    .streamlit-button.stButton>div>div {
        background-color: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

run_button = st.page_link("pages/model-results.py", label="Run")