import pandas as pd
import streamlit as st
import numpy as np
import sys
sys.path.append('../IDS-engine')
import TreeBased #works, just gives error

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
run_details['dataset'] = dataset



#Tree based details
def runTreeBased():
    #data I need
    config = {
        "dataset": "CICIDS2017_sample.csv",
        "features": {
            #deafult to 1.0, paper uses .9. This value removes features until we only use the top 
            #"feature-trimming" features in our model
            "feature_trimming": 1.0
        },
        #default to this value, if not using SMOTE have empty dictionary
        "SMOTE":{
            #posible key options [0,6]
            #possible value options- any integer
            4: 1500
        },
        #possible model_type values are ["decision tree", "random forest","extra trees", "XGBoost"]
        #is list of the model types user want to use, if multiple models it returns the stacking results
        "model_types": ["decision tree", "random forest","extra trees", "XGBoost"],

        #only have to give this a value if "XGBoost" is in "model_types"
        "XGBoost_params":{
            "n_estimators": 10 #10 is deafult, user can pick any integer
        }
    }

    result = TreeBased.run(config)
    print(result)

runTreeBased()