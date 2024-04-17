import pandas as pd
import streamlit as st
import numpy as np
import sys
import json

sys.path.append('../IDS-engine')
import TreeBased #works, just gives error
import LCCDE

def result_to_table1(run):
    if run["config"] != {} and run["config"]["dataset"] == "carHackingDataset_sample_km":
        data = {
            "Method": ["LightGBM", "XGBoost", "CatBoost", "Proposed LCCDE"],
            "F1 (%) of Class 1: Normal": [run["result"]["LightGBM_F1_classes_score"][0], run["result"]["XGBoost_F1_classes_score"][0], run["result"]["CatBoost_F1_classes_score"][0], run["result"]["LCCDE_F1_classes_score"][0]],
            "F1 (%) of Class 2: DoS": [run["result"]["LightGBM_F1_classes_score"][1], run["result"]["XGBoost_F1_classes_score"][1], run["result"]["CatBoost_F1_classes_score"][1], run["result"]["LCCDE_F1_classes_score"][1]],
            "F1 (%) of Class 3: Fuzzy": [run["result"]["LightGBM_F1_classes_score"][2], run["result"]["XGBoost_F1_classes_score"][2], run["result"]["CatBoost_F1_classes_score"][2], run["result"]["LCCDE_F1_classes_score"][2]],
            "F1 (%) of Class 4: Gear Spoofing": [run["result"]["LightGBM_F1_classes_score"][3], run["result"]["XGBoost_F1_classes_score"][3], run["result"]["CatBoost_F1_classes_score"][3], run["result"]["LCCDE_F1_classes_score"][3]],
            "F1 (%) of Class 5: RPM Spoofing": [run["result"]["LightGBM_F1_classes_score"][4], run["result"]["XGBoost_F1_classes_score"][4], run["result"]["CatBoost_F1_classes_score"][4], run["result"]["LCCDE_F1_classes_score"][4]],
        }

        return pd.DataFrame(data)
    elif run["config"] != {} and run["config"]["dataset"] == "CICIDS2017_sample_km":
        data = {
            "Method": ["LightGBM", "XGBoost", "CatBoost", "Proposed LCCDE"],
            "F1 (%) of Class 1: Normal": [run["result"]["LightGBM_F1_classes_score"][0], run["result"]["XGBoost_F1_classes_score"][0], run["result"]["CatBoost_F1_classes_score"][0], run["result"]["LCCDE_F1_classes_score"][0]],
            "F1 (%) of Class 2: DoS": [run["result"]["LightGBM_F1_classes_score"][1], run["result"]["XGBoost_F1_classes_score"][1], run["result"]["CatBoost_F1_classes_score"][1], run["result"]["LCCDE_F1_classes_score"][1]],
            "F1 (%) of Class 3: Sniffing": [run["result"]["LightGBM_F1_classes_score"][2], run["result"]["XGBoost_F1_classes_score"][2], run["result"]["CatBoost_F1_classes_score"][2], run["result"]["LCCDE_F1_classes_score"][2]],
            "F1 (%) of Class 4: Brute-Force": [run["result"]["LightGBM_F1_classes_score"][3], run["result"]["XGBoost_F1_classes_score"][3], run["result"]["CatBoost_F1_classes_score"][3], run["result"]["LCCDE_F1_classes_score"][3]],
            "F1 (%) of Class 5: Web Attack": [run["result"]["LightGBM_F1_classes_score"][4], run["result"]["XGBoost_F1_classes_score"][4], run["result"]["CatBoost_F1_classes_score"][4], run["result"]["LCCDE_F1_classes_score"][4]],
            "F1 (%) of Class 6: Botnets": [run["result"]["LightGBM_F1_classes_score"][5], run["result"]["XGBoost_F1_classes_score"][5], run["result"]["CatBoost_F1_classes_score"][5], run["result"]["LCCDE_F1_classes_score"][5]],
            "F1 (%) of Class 7: Infiltration": [run["result"]["LightGBM_F1_classes_score"][6], run["result"]["XGBoost_F1_classes_score"][6], run["result"]["CatBoost_F1_classes_score"][6], run["result"]["LCCDE_F1_classes_score"][6]],
        }

        return pd.DataFrame(data)
    
    return {}

def result_to_table2(run):
    if run["config"] != {}:
        data = {
            "Method": ["LightGBM", "XGBoost", "CatBoost", "Proposed LCCDE"],
            "Accuracy (%)": [run["result"]["LightGBM_accuracy"], run["result"]["LightGBM_precision"], run["result"]["LightGBM_recall"], run["result"]["LightGBM_F1_score"]],
            "Precision (%)": [run["result"]["LightGBM_accuracy"], run["result"]["LightGBM_precision"], run["result"]["LightGBM_recall"], run["result"]["LightGBM_F1_score"]],
            "Recall (%)": [run["result"]["LightGBM_accuracy"], run["result"]["LightGBM_precision"], run["result"]["LightGBM_recall"], run["result"]["LightGBM_F1_score"]],
            "F1 (%)": [run["result"]["LightGBM_accuracy"], run["result"]["LightGBM_precision"], run["result"]["LightGBM_recall"], run["result"]["LightGBM_F1_score"]],
        }

        return pd.DataFrame(data)
    
    return {}

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
dataset = st.radio('Choose Dataset:', ['CICIDS2017_sample_km', "carHackingDataset_sample_km"], index=None)
#dataset = 'CICIDS2017_sample.csv' if dataset == 'CICIDS2017 Dataset' else None
run_details['dataset'] = dataset

#do the past runs
runs = {}
with open('runs.json', 'r') as f:
    runs = json.load(f)

st.header("Past Runs")
for run in runs["runs"]:
    if run["config"] and run["config"] != {}:
        st.header("Model performance comparison for each class in {} dataset".format(run["config"]["dataset"]))
        st.table(result_to_table1(run))
        st.header("Performance evaluation of model on {} dataset".format(run["config"]["dataset"]))
        st.table(result_to_table2(run))

#Tree based details
def runTreeBased():
    #data I need
    config = {
        "dataset": run_details['dataset'],
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
        "model_types": ["decision tree"],

        #only have to give this a value if "XGBoost" is in "model_types"
        "XGBoost_params":{
            "n_estimators": 10
        }
    }
    result = TreeBased.run(config)

    #save the run
    runs["runs"].append({
        "config": config,
        "result": result
    })
    json_object = json.dumps(runs, indent=4)
    with open("runs.json", "w") as outfile:
        outfile.write(json_object)

    st.rerun()

#Tree based details
def runLCCDE():
    #data I need
    config = {
        #two options carHackingDataset_sample_km && CICIDS2017_sample_km
        "dataset": run_details["dataset"],
        "smote": None #{2:1000,4:1000} for CICIDS2017
    }
    result = LCCDE.run(config)

    #save the run
    runs["runs"].append({
        "config": config,
        "result": result
    })

    json_object = json.dumps(runs, indent=4)
    with open("runs.json", "w") as outfile:
        outfile.write(json_object)
    st.rerun()

run_button = st.button('Run')
if run_button:
    runLCCDE()
