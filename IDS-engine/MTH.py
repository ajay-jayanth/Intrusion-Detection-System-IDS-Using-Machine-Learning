import warnings
warnings.filterwarnings("ignore")

import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,precision_recall_fscore_support
from sklearn.metrics import f1_score,roc_auc_score
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
from xgboost import plot_importance

# Define inputs dictionary for hyperparameters
outputs = {}

# Random Forest Classifier
config = {
    'n_estimators': {'min': 10, 'max': 200, 'step': 1},
    'max_depth': {'min': 5, 'max': 50, 'step': 1},
    'max_features': {'min': 1, 'max': 20, 'step': 1},
    'min_samples_split': {'min': 2, 'max': 11, 'step': 1},
    'min_samples_leaf': {'min': 1, 'max': 11, 'step': 1},
    'criterion': ['gini', 'entropy'], #Remove this one (aka add it back)
    'learning_rate': {'mean': 0.01, 'std': 0.9}
}

def run(config):
    outputs = {}
    #Read dataset
    df = pd.read_csv('{}/../data/{}.csv'.format(__file__, config['dataset']))
    # The results in this code is based on the original CICIDS2017 dataset. Please go to cell [21] if you work on the sampled dataset. 

    # Z-score normalization
    features = df.dtypes[df.dtypes != 'object'].index
    df[features] = df[features].apply(
        lambda x: (x - x.mean()) / (x.std()))
    # Fill empty values by 0
    df = df.fillna(0)

    labelencoder = LabelEncoder()
    df.iloc[:, -1] = labelencoder.fit_transform(df.iloc[:, -1])

    # retain the minority class instances and sample the majority class instances
    df_minor = df[(df['Label']==6)|(df['Label']==1)|(df['Label']==4)]
    df_major = df.drop(df_minor.index)

    X = df_major.drop(['Label'],axis=1) 
    y = df_major.iloc[:, -1].values.reshape(-1,1)
    y=np.ravel(y)

    X = df_major.drop(['Label'],axis=1) 
    y = df_major.iloc[:, -1].values.reshape(-1,1)
    y=np.ravel(y)

    # use k-means to cluster the data samples and select a proportion of data from each cluster
    from sklearn.cluster import MiniBatchKMeans
    kmeans = MiniBatchKMeans(n_clusters=1000, random_state=0).fit(X)

    klabel=kmeans.labels_
    df_major['klabel']=klabel

    cols = list(df_major)
    cols.insert(78, cols.pop(cols.index('Label')))
    df_major = df_major.loc[:, cols]

    def typicalSampling(group):
        name = group.name
        frac = 0.008
        return group.sample(frac=frac)

    result = df_major.groupby(
        'klabel', group_keys=False
    ).apply(typicalSampling)

    result = result.drop(['klabel'],axis=1)
   #print(type(result))
    result = pd.concat([result, df_minor], ignore_index=True)

    # Read the sampled dataset
    df = pd.read_csv('{}/../data/{}_km.csv'.format(__file__, config['dataset']))

    features = df.dtypes[df.dtypes != 'object'].index

    X = df.drop(['Label'],axis=1).values
    y = df.iloc[:, -1].values.reshape(-1,1)
    y=np.ravel(y)

    X_train, X_test, y_train, y_test = train_test_split(X,y, train_size = 0.8, test_size = 0.2, random_state = 0,stratify = y)

    from sklearn.feature_selection import mutual_info_classif
    importances = mutual_info_classif(X_train, y_train)

    # calculate the sum of importance scores
    f_list = sorted(zip(map(lambda x: round(x, 4), importances), features), reverse=True)
    Sum = 0
    fs = []
    for i in range(0, len(f_list)):
        Sum = Sum + f_list[i][0]
        fs.append(f_list[i][1])


    # select the important features from top to bottom until the accumulated importance reaches 90%
    f_list2 = sorted(zip(map(lambda x: round(x, 4), importances/Sum), features), reverse=True)
    Sum2 = 0
    fs = []
    for i in range(0, len(f_list2)):
        Sum2 = Sum2 + f_list2[i][0]
        fs.append(f_list2[i][1])
        if Sum2>=0.9:
            break        

    X_fs = df[fs].values

    from FCBF_module import FCBF, FCBFK, FCBFiP, get_i
    fcbf = FCBFK(k = 20)


    X_fss = fcbf.fit_transform(X_fs,y)

    X_train, X_test, y_train, y_test = train_test_split(X_fss,y, train_size = 0.8, test_size = 0.2, random_state = 0,stratify = y)

    from imblearn.over_sampling import SMOTE
    smote=SMOTE(n_jobs=-1,sampling_strategy={2:1000,4:1000})
    X_train, y_train = smote.fit_resample(X_train, y_train)




    from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
    from sklearn.model_selection import cross_val_score, StratifiedKFold
    def objective(params):
        params = {
            'n_estimators': int(params['n_estimators']), 
            'max_depth': int(params['max_depth']),
            'learning_rate':  abs(float(params['learning_rate'])),

        }
        clf = xgb.XGBClassifier( **params)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        score = accuracy_score(y_test, y_pred)

        return {'loss':-score, 'status': STATUS_OK }

    space = {
        'n_estimators': hp.quniform('n_estimators', config['n_estimators']['min'],
                                    config['n_estimators']['max'],
                                    config['n_estimators']['step']),
        'max_depth': hp.quniform('max_depth', config['max_depth']['min'],
                                config['max_depth']['max'],
                                config['max_depth']['step']),
        'learning_rate': hp.normal('learning_rate', config['learning_rate']['mean'],
                                config['learning_rate']['std'])
    }

    best = fmin(fn=objective,
                space=space,
                algo=tpe.suggest,
                max_evals=20)
   #print("XGBoost: Hyperopt estimated optimum {}".format(best))



    xg = xgb.XGBClassifier(learning_rate= 0.7340229699980686, n_estimators = 70, max_depth = 14)
    xg.fit(X_train,y_train)
    xg_score=xg.score(X_test,y_test)
    y_predict=xg.predict(X_test)
    y_true=y_test
   #print('Accuracy of XGBoost: '+ str(xg_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
   #print('Precision of XGBoost: '+(str(precision)))
   #print('Recall of XGBoost: '+(str(recall)))
   #print('F1-score of XGBoost: '+(str(fscore)))
    #print(classification_report(y_true,y_predict))

    outputs.update({'xgboost_hpo':{'best_param':best,'accuracy':str(xg_score),'precision':str(precision),'f1':str(fscore),'recall': str(recall)}})


    xg_train=xg.predict(X_train)
    xg_test=xg.predict(X_test)


    rf = RandomForestClassifier(random_state = 0)
    rf.fit(X_train,y_train) 
    rf_score=rf.score(X_test,y_test)
    y_predict=rf.predict(X_test)
    y_true=y_test
   #print('Accuracy of RF: '+ str(rf_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
   #print('Precision of RF: '+(str(precision)))
   #print('Recall of RF: '+(str(recall)))
   #print('F1-score of RF: '+(str(fscore)))
    #print(classification_report(y_true,y_predict))
    outputs.update({'random_forest':{'accuracy':str(xg_score),'precision':str(precision),'f1':str(fscore),'recall': str(recall)}})


    # Hyperparameter optimization of random forest
    from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
    from sklearn.model_selection import cross_val_score, StratifiedKFold
    # Define the objective function
    def objective(params):
        params = {
            'n_estimators': int(params['n_estimators']), 
            'max_depth': int(params['max_depth']),
            'max_features': int(params['max_features']),
            "min_samples_split":int(params['min_samples_split']),
            "min_samples_leaf":int(params['min_samples_leaf']),
            "criterion":str(params['criterion'])
        }
        clf = RandomForestClassifier( **params)
        clf.fit(X_train,y_train)
        score=clf.score(X_test,y_test)

        return {'loss':-score, 'status': STATUS_OK }
    # Define the hyperparameter configuration space
    space = {
        'n_estimators': hp.quniform('n_estimators', config['n_estimators']['min'],
                                    config['n_estimators']['max'],
                                    config['n_estimators']['step']),
        'max_depth': hp.quniform('max_depth', config['max_depth']['min'],
                                config['max_depth']['max'],
                                config['max_depth']['step']),
        'max_features': hp.quniform('max_features', config['max_features']['min'],
                                    config['max_features']['max'],
                                    config['max_features']['step']),
        'min_samples_split': hp.quniform('min_samples_split', config['min_samples_split']['min'],
                                        config['min_samples_split']['max'],
                                        config['min_samples_split']['step']),
        'min_samples_leaf': hp.quniform('min_samples_leaf', config['min_samples_leaf']['min'],
                                        config['min_samples_leaf']['max'],
                                        config['min_samples_leaf']['step']),
        'criterion': hp.choice('criterion', config['criterion'])
    }

    best = fmin(fn=objective,
                space=space,
                algo=tpe.suggest,
                max_evals=20)
   #print("Random Forest: Hyperopt estimated optimum {}".format(best))


    rf_hpo = RandomForestClassifier(n_estimators = 71, min_samples_leaf = 1, max_depth = 46, min_samples_split = 9, max_features = 20, criterion = 'entropy')
    rf_hpo.fit(X_train,y_train)
    rf_score=rf_hpo.score(X_test,y_test)
    y_predict=rf_hpo.predict(X_test)
    y_true=y_test
   #print('Accuracy of RF: '+ str(rf_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
   #print('Precision of RF: '+(str(precision)))
   #print('Recall of RF: '+(str(recall)))
   #print('F1-score of RF: '+(str(fscore)))
    #print(classification_report(y_true,y_predict))
    outputs.update({'random_forest_hpo':{'best_param':best,'accuracy':str(xg_score),'precision':str(precision),'f1':str(fscore),'recall': str(recall)}})

    rf_train=rf_hpo.predict(X_train)
    rf_test=rf_hpo.predict(X_test)



    dt = DecisionTreeClassifier(random_state = 0)
    dt.fit(X_train,y_train) 
    dt_score=dt.score(X_test,y_test)
    y_predict=dt.predict(X_test)
    y_true=y_test
   #print('Accuracy of DT: '+ str(dt_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
   #print('Precision of DT: '+(str(precision)))
   #print('Recall of DT: '+(str(recall)))
   #print('F1-score of DT: '+(str(fscore)))
    #print(classification_report(y_true,y_predict))
    outputs.update({'dt':{'accuracy':str(xg_score),'precision':str(precision),'f1':str(fscore),'recall': str(recall)}})


    # Hyperparameter optimization of decision tree
    from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
    from sklearn.model_selection import cross_val_score, StratifiedKFold
    # Define the objective function
    def objective(params):
        params = {
            'max_depth': int(params['max_depth']),
            'max_features': int(params['max_features']),
            "min_samples_split":int(params['min_samples_split']),
            "min_samples_leaf":int(params['min_samples_leaf']),
            "criterion":str(params['criterion'])
        }
        clf = DecisionTreeClassifier( **params)
        clf.fit(X_train,y_train)
        score=clf.score(X_test,y_test)

        return {'loss':-score, 'status': STATUS_OK }
    # Define the hyperparameter configuration space
    dt_space = {
        'max_depth': hp.quniform('max_depth', config['max_depth']['min'], config['max_depth']['max'], config['max_depth']['step']),
        'max_features': hp.quniform('max_features', config['max_features']['min'], config['max_features']['max'], config['max_features']['step']),
        'min_samples_split': hp.quniform('min_samples_split', config['min_samples_split']['min'], config['min_samples_split']['max'], config['min_samples_split']['step']),
        'min_samples_leaf': hp.quniform('min_samples_leaf', config['min_samples_leaf']['min'], config['min_samples_leaf']['max'], config['min_samples_leaf']['step']),
        'criterion': hp.choice('criterion', config['criterion'])
    }

    best = fmin(fn=objective,
                space=space,
                algo=tpe.suggest,
                max_evals=50)
   #print("Decision tree: Hyperopt estimated optimum {}".format(best))


    dt_hpo = DecisionTreeClassifier(min_samples_leaf = 2, max_depth = 47, min_samples_split = 3, max_features = 19, criterion = 'gini')
    dt_hpo.fit(X_train,y_train)
    dt_score=dt_hpo.score(X_test,y_test)
    y_predict=dt_hpo.predict(X_test)
    y_true=y_test
   #print('Accuracy of DT: '+ str(dt_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
   #print('Precision of DT: '+(str(precision)))
   #print('Recall of DT: '+(str(recall)))
   #print('F1-score of DT: '+(str(fscore)))
    #print(classification_report(y_true,y_predict))
    outputs.update({'decision_tree_hpo':{'best_param':best,'accuracy':str(xg_score),'precision':str(precision),'f1':str(fscore),'recall': str(recall)}})

    dt_train=dt_hpo.predict(X_train)
    dt_test=dt_hpo.predict(X_test)


    et = ExtraTreesClassifier(random_state = 0)
    et.fit(X_train,y_train) 
    et_score=et.score(X_test,y_test)
    y_predict=et.predict(X_test)
    y_true=y_test
   #print('Accuracy of ET: '+ str(et_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
   #print('Precision of ET: '+(str(precision)))
   #print('Recall of ET: '+(str(recall)))
   #print('F1-score of ET: '+(str(fscore)))
    #print(classification_report(y_true,y_predict))
    outputs.update({'extra_trees':{'accuracy':str(xg_score),'precision':str(precision),'f1':str(fscore),'recall': str(recall)}})



    # Hyperparameter optimization of extra trees
    from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
    from sklearn.model_selection import cross_val_score, StratifiedKFold
    # Define the objective function
    def objective(params):
        params = {
            'n_estimators': int(params['n_estimators']), 
            'max_depth': int(params['max_depth']),
            'max_features': int(params['max_features']),
            "min_samples_split":int(params['min_samples_split']),
            "min_samples_leaf":int(params['min_samples_leaf']),
            "criterion":str(params['criterion'])
        }
        clf = ExtraTreesClassifier( **params)
        clf.fit(X_train,y_train)
        score=clf.score(X_test,y_test)

        return {'loss':-score, 'status': STATUS_OK }
    # Define the hyperparameter configuration space
    space = {
        'n_estimators': hp.quniform('n_estimators', config['n_estimators']['min'],
                                    config['n_estimators']['max'],
                                    config['n_estimators']['step']),
        'max_depth': hp.quniform('max_depth', config['max_depth']['min'],
                                config['max_depth']['max'],
                                config['max_depth']['step']),
        'max_features': hp.quniform('max_features', config['max_features']['min'],
                                    config['max_features']['max'],
                                    config['max_features']['step']),
        'min_samples_split': hp.quniform('min_samples_split', config['min_samples_split']['min'],
                                        config['min_samples_split']['max'],
                                        config['min_samples_split']['step']),
        'min_samples_leaf': hp.quniform('min_samples_leaf', config['min_samples_leaf']['min'],
                                        config['min_samples_leaf']['max'],
                                        config['min_samples_leaf']['step']),
        'criterion': hp.choice('criterion', config['criterion'])
    }

    best = fmin(fn=objective,
                space=space,
                algo=tpe.suggest,
                max_evals=20)
   #print("Random Forest: Hyperopt estimated optimum {}".format(best))





    et_hpo = ExtraTreesClassifier(n_estimators = 53, min_samples_leaf = 1, max_depth = 31, min_samples_split = 5, max_features = 20, criterion = 'entropy')
    et_hpo.fit(X_train,y_train) 
    et_score=et_hpo.score(X_test,y_test)
    y_predict=et_hpo.predict(X_test)
    y_true=y_test
   #print('Accuracy of ET: '+ str(et_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
   #print('Precision of ET: '+(str(precision)))
   #print('Recall of ET: '+(str(recall)))
   #print('F1-score of ET: '+(str(fscore)))
    #print(classification_report(y_true,y_predict))
    outputs.update({'extra_trees_hpo':{'best_param':best,'accuracy':str(xg_score),'precision':str(precision),'f1':str(fscore),'recall': str(recall)}})


    et_train=et_hpo.predict(X_train)
    et_test=et_hpo.predict(X_test)


    base_predictions_train = pd.DataFrame( {
        'DecisionTree': dt_train.ravel(),
        'RandomForest': rf_train.ravel(),
        'ExtraTrees': et_train.ravel(),
        'XgBoost': xg_train.ravel(),
        })
    base_predictions_train.head(5)


    dt_train=dt_train.reshape(-1, 1)
    et_train=et_train.reshape(-1, 1)
    rf_train=rf_train.reshape(-1, 1)
    xg_train=xg_train.reshape(-1, 1)
    dt_test=dt_test.reshape(-1, 1)
    et_test=et_test.reshape(-1, 1)
    rf_test=rf_test.reshape(-1, 1)
    xg_test=xg_test.reshape(-1, 1)


    x_train = np.concatenate(( dt_train, et_train, rf_train, xg_train), axis=1)
    x_test = np.concatenate(( dt_test, et_test, rf_test, xg_test), axis=1)


    stk = xgb.XGBClassifier().fit(x_train, y_train)
    y_predict=stk.predict(x_test)
    y_true=y_test
    stk_score=accuracy_score(y_true,y_predict)
   #print('Accuracy of Stacking: '+ str(stk_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
   #print('Precision of Stacking: '+(str(precision)))
   #print('Recall of Stacking: '+(str(recall)))
   #print('F1-score of Stacking: '+(str(fscore)))
    #print(classification_report(y_true,y_predict))
    outputs.update({'stack':{'accuracy':str(xg_score),'precision':str(precision),'f1':str(fscore),'recall': str(recall)}})


    from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
    from sklearn.model_selection import cross_val_score, StratifiedKFold
    def objective(params):
        params = {
            'n_estimators': int(params['n_estimators']), 
            'max_depth': int(params['max_depth']),
            'learning_rate':  abs(float(params['learning_rate'])),

        }
        clf = xgb.XGBClassifier( **params)
        clf.fit(x_train, y_train)
        y_pred = clf.predict(x_test)
        score = accuracy_score(y_test, y_pred)

        return {'loss':-score, 'status': STATUS_OK }

    space = {
        'n_estimators': hp.quniform('n_estimators', config['n_estimators']['min'],
                                    config['n_estimators']['max'],
                                    config['n_estimators']['step']),
        'max_depth': hp.quniform('max_depth', config['max_depth']['min'],
                                config['max_depth']['max'],
                                config['max_depth']['step']),
        'learning_rate': hp.normal('learning_rate', config['learning_rate']['mean'],
                                                    config['learning_rate']['std'])
    }

    best = fmin(fn=objective,
                space=space,
                algo=tpe.suggest,
                max_evals=20)
   #print("Stacking: Hyperopt estimated optimum {}".format(best))



    xg = xgb.XGBClassifier(learning_rate= 0.19229249758051492, n_estimators = 30, max_depth = 36)
    xg.fit(x_train,y_train)
    xg_score=xg.score(x_test,y_test)
    y_predict=xg.predict(x_test)
    y_true=y_test
   #print('Accuracy of XGBoost: '+ str(xg_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted') 
   #print('Precision of XGBoost: '+(str(precision)))
   #print('Recall of XGBoost: '+(str(recall)))
   #print('F1-score of XGBoost: '+(str(fscore)))
    #print(classification_report(y_true,y_predict))
    outputs.update({'stack_hpo':{'best_param':best,'accuracy':str(xg_score),'precision':str(precision),'f1':str(fscore),'recall': str(recall)}})

    df=result
    df1 = df[df['Label'] != 5]
    df1['Label'][df1['Label'] > 0] = 1
    # df1.to_csv('/kaggle/working/CICIDS2017_sample_km_without_portscan.csv',index=0)

    df2 = df[df['Label'] == 5]
    df2['Label'][df2['Label'] == 5] = 1
    # df2.to_csv('/kaggle/working/CICIDS2017_sample_km_portscan.csv',index=0)

    features = df1.drop(['Label'],axis=1).dtypes[df1.dtypes != 'object'].index
    df1[features] = df1[features].apply(
        lambda x: (x - x.mean()) / (x.std()))
    df2[features] = df2[features].apply(
        lambda x: (x - x.mean()) / (x.std()))
    df1 = df1.fillna(0)
    df2 = df2.fillna(0)

    df2p=df1[df1['Label']==0]
    df2pp=df2p.sample(n=None, frac=1255/18225, replace=False, weights=None, random_state=None, axis=0)
    df2=pd.concat([df2, df2pp])

    df = pd.concat([df1, df2], ignore_index=True)

    X = df.drop(['Label'],axis=1) .values
    y = df.iloc[:, -1].values.reshape(-1,1)
    y=np.ravel(y)
    pd.Series(y).value_counts()


    from sklearn.feature_selection import mutual_info_classif
    importances = mutual_info_classif(X, y)


    # calculate the sum of importance scores
    f_list = sorted(zip(map(lambda x: round(x, 4), importances), features), reverse=True)
    Sum = 0
    fs = []
    for i in range(0, len(f_list)):
        Sum = Sum + f_list[i][0]
        fs.append(f_list[i][1])


    # select the important features from top to bottom until the accumulated importance reaches 90%
    f_list2 = sorted(zip(map(lambda x: round(x, 4), importances/Sum), features), reverse=True)
    Sum2 = 0
    fs = []
    for i in range(0, len(f_list2)):
        Sum2 = Sum2 + f_list2[i][0]
        fs.append(f_list2[i][1])
        if Sum2>=0.9:
            break        


    X_fs = df[fs].values


    from FCBF_module import FCBF, FCBFK, FCBFiP, get_i
    fcbf = FCBFK(k = 20)
    #fcbf.fit(X_fs, y)

    X_fss = fcbf.fit_transform(X_fs,y)



    from sklearn.decomposition import KernelPCA
    kpca = KernelPCA(n_components = 10, kernel = 'rbf')
    kpca.fit(X_fss, y)
    X_kpca = kpca.transform(X_fss)

    # from sklearn.decomposition import PCA
    # kpca = PCA(n_components = 10)
    # kpca.fit(X_fss, y)
    # X_kpca = kpca.transform(X_fss)



    X_train = X_kpca[:len(df1)]
    y_train = y[:len(df1)]
    X_test = X_kpca[len(df1):]
    y_test = y[len(df1):]



    from imblearn.over_sampling import SMOTE
    smote=SMOTE(n_jobs=-1,sampling_strategy={1:18225})
    X_train, y_train = smote.fit_resample(X_train, y_train)

    def CL_kmeans(X_train, X_test, y_train, y_test,n,b=100):
        km_cluster = MiniBatchKMeans(n_clusters=n,batch_size=b)
        result = km_cluster.fit_predict(X_train)
        result2 = km_cluster.predict(X_test)

        count=0
        a=np.zeros(n)
        b=np.zeros(n)
        for v in range(0,n):
            for i in range(0,len(y_train)):
                if result[i]==v:
                    if y_train[i]==1:
                        a[v]=a[v]+1
                    else:
                        b[v]=b[v]+1
        list1=[]
        list2=[]
        for v in range(0,n):
            if a[v]<=b[v]:
                list1.append(v)
            else: 
                list2.append(v)
        for v in range(0,len(y_test)):
            if result2[v] in list1:
                result2[v]=0
            elif result2[v] in list2:
                result2[v]=1
            else:
                pass
               #print("-1")
        #print(classification_report(y_test, result2))




    CL_kmeans(X_train, X_test, y_train, y_test, 8)

    np.int = np.int32


    #Hyperparameter optimization by BO-GP
    from skopt.space import Real, Integer
    from skopt.utils import use_named_args
    from sklearn import metrics

    space  = [Integer(2, 50, name='n_clusters')]
    @use_named_args(space)
    def objective(**params):
        km_cluster = MiniBatchKMeans(batch_size=100, **params)
        n=params['n_clusters']
        
        result = km_cluster.fit_predict(X_train)
        result2 = km_cluster.predict(X_test)

        count=0
        a=np.zeros(n)
        b=np.zeros(n)
        for v in range(0,n):
            for i in range(0,len(y_train)):
                if result[i]==v:
                    if y_train[i]==1:
                        a[v]=a[v]+1
                    else:
                        b[v]=b[v]+1
        list1=[]
        list2=[]
        for v in range(0,n):
            if a[v]<=b[v]:
                list1.append(v)
            else: 
                list2.append(v)
        for v in range(0,len(y_test)):
            if result2[v] in list1:
                result2[v]=0
            elif result2[v] in list2:
                result2[v]=1
            else:
                pass
               #print("-1")
        cm=metrics.accuracy_score(y_test,result2)
       #print(str(n)+" "+str(cm))
        return (1-cm)
    from skopt import gp_minimize
    import time
    t1=time.time()
    res_gp = gp_minimize(objective, space, n_calls=20, random_state=0)
    t2=time.time()
   #print(t2-t1)
   #print("Best score=%.4f" % (1-res_gp.fun))
   #print("""Best parameters: n_clusters=%d""" % (res_gp.x[0]))


    #Hyperparameter optimization by BO-TPE
    from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
    from sklearn.model_selection import cross_val_score, StratifiedKFold
    from sklearn.cluster import MiniBatchKMeans
    from sklearn import metrics

    def objective(params):
        params = {
            'n_clusters': int(params['n_clusters']), 
        }
        km_cluster = MiniBatchKMeans(batch_size=100, **params)
        n=params['n_clusters']
        
        result = km_cluster.fit_predict(X_train)
        result2 = km_cluster.predict(X_test)

        count=0
        a=np.zeros(n)
        b=np.zeros(n)
        for v in range(0,n):
            for i in range(0,len(y_train)):
                if result[i]==v:
                    if y_train[i]==1:
                        a[v]=a[v]+1
                    else:
                        b[v]=b[v]+1
        list1=[]
        list2=[]
        for v in range(0,n):
            if a[v]<=b[v]:
                list1.append(v)
            else: 
                list2.append(v)
        for v in range(0,len(y_test)):
            if result2[v] in list1:
                result2[v]=0
            elif result2[v] in list2:
                result2[v]=1
            else:
                pass
               #print("-1")
        score=metrics.accuracy_score(y_test,result2)
       #print(str(params['n_clusters'])+" "+str(score))
        return {'loss':1-score, 'status': STATUS_OK }
    space = {
        'n_clusters': hp.quniform('n_clusters', 2, 50, 1),
    }

    best = fmin(fn=objective,
                space=space,
                algo=tpe.suggest,
                max_evals=20)
   #print("Random Forest: Hyperopt estimated optimum {}".format(best))


    CL_kmeans(X_train, X_test, y_train, y_test, 16)
    
    return {
        "random_forest_accuracy": float(outputs["random_forest"]["accuracy"]),
        "random_forest_precision": float(outputs["random_forest"]["precision"]),
        "random_forest_F1": float(outputs["random_forest"]["f1"]),
        "random_forest_recall": float(outputs["random_forest"]["recall"]),

        "random_forest_hpo_accuracy": float(outputs["random_forest_hpo"]["accuracy"]),
        "random_forest_hpo_precision": float(outputs["random_forest_hpo"]["precision"]),
        "random_forest_hpo_F1": float(outputs["random_forest_hpo"]["f1"]),
        "random_forest_hpo_recall": float(outputs["random_forest_hpo"]["recall"]),

        "decision_tree_accuracy": float(outputs["dt"]["accuracy"]),
        "decision_tree_precision": float(outputs["dt"]["precision"]),
        "decision_tree_F1": float(outputs["dt"]["f1"]),
        "decision_tree_recall": float(outputs["dt"]["recall"]),

        "decision_tree_hpo_accuracy": float(outputs["decision_tree_hpo"]["accuracy"]),
        "decision_tree_hpo_precision": float(outputs["decision_tree_hpo"]["precision"]),
        "decision_tree_hpo_F1": float(outputs["decision_tree_hpo"]["f1"]),
        "decision_tree_hpo_recall": float(outputs["decision_tree_hpo"]["recall"]),

        "extra_trees_accuracy": float(outputs["extra_trees"]["accuracy"]), 
        "extra_trees_precision": float(outputs["extra_trees"]["precision"]), 
        "extra_trees_F1": float(outputs["extra_trees"]["f1"]), 
        "extra_trees_recall": float(outputs["extra_trees"]["recall"]), 

        "extra_trees_hpo_accuracy": float(outputs["extra_trees_hpo"]["accuracy"]),
        "extra_trees_hpo_precision": float(outputs["extra_trees_hpo"]["precision"]),
        "extra_trees_hpo_F1": float(outputs["extra_trees_hpo"]["f1"]),
        "extra_trees_hpo_recall": float(outputs["extra_trees_hpo"]["recall"]),

        "mth_ids_accuracy": float(outputs["stack"]["accuracy"]),
        "mth_ids_precision": float(outputs["stack"]["precision"]),
        "mth_ids_F1": float(outputs["stack"]["f1"]),
        "mth_ids_recall": float(outputs["stack"]["recall"]),

        "mth_ids_hpo_accuracy": float(outputs["stack_hpo"]["accuracy"]),
        "mth_ids_hpo_precision": float(outputs["stack_hpo"]["precision"]),
        "mth_ids_hpo_F1": float(outputs["stack_hpo"]["f1"]),
        "mth_ids_hpo_recall": float(outputs["stack_hpo"]["recall"]),
    }