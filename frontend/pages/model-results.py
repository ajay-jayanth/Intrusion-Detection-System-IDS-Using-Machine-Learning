import streamlit as st
import importlib
import sys
import json
sys.path.append('../streamlit-app.py')
from streamlit_app import run_button, TreeBased

if run_button:
    with open('run_details.json', 'r') as f:
        run_details = json.load(f)

    #data I need
    config = {
        "dataset": run_details["dataset"],
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

    st.title('Model Results')

    acc_col, prec_col, rec_col, f1_col = st.columns(4)
    acc_col.metric("Accuracy", f'{result["accuracy"]:.2%}', '5%')
    prec_col.metric("Precision", f'{result["precision"]:.2%}', '4%')
    rec_col.metric("Recall", f'{result["recall"]:.2%}', '3%')
    f1_col.metric("F1 Score", f'{result["F1_score"]:.2%}', '2%')

    st.write(result)
