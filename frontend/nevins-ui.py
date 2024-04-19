import streamlit as st
import json
import pandas as pd
from datetime import datetime
import sys
sys.path.append('../IDS-engine')
import LCCDE


#FUNCTIONS---------------------------------------------------------------------------
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
    #st.rerun()

#LOGIC CODE------------------------------------------------------------------------------------------
#get paper results
paper_runs = {}
with open('LCCDE_PAPER.json', 'r') as f:
    paper_runs = json.load(f)

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
        st.session_state.dataset = st.session_state.copied_parameters["dataset"]
        st.session_state.test_data_percent = st.session_state.copied_parameters["test_data_percent"]
        st.session_state.random_state = st.session_state.copied_parameters["random_state"]
        st.session_state.boosting_type = st.session_state.copied_parameters["boosting_type"]
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

        config["dataset"] = st.selectbox("Dataset: ", ("carHackingDataset_km", "carHackingDataset_sample_km", "CICIDS2017_km", "CICIDS2017_sample_km"), key="dataset")
        
        config["test_data_percent"] = st.slider("Test Data Percent: ", 0.01, .99, 0.2, 0.01, key="test_data_percent")

        config["random_state"] = st.number_input("Random State: ", value=0, step=1, key="random_state")

        config["boosting_type"] = st.selectbox("Boosting Type: ", ("Plain", "Ordered"), key="boosting_type")

        config["smote"] = st.text_input('SMOTE (optional): ', '{"2":1000, "4":1000}' if config["dataset"] == "CICIDS2017_km" or config["dataset"] == "CICIDS2017_sample_km" else "")

        #display run button
        if st.button("Run"):
            # Code to run when the button is clicked
            with st.spinner("Training Model..."):
                runLCCDE(config, rundata, runs)
                st.rerun()

    else:
        st.text_input('Run Name: ', '{}'.format(runs["runs"][currentRun - 1]["rundata"]["name"]), disabled=True)

        st.text_input('Timestamp: ', '{}'.format(runs["runs"][currentRun - 1]["rundata"]["timestamp"]), disabled=True)

        st.selectbox("Dataset: ",["{}".format(runs["runs"][currentRun - 1]["config"]["dataset"])], disabled=True)

        st.slider("Test Data Percent: ", 0.01, .99, runs["runs"][currentRun - 1]["config"]["test_data_percent"], 0.01, disabled=True)

        st.number_input("Random State: ", value=runs["runs"][currentRun - 1]["config"]["random_state"], step=1, disabled=True)

        st.selectbox("Boosting Type: ", [runs["runs"][currentRun - 1]["config"]["boosting_type"]], disabled=True)

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
                    "dataset": runs["runs"][currentRun - 1]["config"]["dataset"],
                    "test_data_percent": runs["runs"][currentRun - 1]["config"]["test_data_percent"],
                    "random_state": runs["runs"][currentRun - 1]["config"]["random_state"],
                    "boosting_type": runs["runs"][currentRun - 1]["config"]["boosting_type"],
                    "smote": runs["runs"][currentRun - 1]["config"]["smote"]
                }

                st.session_state.copy_parameters = True
                st.rerun()

#right 2/3 of the screen
with col2:
    if currentRun == 0:
        st.header("LCCDE Paper Results")
        left, right = st.columns(2)
        with left:
            st.write("CICIDS2017 Dataset Results")
            st.table(result_to_table1(paper_runs["CICIDS2017"]))
            st.table(result_to_table2(paper_runs["CICIDS2017"]))

        with right:
            st.write("Car Hacking Dataset Results")
            st.table(result_to_table1(paper_runs["CarHacking"]))
            st.table(result_to_table2(paper_runs["CarHacking"]))
    else:
        st.header("Run Results")
        compareOptions = ['None']
        compareOptions += ["{} - {} - {}".format(run["rundata"]["name"], run["rundata"]["timestamp"], run["config"]["dataset"]) for run in runs["runs"]]
        compareOptions = {value: index for index, value in enumerate(compareOptions)}
        compareRun = st.selectbox("Compare Run With: ", compareOptions.keys(),index = 0)
        compareRun = compareOptions[compareRun]

        if compareRun == 0:
            st.write(list(compareOptions.keys())[currentRun])
            st.table(result_to_table1(runs["runs"][currentRun - 1]))
            st.table(result_to_table2(runs["runs"][currentRun - 1]))
        else:
            left, right = st.columns(2)
            with left:
                st.write(list(compareOptions.keys())[currentRun])
                st.table(result_to_table1(runs["runs"][currentRun - 1]))
                st.table(result_to_table2(runs["runs"][currentRun - 1]))
            with right:
                st.write(list(compareOptions.keys())[compareRun])
                st.table(result_to_table1(runs["runs"][compareRun - 1]))
                st.table(result_to_table2(runs["runs"][compareRun - 1]))

