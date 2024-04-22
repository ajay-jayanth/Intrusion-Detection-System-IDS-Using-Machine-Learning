import streamlit as st
import json
import pandas as pd
from datetime import datetime
import sys
sys.path.append('../IDS-engine')
import LCCDE
import TreeBased
import MTH


#FUNCTIONS---------------------------------------------------------------------------
def result_to_table1_LCCDE(run):
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

def result_to_table2_LCCDE(run):
    if run["config"] != {}:
        data = {
            "Method": ["LightGBM", "XGBoost", "CatBoost", "Proposed LCCDE"],
            "Accuracy (%)": [run["result"]["LightGBM_accuracy"], run["result"]["XGBoost_accuracy"], run["result"]["CatBoost_accuracy"], run["result"]["LCCDE_accuracy"]],
            "Precision (%)": [run["result"]["LightGBM_precision"], run["result"]["XGBoost_precision"], run["result"]["CatBoost_precision"], run["result"]["LCCDE_precision"]],
            "Recall (%)": [run["result"]["LightGBM_recall"], run["result"]["XGBoost_recall"], run["result"]["CatBoost_recall"], run["result"]["LCCDE_recall"]],
            "F1 (%)": [run["result"]["LightGBM_F1_score"], run["result"]["XGBoost_F1_score"], run["result"]["CatBoost_F1_score"], run["result"]["LCCDE_F1_score"]],
        }

        return pd.DataFrame(data)
    
    return {}

def result_to_table1_TreeBased(run):
    if run["config"] != {}:
        data = {
            "Method": ["Decision Tree", "Random Forest", "Extra Trees", "XGBoost", "Stacking"],
            "Accuracy (%)": [run["result"]["decision_tree_accuracy"], run["result"]["random_forest_accuracy"], run["result"]["extra_trees_accuracy"], run["result"]["XGBoost_accuracy"], run["result"]["stacking_accuracy"]],
            "Precision (%)": [run["result"]["decision_tree_precision"], run["result"]["random_forest_precision"], run["result"]["extra_trees_precision"], run["result"]["XGBoost_precision"], run["result"]["stacking_precision"]],
            "Recall (%)": [run["result"]["decision_tree_recall"], run["result"]["random_forest_recall"], run["result"]["extra_trees_recall"], run["result"]["XGBoost_recall"], run["result"]["stacking_recall"]],
            "F1 (%)": [run["result"]["decision_tree_F1_score"], run["result"]["random_forest_F1_score"], run["result"]["extra_trees_F1_score"], run["result"]["XGBoost_F1_score"], run["result"]["stacking_F1_score"]],
        }

        return pd.DataFrame(data)
    
    return {}

def result_to_table1_MTH(run):
    if run["config"] != {}:
        data = {
            "Method": ["Random Forest", "Random Forest (HPO)", "Decision Tree", "Decision Tree (HPO)", "Extra Trees", "Extra Trees (HPO)", "MTH-DS", "MTH-IDS (HPO)"],
            "Accuracy (%)": [
                run["result"]["random_forest_accuracy"],
                run["result"]["random_forest_hpo_accuracy"],
                run["result"]["decision_tree_accuracy"],
                run["result"]["decision_tree_hpo_accuracy"],
                run["result"]["extra_trees_accuracy"],
                run["result"]["extra_trees_hpo_accuracy"],
                run["result"]["mth_ids_accuracy"],
                run["result"]["mth_ids_hpo_accuracy"]
            ], 
            "Precision (%)": [
                run["result"]["random_forest_precision"],
                run["result"]["random_forest_hpo_precision"],
                run["result"]["decision_tree_precision"],
                run["result"]["decision_tree_hpo_precision"],
                run["result"]["extra_trees_precision"],
                run["result"]["extra_trees_hpo_precision"],
                run["result"]["mth_ids_precision"],
                run["result"]["mth_ids_hpo_precision"]
            ],
            "Recall (%)": [
                run["result"]["random_forest_F1"],
                run["result"]["random_forest_hpo_F1"],
                run["result"]["decision_tree_F1"],
                run["result"]["decision_tree_hpo_F1"],
                run["result"]["extra_trees_F1"],
                run["result"]["extra_trees_hpo_F1"],
                run["result"]["mth_ids_F1"],
                run["result"]["mth_ids_hpo_F1"]
            ],
            "F1 (%)": [
                run["result"]["random_forest_recall"],
                run["result"]["random_forest_hpo_recall"],
                run["result"]["decision_tree_recall"],
                run["result"]["decision_tree_hpo_recall"],
                run["result"]["extra_trees_recall"],
                run["result"]["extra_trees_hpo_recall"],
                run["result"]["mth_ids_recall"],
                run["result"]["mth_ids_hpo_recall"]
            ]
        }

        return pd.DataFrame(data)
    
    return {}

def runLCCDE(config, rundata, runs):
    #do timestamp
    rundata["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = LCCDE.run(config)

    #save the run
    runs["runs"].append({
        "rundata": rundata,
        "config": config,
        "result": result
    })

    json_object = json.dumps(runs, indent=4)
    with open("runs.json", "w") as outfile:
        outfile.write(json_object)

def runTreeBased(config, rundata, runs):
    #do timestamp
    rundata["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = TreeBased.run(config)

    #save the run
    runs["runs"].append({
        "rundata": rundata,
        "config": config,
        "result": result
    })

    json_object = json.dumps(runs, indent=4)
    with open("runs.json", "w") as outfile:
        outfile.write(json_object)

def runMTH(config, rundata, runs):
    #do timestamp
    rundata["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #reformat config
    mth_config = {
        'dataset': config['dataset'],
        'n_estimators': {'min': config['n_estimators_min'], 'max': config['n_estimators_max'], 'step': config['n_estimators_step']},
        'max_depth': {'min': config['max_depth_min'], 'max': config['max_depth_max'], 'step': config['max_depth_step']},
        'max_features': {'min': config['max_features_min'], 'max': config['max_features_max'], 'step': config['max_features_step']},
        'min_samples_split': {'min': config['min_samples_split_min'], 'max': config['min_samples_split_max'], 'step': config['min_samples_split_step']},
        'min_samples_leaf': {'min': config['min_samples_leaf_min'], 'max': config['min_samples_leaf_max'], 'step': config['min_samples_leaf_step']},
        'criterion': ['gini', 'entropy'],
        'learning_rate': {'mean': config['learning_rate_mean'], 'std': config['learning_rate_std']}
    }
    result = MTH.run(mth_config)

    #save the run
    runs["runs"].append({
        "rundata": rundata,
        "config": config,
        "result": result
    })

    json_object = json.dumps(runs, indent=4)
    with open("runs.json", "w") as outfile:
        outfile.write(json_object)

#LOGIC CODE------------------------------------------------------------------------------------------
#get paper results
paper_runs_LCCDE = {}
with open('LCCDE_PAPER.json', 'r') as f:
    paper_runs_LCCDE = json.load(f)

paper_runs_Tree_Based = {}
with open('Tree_Based_Paper.json', 'r') as f:
    paper_runs_Tree_Based = json.load(f)

paper_runs_MTH = {}
with open('MTH_Paper.json', 'r') as f:
    paper_runs_MTH = json.load(f)

#do the past runs
runs = {}
with open('runs.json', 'r') as f:
    runs = json.load(f)



config = {}
rundata = {}

if 'copy_parameters' not in st.session_state:
    st.session_state.copy_parameters = False

if 'delete_run' not in st.session_state:
    st.session_state.delete_run = False
#STREAMLIT ---------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide") #make page wide

#get rid of streamlit header bar
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        .block-container {
            padding-top: .5em;
        }
        header{
            visibility: hidden;
        }
        h2{
            margin-top: 0;
            padding-top: 0;
        }
        hr{
            height: 2px;
            margin-top: 0;
            margin-bottom: 0;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,3])

#left 1/3 of the screen
with col1:
    #testing
    if st.session_state.copy_parameters:
        st.session_state.current_run = 'New Run'
        st.session_state.model_type = st.session_state.copied_parameters["model_type"]
        st.session_state.dataset = st.session_state.copied_parameters["dataset"]
        st.session_state.test_data_percent = st.session_state.copied_parameters["test_data_percent"]
        st.session_state.random_state = st.session_state.copied_parameters["random_state"]
        st.session_state.boosting_type = st.session_state.copied_parameters["boosting_type"]

        st.session_state.max_value_ne = st.session_state.copied_parameters["n_estimators_max"]
        st.session_state.min_value_ne = st.session_state.copied_parameters["n_estimators_min"]
        st.session_state.step_value_ne = st.session_state.copied_parameters["n_estimators_step"]
        st.session_state.max_value_md = st.session_state.copied_parameters["max_depth_max"]
        st.session_state.min_value_md = st.session_state.copied_parameters["max_depth_min"]
        st.session_state.step_value_md = st.session_state.copied_parameters["max_depth_step"]
        st.session_state.max_value_mf = st.session_state.copied_parameters["max_features_max"]
        st.session_state.min_value_mf = st.session_state.copied_parameters["max_features_min"]
        st.session_state.step_value_mf = st.session_state.copied_parameters["max_features_step"]
        st.session_state.max_value_mss = st.session_state.copied_parameters["min_samples_split_max"]
        st.session_state.min_value_mss = st.session_state.copied_parameters["min_samples_split_min"]
        st.session_state.step_value_mss = st.session_state.copied_parameters["min_samples_split_step"]
        st.session_state.max_value_msl = st.session_state.copied_parameters["min_samples_leaf_max"]
        st.session_state.min_value_msl = st.session_state.copied_parameters["min_samples_leaf_min"]
        st.session_state.step_value_msl = st.session_state.copied_parameters["min_samples_leaf_step"]
        st.session_state.mean_value_lr = st.session_state.copied_parameters["learning_rate_mean"]
        st.session_state.std_value_lr = st.session_state.copied_parameters["learning_rate_std"]

        #st.session_state.smote = st.session_state.copied_parameters["smote"]
    st.session_state.copy_parameters = False

    if st.session_state.delete_run:
        st.session_state.current_run = "New Run"
    st.session_state.delete_run = False
    #end testing

    st.header("Run Configuration")
    #select past run or new run
    runOptions = ['New Run']
    runOptions += ["{} - {} - {}".format(run["rundata"]["name"], run["rundata"]["timestamp"], run["config"]["dataset"]) for run in runs["runs"]]
    runOptions = {value: index for index, value in enumerate(runOptions)}
    currentRun = st.selectbox("View Run: ", runOptions.keys(),index = 0, key="current_run")
    currentRun = runOptions[currentRun]
    # Add a horizontal line
    st.markdown("<hr>", unsafe_allow_html=True)

    #display run parameters
    if currentRun == 0:
        rundata["name"] = st.text_input('Run Name: ', 'Run {}'.format(len(runs["runs"]) + 1))

        rundata["model_type"] = st.selectbox('Model Type: ', ("LCCDE", "MTH", "Tree Based"), key="model_type")

        if rundata["model_type"] == "LCCDE":
            config["dataset"] = st.selectbox("Dataset: ", ("carHackingDataset_km", "carHackingDataset_sample_km", "CICIDS2017_km", "CICIDS2017_sample_km"), key="dataset")
            
            config["test_data_percent"] = st.slider("Test Data Percent: ", min_value=0.01, max_value=.99,value=(st.session_state.test_data_percent if "test_data_percent" in st.session_state else .2), step=0.01, key="test_data_percent")

            config["random_state"] = st.number_input("Random State: ", min_value=0, value=0, step=1, key="random_state")

            config["boosting_type"] = st.selectbox("Boosting Type: ", ("Plain", "Ordered"), key="boosting_type")

            config["smote"] = st.text_input('SMOTE (optional): ', '{"2":1000, "4":1000}' if config["dataset"] == "CICIDS2017_km" or config["dataset"] == "CICIDS2017_sample_km" else "")
        elif rundata["model_type"] == "MTH":
            config["dataset"] = st.selectbox("Dataset: ", ["CICIDS2017_sample", "CICIDS2017"], key="dataset_MTH")
            
            # Get user inputs for max, min, and step for n estimators
            st.write("N Estimators: ")
            maxLabel_ne, maxInput_ne, minLabel_ne, minInput_ne, stepLabel_ne, stepInput_ne = st.columns(6)
            with maxLabel_ne:
                st.write("Max:")
            with maxInput_ne:
                config["n_estimators_max"] = st.number_input("Max: ", min_value=1, value=200, step=1, label_visibility="collapsed", key="max_value_ne")

            with minLabel_ne:
                st.write("Min:")
            with minInput_ne:
                config["n_estimators_min"] = st.number_input("Min: ", min_value=0, value=10, step=1, label_visibility="collapsed", key="min_value_ne")

            with stepLabel_ne:
                st.write("Step:")
            with stepInput_ne: 
                config["n_estimators_step"] = st.number_input("Step: ", min_value=1, value=1, step=1, label_visibility="collapsed", key="step_value_ne")
            
            # Get user inputs for max, min, and step for n estimators
            st.write("Max Depth: ")
            maxLabel_md, maxInput_md, minLabel_md, minInput_md, stepLabel_md, stepInput_md = st.columns(6)
            with maxLabel_md:
                st.write("Max:")
            with maxInput_md:
                config["max_depth_max"] = st.number_input("Max: ", min_value=1, value=50, step=1, label_visibility="collapsed", key="max_value_md")

            with minLabel_md:
                st.write("Min:")
            with minInput_md:
                config["max_depth_min"] = st.number_input("Min: ", min_value=0, value=5, step=1, label_visibility="collapsed", key="min_value_md")

            with stepLabel_md:
                st.write("Step:")
            with stepInput_md: 
                config["max_depth_step"] = st.number_input("Step: ", min_value=1, value=1, step=1, label_visibility="collapsed", key="step_value_md")

            # Get user inputs for max, min, and step for n estimators
            st.write("Max Features: ")
            maxLabel_mf, maxInput_mf, minLabel_mf, minInput_mf, stepLabel_mf, stepInput_mf = st.columns(6)
            with maxLabel_mf:
                st.write("Max:")
            with maxInput_mf:
                config["max_features_max"] = st.number_input("Max: ", min_value=1, value=20, step=1, label_visibility="collapsed", key="max_value_mf")

            with minLabel_mf:
                st.write("Min:")
            with minInput_mf:
                config["max_features_min"] = st.number_input("Min: ", min_value=0, value=1, step=1, label_visibility="collapsed", key="min_value_mf")

            with stepLabel_mf:
                st.write("Step:")
            with stepInput_mf: 
                config["max_features_step"] = st.number_input("Step: ", min_value=1, value=1, step=1, label_visibility="collapsed", key="step_value_mf")

            # Get user inputs for max, min, and step for n estimators
            st.write("Min Samples Split: ")
            maxLabel_mss, maxInput_mss, minLabel_mss, minInput_mss, stepLabel_mss, stepInput_mss = st.columns(6)
            with maxLabel_mss:
                st.write("Max:")
            with maxInput_mss:
                config["min_samples_split_max"] = st.number_input("Max: ", min_value=1, value=11, step=1, label_visibility="collapsed", key="max_value_mss")

            with minLabel_mss:
                st.write("Min:")
            with minInput_mss:
                config["min_samples_split_min"] = st.number_input("Min: ", min_value=0, value=2, step=1, label_visibility="collapsed", key="min_value_mss")

            with stepLabel_mss:
                st.write("Step:")
            with stepInput_mss: 
                config["min_samples_split_step"] = st.number_input("Step: ", min_value=1, value=1, step=1, label_visibility="collapsed", key="step_value_mss")

            # Get user inputs for max, min, and step for n estimators
            st.write("Min Samples Leaf: ")
            maxLabel_msl, maxInput_msl, minLabel_msl, minInput_msl, stepLabel_msl, stepInput_msl = st.columns(6)
            with maxLabel_msl:
                st.write("Max:")
            with maxInput_msl:
                config["min_samples_leaf_max"] = st.number_input("Max: ", min_value=1, value=11, step=1, label_visibility="collapsed", key="max_value_msl")

            with minLabel_msl:
                st.write("Min:")
            with minInput_msl:
                config["min_samples_leaf_min"] = st.number_input("Min: ", min_value=0, value=1, step=1, label_visibility="collapsed", key="min_value_msl")

            with stepLabel_msl:
                st.write("Step:")
            with stepInput_msl: 
                config["min_samples_leaf_step"] = st.number_input("Step: ", min_value=1, value=1, step=1, label_visibility="collapsed", key="step_value_msl")

            st.write("Learning Rate: ")
            meanLabel_lr, meanInput_lr, stdLabel_lr, stdInput_lr= st.columns(4)
            with meanLabel_lr:
                st.write("Mean:")
            with meanInput_lr:
                config["learning_rate_mean"] = st.number_input("Mean: ", min_value=0.0, max_value=1.0, value=.01, step=.01, label_visibility="collapsed", key="mean_value_lr")
            
            with stdLabel_lr:
                st.write("Std:")
            with stdInput_lr:
                config["learning_rate_std"] = st.number_input("Std: ", min_value=0.0, max_value=1.0, value=.9, step=.01, label_visibility="collapsed", key="std_value_lr")


        elif rundata["model_type"] == "Tree Based":
            config["dataset"] = st.selectbox("Dataset: ", ("CICIDS2017_sample", "CICIDS2017", "CANIntrusion_sample", "CANIntrusion"), key="dataset_TreeBased")
            
            config["test_data_percent"] = st.slider("Test Data Percent: ", min_value=0.01, max_value=.99,value=(st.session_state.test_data_percent_TreeBased if "test_data_percent_TreeBased" in st.session_state else .2), step=0.01, key="test_data_percent_TreeBased")

            config["random_state"] = st.number_input("Random State: ", min_value=0, value=0, step=1, key="random_state_TreeBased")

            config["feature_trimming"] = st.slider("Feature Trimming: ", min_value=0.01, max_value=1.0,value=(st.session_state.feature_trimming_TreeBased if "feature_trimming_TreeBased" in st.session_state else .9), step=0.01, key="feature_trimming_TreeBased")

            config["model_types"] = st.multiselect("Model Types: ", ["decision tree", "random forest","extra trees", "XGBoost"], default=["decision tree", "random forest","extra trees", "XGBoost"], key="model_types_TreeBased")

            config["XGBoost_n_estimators"] = st.number_input("XGBoost n estimators: ", min_value=1, value=10, step=1, key="xgboost_n_estimators")
            
            config["smote"] = st.text_input('SMOTE (optional): ', '{"4":1500}' if config["dataset"] == "CICIDS2017" or config["dataset"] == "CICIDS2017_sample" else "")

        #display run button
        if st.button("Run"):
            # Code to run when the button is clicked
            with st.spinner("Training Model..."):
                if rundata["model_type"] == "LCCDE":
                    runLCCDE(config, rundata, runs)
                    st.rerun()
                elif rundata["model_type"] == "MTH":
                    runMTH(config, rundata, runs)
                    st.rerun()
                elif rundata["model_type"] == "Tree Based":
                    runTreeBased(config, rundata, runs)
                    st.rerun()

    else:
        st.text_input('Run Name: ', '{}'.format(runs["runs"][currentRun - 1]["rundata"]["name"]), disabled=True)
        
        st.selectbox('Model Type: ', ["{}".format(runs["runs"][currentRun - 1]["rundata"]["model_type"])], disabled=True)

        if runs["runs"][currentRun - 1]["rundata"]["model_type"] == "LCCDE":
            st.text_input('Timestamp: ', '{}'.format(runs["runs"][currentRun - 1]["rundata"]["timestamp"]), disabled=True)

            st.selectbox("Dataset: ",["{}".format(runs["runs"][currentRun - 1]["config"]["dataset"])], disabled=True)

            st.slider("Test Data Percent: ", 0.01, .99, runs["runs"][currentRun - 1]["config"]["test_data_percent"], 0.01, disabled=True)

            st.number_input("Random State: ", value=runs["runs"][currentRun - 1]["config"]["random_state"], step=1, disabled=True)

            st.selectbox("Boosting Type: ", [runs["runs"][currentRun - 1]["config"]["boosting_type"]], disabled=True)

            st.text_input('SMOTE (optional): ', runs["runs"][currentRun - 1]["config"]["smote"], disabled=True)
        elif runs["runs"][currentRun - 1]["rundata"]["model_type"] == "MTH":
            st.text_input('Timestamp: ', '{}'.format(runs["runs"][currentRun - 1]["rundata"]["timestamp"]), disabled=True)
            
            st.selectbox("Dataset: ", ["{}".format(runs["runs"][currentRun - 1]["config"]["dataset"])], key="dataset_MTH", disabled=True)
            
            # Get user inputs for max, min, and step for n estimators
            st.write("N Estimators: ")
            maxLabel_ne, maxInput_ne, minLabel_ne, minInput_ne, stepLabel_ne, stepInput_ne = st.columns(6)
            with maxLabel_ne:
                st.write("Max:")
            with maxInput_ne:
                st.number_input("Max: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["n_estimators_max"], step=1, label_visibility="collapsed", disabled = True, key="randomKeyInput0")

            with minLabel_ne:
                st.write("Min:")
            with minInput_ne:
                st.number_input("Min: ", min_value=0, value=runs["runs"][currentRun - 1]["config"]["n_estimators_min"], step=1, label_visibility="collapsed", disabled = True, key="randomKeyInput1")

            with stepLabel_ne:
                st.write("Step:")
            with stepInput_ne: 
                st.number_input("Step: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["n_estimators_step"], step=1, label_visibility="collapsed", disabled = True, key="randomKeyInput2")
            
            # Get user inputs for max, min, and step for n estimators
            st.write("Max Depth: ")
            maxLabel_md, maxInput_md, minLabel_md, minInput_md, stepLabel_md, stepInput_md = st.columns(6)
            with maxLabel_md:
                st.write("Max:")
            with maxInput_md:
                st.number_input("Max: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["max_depth_max"], step=1, label_visibility="collapsed", disabled = True, key="randomKeyInput3")

            with minLabel_md:
                st.write("Min:")
            with minInput_md:
                st.number_input("Min: ", min_value=0, value=runs["runs"][currentRun - 1]["config"]["max_depth_min"], step=1, label_visibility="collapsed", disabled = True, key="randomKeyInput4")

            with stepLabel_md:
                st.write("Step:")
            with stepInput_md: 
                st.number_input("Step: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["max_depth_step"], step=1, label_visibility="collapsed", disabled = True, key="randomKeyInput5") #need random key for some reason

            # Get user inputs for max, min, and step for n estimators
            st.write("Max Features: ")
            maxLabel_mf, maxInput_mf, minLabel_mf, minInput_mf, stepLabel_mf, stepInput_mf = st.columns(6)
            with maxLabel_mf:
                st.write("Max:")
            with maxInput_mf:
                st.number_input("Max: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["max_features_max"], step=1, label_visibility="collapsed", disabled=True, key="randomKeyInput6")

            with minLabel_mf:
                st.write("Min:")
            with minInput_mf:
                st.number_input("Min: ", min_value=0, value=runs["runs"][currentRun - 1]["config"]["max_features_min"], step=1, label_visibility="collapsed", disabled=True, key="randomKeyInput7")

            with stepLabel_mf:
                st.write("Step:")
            with stepInput_mf: 
                st.number_input("Step: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["max_features_step"], step=1, label_visibility="collapsed", disabled=True, key="randomKeyInput8")

            # Get user inputs for max, min, and step for n estimators
            st.write("Min Samples Split: ")
            maxLabel_mss, maxInput_mss, minLabel_mss, minInput_mss, stepLabel_mss, stepInput_mss = st.columns(6)
            with maxLabel_mss:
                st.write("Max:")
            with maxInput_mss:
                st.number_input("Max: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["min_samples_split_max"], step=1, label_visibility="collapsed", disabled=True, key="randomKeyInput9")

            with minLabel_mss:
                st.write("Min:")
            with minInput_mss:
                st.number_input("Min: ", min_value=0, value=runs["runs"][currentRun - 1]["config"]["min_samples_split_min"], step=1, label_visibility="collapsed", disabled=True, key="randomKeyInput10")

            with stepLabel_mss:
                st.write("Step:")
            with stepInput_mss: 
                st.number_input("Step: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["min_samples_split_step"], step=1, label_visibility="collapsed", disabled=True, key="randomKeyInput11")

            # Get user inputs for max, min, and step for n estimators
            st.write("Min Samples Leaf: ")
            maxLabel_msl, maxInput_msl, minLabel_msl, minInput_msl, stepLabel_msl, stepInput_msl = st.columns(6)
            with maxLabel_msl:
                st.write("Max:")
            with maxInput_msl:
                st.number_input("Max: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["min_samples_leaf_max"], step=1, label_visibility="collapsed", disabled=True, key="randomKeyInput12")

            with minLabel_msl:
                st.write("Min:")
            with minInput_msl:
                st.number_input("Min: ", min_value=0, value=runs["runs"][currentRun - 1]["config"]["min_samples_leaf_min"], step=1, label_visibility="collapsed", disabled=True, key="randomKeyInput13")

            with stepLabel_msl:
                st.write("Step:")
            with stepInput_msl: 
                st.number_input("Step: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["min_samples_leaf_step"], step=1, label_visibility="collapsed", disabled=True, key="randomKeyInput14")

            st.write("Learning Rate: ")
            meanLabel_lr, meanInput_lr, stdLabel_lr, stdInput_lr= st.columns(4)
            with meanLabel_lr:
                st.write("Mean:")
            with meanInput_lr:
                st.number_input("Mean: ", min_value=0.0, max_value=1.0, value=runs["runs"][currentRun - 1]["config"]["learning_rate_mean"], step=.01, label_visibility="collapsed", disabled=True, key="randomKeyInput15")
            
            with stdLabel_lr:
                st.write("Std:")
            with stdInput_lr:
                st.number_input("Std: ", min_value=0.0, max_value=1.0, value=runs["runs"][currentRun - 1]["config"]["learning_rate_std"], step=.01, label_visibility="collapsed", disabled=True, key="randomKeyInput16")

        elif runs["runs"][currentRun - 1]["rundata"]["model_type"] == "Tree Based":
            st.text_input('Timestamp: ', '{}'.format(runs["runs"][currentRun - 1]["rundata"]["timestamp"]), disabled=True)

            st.selectbox("Dataset: ",["{}".format(runs["runs"][currentRun - 1]["config"]["dataset"])], disabled=True)

            st.slider("Test Data Percent: ", 0.01, .99, runs["runs"][currentRun - 1]["config"]["test_data_percent"], 0.01, disabled=True)

            st.number_input("Random State: ", value=runs["runs"][currentRun - 1]["config"]["random_state"], step=1, disabled=True)

            st.slider("Feature Trimming: ", 0.01, 1.0, runs["runs"][currentRun - 1]["config"]["feature_trimming"], 0.01, disabled=True)

            st.multiselect("Model Types: ", ["decision tree", "random forest","extra trees", "XGBoost"], default= runs["runs"][currentRun - 1]["config"]["model_types"], disabled=True)

            st.number_input("XGBoost n estimators: ", min_value=1, value=runs["runs"][currentRun - 1]["config"]["XGBoost_n_estimators"], step=1, disabled=True)
            
            st.text_input('SMOTE (optional): ', runs["runs"][currentRun - 1]["config"]["smote"], disabled=True)

        left, right = st.columns(2)
        with left:
            #display delete button
            if st.button("Delete Run"):
                # Code to run when the button is clicked
                runs["runs"].pop(currentRun - 1)

                json_object = json.dumps(runs, indent=4)
                with open("runs.json", "w") as outfile:
                    outfile.write(json_object)

                st.session_state.delete_run = True
                st.rerun()
        
        with right:
            #display copy run button
            if st.button("Copy Run"):
                # Code to run when the button is clicked
                st.session_state.copied_parameters = {
                    "model_type": runs["runs"][currentRun - 1]["rundata"]["model_type"],
                    "dataset": runs["runs"][currentRun - 1]["config"]["dataset"],
                    "test_data_percent": runs["runs"][currentRun - 1]["config"]["test_data_percent"] if "test_data_percent" in runs["runs"][currentRun - 1]["config"] else "",
                    "random_state": runs["runs"][currentRun - 1]["config"]["random_state"] if "random_state" in runs["runs"][currentRun - 1]["config"] else "",
                    "boosting_type": runs["runs"][currentRun - 1]["config"]["boosting_type"] if "boosting_type" in runs["runs"][currentRun - 1]["config"] else "",
                    "smote": runs["runs"][currentRun - 1]["config"]["smote"] if "smote" in runs["runs"][currentRun - 1]["config"] else "",

                    "n_estimators_max": runs["runs"][currentRun - 1]["config"]["n_estimators_max"] if "n_estimators_max" in runs["runs"][currentRun - 1]["config"] else "",
                    "n_estimators_min": runs["runs"][currentRun - 1]["config"]["n_estimators_min"] if "n_estimators_min" in runs["runs"][currentRun - 1]["config"] else "",
                    "n_estimators_step": runs["runs"][currentRun - 1]["config"]["n_estimators_step"] if "n_estimators_step" in runs["runs"][currentRun - 1]["config"] else "",
                    "max_depth_max": runs["runs"][currentRun - 1]["config"]["max_depth_max"] if "max_depth_max" in runs["runs"][currentRun - 1]["config"] else "",
                    "max_depth_min": runs["runs"][currentRun - 1]["config"]["max_depth_min"] if "max_depth_min" in runs["runs"][currentRun - 1]["config"] else "",
                    "max_depth_step": runs["runs"][currentRun - 1]["config"]["max_depth_step"] if "max_depth_step" in runs["runs"][currentRun - 1]["config"] else "",
                    "max_features_max": runs["runs"][currentRun - 1]["config"]["max_features_max"] if "max_features_max" in runs["runs"][currentRun - 1]["config"] else "",
                    "max_features_min": runs["runs"][currentRun - 1]["config"]["max_features_min"] if "max_features_min" in runs["runs"][currentRun - 1]["config"] else "",
                    "max_features_step": runs["runs"][currentRun - 1]["config"]["max_features_step"] if "max_features_step" in runs["runs"][currentRun - 1]["config"] else "",
                    "min_samples_split_max": runs["runs"][currentRun - 1]["config"]["min_samples_split_max"] if "min_samples_split_max" in runs["runs"][currentRun - 1]["config"] else "",
                    "min_samples_split_min": runs["runs"][currentRun - 1]["config"]["min_samples_split_min"] if "min_samples_split_min" in runs["runs"][currentRun - 1]["config"] else "",
                    "min_samples_split_step": runs["runs"][currentRun - 1]["config"]["min_samples_split_step"] if "min_samples_split_step" in runs["runs"][currentRun - 1]["config"] else "",
                    "min_samples_leaf_max": runs["runs"][currentRun - 1]["config"]["min_samples_leaf_max"] if "min_samples_leaf_max" in runs["runs"][currentRun - 1]["config"] else "",
                    "min_samples_leaf_min": runs["runs"][currentRun - 1]["config"]["min_samples_leaf_min"] if "min_samples_leaf_min" in runs["runs"][currentRun - 1]["config"] else "",
                    "min_samples_leaf_step": runs["runs"][currentRun - 1]["config"]["min_samples_leaf_step"] if "min_samples_leaf_step" in runs["runs"][currentRun - 1]["config"] else "",
                    "learning_rate_mean": runs["runs"][currentRun - 1]["config"]["learning_rate_mean"] if "learning_rate_mean" in runs["runs"][currentRun - 1]["config"] else "",
                    "learning_rate_std": runs["runs"][currentRun - 1]["config"]["learning_rate_std"] if "learning_rate_std" in runs["runs"][currentRun - 1]["config"] else ""
                }

                st.session_state.copy_parameters = True
                st.rerun()

#right 2/3 of the screen
with col2:
    if currentRun == 0:
        st.header("{} Paper Results".format(rundata["model_type"]))
        if rundata["model_type"] == "LCCDE":
            left, right = st.columns(2)
            with left:
                st.write("CICIDS2017 Dataset Results")
                st.table(result_to_table1_LCCDE(paper_runs_LCCDE["CICIDS2017"]))
                st.table(result_to_table2_LCCDE(paper_runs_LCCDE["CICIDS2017"]))

            with right:
                st.write("Car Hacking Dataset Results")
                st.table(result_to_table1_LCCDE(paper_runs_LCCDE["CarHacking"]))
                st.table(result_to_table2_LCCDE(paper_runs_LCCDE["CarHacking"]))
        elif rundata["model_type"] == "MTH":
            st.write("CICIDS2017 Dataset Results")
            st.table(result_to_table1_MTH(paper_runs_MTH["CICIDS2017"]))
        elif rundata["model_type"] == "Tree Based":
            left, right = st.columns(2)
            with left:
                st.write("CICIDS2017 Dataset Results")
                st.table(result_to_table1_TreeBased(paper_runs_Tree_Based["CICIDS2017"]))
            with right:
                st.write("CANIntrusion Dataset Results")
                st.table(result_to_table1_TreeBased(paper_runs_Tree_Based["CANIntrusion"]))
    else:
        st.header("Run Results")
        compareOptions = ['None']
        compareOptions += ["{} - {} - {}".format(run["rundata"]["name"], run["rundata"]["timestamp"], run["config"]["dataset"]) for run in runs["runs"]]
        compareOptions = {value: index for index, value in enumerate(compareOptions)}
        compareRun = st.selectbox("Compare Run With: ", compareOptions.keys(),index = 0)
        compareRun = compareOptions[compareRun]

        if compareRun == 0:
            st.write(list(compareOptions.keys())[currentRun])
            if runs["runs"][currentRun - 1]["rundata"]["model_type"] == "LCCDE":
                st.table(result_to_table1_LCCDE(runs["runs"][currentRun - 1]))
                st.table(result_to_table2_LCCDE(runs["runs"][currentRun - 1]))
            elif runs["runs"][currentRun - 1]["rundata"]["model_type"] == "MTH":
                st.table(result_to_table1_MTH(runs["runs"][currentRun - 1]))
            elif runs["runs"][currentRun - 1]["rundata"]["model_type"] == "Tree Based":
                st.table(result_to_table1_TreeBased(runs["runs"][currentRun - 1]))
        else:
            left, right = st.columns(2)
            with left:
                st.write(list(compareOptions.keys())[currentRun])
                if runs["runs"][currentRun - 1]["rundata"]["model_type"] == "LCCDE":
                    st.table(result_to_table1_LCCDE(runs["runs"][currentRun - 1]))
                    st.table(result_to_table2_LCCDE(runs["runs"][currentRun - 1]))
                elif runs["runs"][currentRun - 1]["rundata"]["model_type"] == "MTH":
                    st.table(result_to_table1_MTH(runs["runs"][currentRun - 1]))
                elif runs["runs"][currentRun - 1]["rundata"]["model_type"] == "Tree Based":
                    st.table(result_to_table1_TreeBased(runs["runs"][currentRun - 1]))
            with right:
                st.write(list(compareOptions.keys())[compareRun])
                if runs["runs"][compareRun - 1]["rundata"]["model_type"] == "LCCDE":
                    st.table(result_to_table1_LCCDE(runs["runs"][compareRun - 1]))
                    st.table(result_to_table2_LCCDE(runs["runs"][compareRun - 1]))
                elif runs["runs"][compareRun - 1]["rundata"]["model_type"] == "MTH":
                    st.table(result_to_table1_MTH(runs["runs"][currentRun - 1]))
                elif runs["runs"][compareRun - 1]["rundata"]["model_type"] == "Tree Based":
                    st.table(result_to_table1_TreeBased(runs["runs"][compareRun - 1]))

