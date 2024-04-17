import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score, precision_score, recall_score, f1_score
import lightgbm as lgb
import catboost as cbt
import xgboost as xgb
import time
import json
from river import stream
from statistics import mode

#data I need
config = {
    #two options carHackingDataset_sample_km && CICIDS2017_sample_km
    "dataset": "carHackingDataset_sample_km",
    "smote": None #{2:1000,4:1000} for CICIDS2017
}

def run(config):
    #settup result
    result = {
        "LightGBM_accuracy": "",
        "LightGBM_precision": "", 
        "LightGBM_recall": "",
        "LightGBM_F1_score": "",
        "LightGBM_F1_classes_score": "",
        
        "XGBoost_accuracy": "",
        "XGBoost_precision": "", 
        "XGBoost_recall": "",
        "XGBoost_F1_score": "",
        "XGBoost_F1_classes_score": "",

        "CatBoost_accuracy": "",
        "CatBoost_precision": "", 
        "CatBoost_recall": "",
        "CatBoost_F1_score": "",
        "CatBoost_F1_classes_score": "",

        "LCCDE_accuracy": "",
        "LCCDE_precision": "", 
        "LCCDE_recall": "",
        "LCCDE_F1_score": "",
        "LCCDE_F1_classes_score": "",
    }

    df = pd.read_csv('{}/../data/{}.csv'.format(__file__, config['dataset']))
    X = df.drop(['Label'],axis=1)
    y = df['Label']
    X_train, X_test, y_train, y_test = train_test_split(X,y, train_size = 1 - config["test_data_percent"], test_size = config["test_data_percent"], random_state = config["random_state"]) #shuffle=False
    from imblearn.over_sampling import SMOTE
    # print(pd.Series(y_train).value_counts()) #prints label values for smote
    if(config["smote"] != None and config["smote"] != ""):
        config["smote"]  = json.loads(config["smote"], parse_int=int)
        config["smote"] = {int(key): value for key, value in config["smote"].items()}
        smote=SMOTE(n_jobs=1,sampling_strategy=config["smote"])
        X_train, y_train = smote.fit_resample(X_train, y_train)

    #LightGBM
    # Train the LightGBM algorithm
    import lightgbm as lgb
    lg = lgb.LGBMClassifier()
    lg.fit(X_train, y_train)
    y_pred = lg.predict(X_test)
    #print(classification_report(y_test,y_pred))
    result["LightGBM_accuracy"] = accuracy_score(y_test, y_pred)
    result["LightGBM_precision"] = precision_score(y_test, y_pred, average='weighted')
    result["LightGBM_recall"] = recall_score(y_test, y_pred, average='weighted')
    result["LightGBM_F1_score"] = f1_score(y_test, y_pred, average='weighted')
    lg_f1=f1_score(y_test, y_pred, average=None)
    result["LightGBM_F1_classes_score"] = lg_f1.tolist()

    # Plot the confusion matrix
    # cm=confusion_matrix(y_test,y_pred)
    # f,ax=plt.subplots(figsize=(5,5))
    # sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
    # plt.xlabel("y_pred")
    # plt.ylabel("y_true")
    # plt.show()

    #XGBoost
    # Train the XGBoost algorithm
    import xgboost as xgb
    xg = xgb.XGBClassifier()

    X_train_x = X_train.values
    X_test_x = X_test.values

    xg.fit(X_train_x, y_train)

    y_pred = xg.predict(X_test_x)
    #print(classification_report(y_test,y_pred))
    result["XGBoost_accuracy"] = accuracy_score(y_test, y_pred)
    result["XGBoost_precision"] = precision_score(y_test, y_pred, average='weighted')
    result["XGBoost_recall"] = recall_score(y_test, y_pred, average='weighted')
    result["XGBoost_F1_score"] = f1_score(y_test, y_pred, average='weighted')
    xg_f1=f1_score(y_test, y_pred, average=None)
    result["XGBoost_F1_classes_score"] = xg_f1.tolist()

    # Plot the confusion matrix
    # cm=confusion_matrix(y_test,y_pred)
    # f,ax=plt.subplots(figsize=(5,5))
    # sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
    # plt.xlabel("y_pred")
    # plt.ylabel("y_true")
    # plt.show()

    #CatBoost
    # Train the CatBoost algorithm
    import catboost as cbt
    cb = cbt.CatBoostClassifier(verbose=0,boosting_type=config["boosting_type"])
    #cb = cbt.CatBoostClassifier()

    cb.fit(X_train, y_train)
    y_pred = cb.predict(X_test)
    #print(classification_report(y_test,y_pred))
    result["CatBoost_accuracy"] = accuracy_score(y_test, y_pred)
    result["CatBoost_precision"] = precision_score(y_test, y_pred, average='weighted')
    result["CatBoost_recall"] = recall_score(y_test, y_pred, average='weighted')
    result["CatBoost_F1_score"] = f1_score(y_test, y_pred, average='weighted')
    cb_f1=f1_score(y_test, y_pred, average=None)
    result["CatBoost_F1_classes_score"] = cb_f1.tolist()

    # Plot the confusion matrix
    # cm=confusion_matrix(y_test,y_pred)
    # f,ax=plt.subplots(figsize=(5,5))
    # sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
    # plt.xlabel("y_pred")
    # plt.ylabel("y_true")
    # plt.show()

    #LCCDE Stuff
    # Leading model list for each class
    model=[]
    for i in range(len(lg_f1)):
        if max(lg_f1[i],xg_f1[i],cb_f1[i]) == lg_f1[i]:
            model.append(lg)
        elif max(lg_f1[i],xg_f1[i],cb_f1[i]) == xg_f1[i]:
            model.append(xg)
        else:
            model.append(cb)

    def LCCDE(X_test, y_test, m1, m2, m3):
        i = 0
        t = []
        m = []
        yt = []
        yp = []
        l = []
        pred_l = []
        pro_l = []

        # For each class (normal or a type of attack), find the leader model
        for xi, yi in stream.iter_pandas(X_test, y_test):

            xi2=np.array(list(xi.values()))
            y_pred1 = m1.predict(xi2.reshape(1, -1))      # model 1 (LightGBM) makes a prediction on text sample xi
            y_pred1 = int(y_pred1[0])
            y_pred2 = m2.predict(xi2.reshape(1, -1))      # model 2 (XGBoost) makes a prediction on text sample xi
            y_pred2 = int(y_pred2[0])
            y_pred3 = m3.predict(xi2.reshape(1, -1))      # model 3 (Catboost) makes a prediction on text sample xi
            y_pred3 = int(y_pred3[0])

            p1 = m1.predict_proba(xi2.reshape(1, -1))     # The prediction probability (confidence) list of model 1 
            p2 = m2.predict_proba(xi2.reshape(1, -1))     # The prediction probability (confidence) list of model 2  
            p3 = m3.predict_proba(xi2.reshape(1, -1))     # The prediction probability (confidence) list of model 3  

            # Find the highest prediction probability among all classes for each ML model
            y_pred_p1 = np.max(p1)
            y_pred_p2 = np.max(p2)
            y_pred_p3 = np.max(p3)

            if y_pred1 == y_pred2 == y_pred3: # If the predicted classes of all the three models are the same
                y_pred = y_pred1 # Use this predicted class as the final predicted class

            elif y_pred1 != y_pred2 != y_pred3: # If the predicted classes of all the three models are different
                # For each prediction model, check if the predicted class’s original ML model is the same as its leader model
                if model[y_pred1]==m1: # If they are the same and the leading model is model 1 (LightGBM)
                    l.append(m1)
                    pred_l.append(y_pred1) # Save the predicted class
                    pro_l.append(y_pred_p1) # Save the confidence

                if model[y_pred2]==m2: # If they are the same and the leading model is model 2 (XGBoost)
                    l.append(m2)
                    pred_l.append(y_pred2)
                    pro_l.append(y_pred_p2)

                if model[y_pred3]==m3: # If they are the same and the leading model is model 3 (CatBoost)
                    l.append(m3)
                    pred_l.append(y_pred3)
                    pro_l.append(y_pred_p3)

                if len(l)==0: # Avoid empty probability list
                    pro_l=[y_pred_p1,y_pred_p2,y_pred_p3]

                elif len(l)==1: # If only one pair of the original model and the leader model for each predicted class is the same
                    y_pred=pred_l[0] # Use the predicted class of the leader model as the final prediction class

                else: # If no pair or multiple pairs of the original prediction model and the leader model for each predicted class are the same
                    max_p = max(pro_l) # Find the highest confidence
                    
                    # Use the predicted class with the highest confidence as the final prediction class
                    if max_p == y_pred_p1:
                        y_pred = y_pred1
                    elif max_p == y_pred_p2:
                        y_pred = y_pred2
                    else:
                        y_pred = y_pred3  
            
            else: # If two predicted classes are the same and the other one is different
                n = mode([y_pred1,y_pred2,y_pred3]) # Find the predicted class with the majority vote
                y_pred = model[n].predict(xi2.reshape(1, -1)) # Use the predicted class of the leader model as the final prediction class
                y_pred = int(y_pred[0]) 

            yt.append(yi)
            yp.append(y_pred) # Save the predicted classes for all tested samples
        return yt, yp
    
    # Implementing LCCDE
    yt, yp = LCCDE(X_test, y_test, m1 = lg, m2 = xg, m3 = cb)

    # The performance of the proposed lCCDE model
    result["LCCDE_accuracy"] = accuracy_score(yt, yp)
    result["LCCDE_precision"] = precision_score(yt, yp, average='weighted')
    result["LCCDE_recall"] = recall_score(yt, yp, average='weighted')
    result["LCCDE_F1_score"] = f1_score(yt, yp, average='weighted')
    result["LCCDE_F1_classes_score"] = f1_score(yt, yp, average=None).tolist()
    

    #Comparison: The F1-scores for each base model
    #print("F1 of LightGBM for each type of attack: "+ str(lg_f1))
    #print("F1 of XGBoost for each type of attack: "+ str(xg_f1))
    #print("F1 of CatBoost for each type of attack: "+ str(cb_f1))

    return result