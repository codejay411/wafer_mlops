from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics  import roc_auc_score,accuracy_score
import os
import json
import yaml
def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

params_path = os.path.join("config", "params.yaml")
config = read_params(params_path)

class Model_Finder:
    """
                This class shall  be used to find the model with best accuracy and AUC score.
                Written By: iNeuron Intelligence
                Version: 1.0
                Revisions: None

                """

    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.clf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')
        self.json_random_forest={}
        self.json_xgboost={}

    def get_best_params_for_random_forest(self,train_x,train_y):
        """
                                Method Name: get_best_params_for_random_forest
                                Description: get the parameters for Random Forest Algorithm which give the best accuracy.
                                             Use Hyper Parameter Tuning.
                                Output: The model with the best parameters
                                On Failure: Raise Exception

                                Written By: iNeuron Intelligence
                                Version: 1.0
                                Revisions: None

                        """
        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_random_forest method of the Model_Finder class')
        n_estimator = config["training"]["random_forest"]["param_grid"]["n_estimators"]
        criterion = config["training"]["random_forest"]["param_grid"]["criterion"]
        max_depth = config["training"]["random_forest"]["param_grid"]["max_depth"]
        max_features = config["training"]["random_forest"]["param_grid"]["max_features"]
        cv = config["training"]["random_forest"]["cv"]
        verbose = config["training"]["random_forest"]["verbose"]

        # print(n_estimator)
        # print(criterion)
        # print(max_depth)
        # print(max_features)


        try:
            # initializing with different combination of parameters

            self.param_grid = {"n_estimators": n_estimator, "criterion": criterion,
            "max_depth": max_depth, "max_features": max_features}

            #Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.clf, param_grid=self.param_grid, cv=cv,  verbose=verbose)
            #finding the best parameters
            self.grid.fit(train_x, train_y)

            #extracting the best parameters
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']

            #creating a new model with the best parameters
            self.clf = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                              max_depth=self.max_depth, max_features=self.max_features)
            # training the mew model
            self.clf.fit(train_x, train_y)

            # predicted = self.clf.predict()
            # ------------------------------------
            # params_file = config["reports"]["params"]
            params = {
                "model": "RandomForest",
                "n_estimators": self.n_estimators,
                "max_features": self.max_features,
                "max_depth": self.max_depth,
                "criterion": self.criterion,
            }
            self.json_random_forest.update(params)
            
            # -------------------------------------

            self.logger_object.log(self.file_object,
                                   'Random Forest best params: '+str(self.grid.best_params_)+'. Exited the get_best_params_for_random_forest method of the Model_Finder class')

            return self.clf
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_params_for_random_forest method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Random Forest Parameter tuning  failed. Exited the get_best_params_for_random_forest method of the Model_Finder class')
            raise Exception()

    def get_best_params_for_xgboost(self,train_x,train_y):

        """
                                        Method Name: get_best_params_for_xgboost
                                        Description: get the parameters for XGBoost Algorithm which give the best accuracy.
                                                     Use Hyper Parameter Tuning.
                                        Output: The model with the best parameters
                                        On Failure: Raise Exception

                                        Written By: iNeuron Intelligence
                                        Version: 1.0
                                        Revisions: None

                                """
        self.logger_object.log(self.file_object,
                               'Entered the get_best_params_for_xgboost method of the Model_Finder class')

        n_estimator = config["training"]["xg_boost"]["param_grid"]["n_estimators"]
        learning_rate = config["training"]["xg_boost"]["param_grid"]["learning_rate"]
        max_depth = config["training"]["xg_boost"]["param_grid"]["max_depth"]
        cv = config["training"]["xg_boost"]["cv"]
        verbose = config["training"]["xg_boost"]["verbose"]
        try:
            # initializing with different combination of parameters
            self.param_grid_xgboost = {

                'learning_rate': learning_rate,
                'max_depth': max_depth,
                'n_estimators': n_estimator

            }
            # Creating an object of the Grid Search class
            # self.grid= GridSearchCV(XGBClassifier(objective='binary:logistic'),self.param_grid_xgboost, verbose=verbose,cv=cv)
            # finding the best parameters
            # self.grid.fit(train_x, train_y)

            # extracting the best parameters
            # self.learning_rate = self.grid.best_params_['learning_rate']
            # self.max_depth = self.grid.best_params_['max_depth']
            # self.n_estimators = self.grid.best_params_['n_estimators']


            self.learning_rate = 0.5
            self.max_depth = 3
            self.n_estimators = 10

            # creating a new model with the best parameters
            self.xgb = XGBClassifier(learning_rate=self.learning_rate, max_depth=self.max_depth, n_estimators=self.n_estimators)
            # training the mew model
            self.xgb.fit(train_x, train_y)
            
            # ------------------------------------
            # params_file = config["reports"]["params"]
            params = {
                "model": "XGBoost",
                "learning_rate": self.learning_rate,
                "max_depth": self.max_depth,
                "n_estimators": self.n_estimators,
            }
            self.json_xgboost.update(params)
            
            # -------------------------------------

            # self.logger_object.log(self.file_object,
            #                        'XGBoost best params: ' + str(
            #                            self.grid.best_params_) + '. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            return self.xgb
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_params_for_xgboost method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'XGBoost Parameter tuning  failed. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            raise Exception()


    def get_best_model(self,train_x,train_y,test_x,test_y):
        """
                                                Method Name: get_best_model
                                                Description: Find out the Model which has the best AUC score.
                                                Output: The best model name and the model object
                                                On Failure: Raise Exception

                                                Written By: iNeuron Intelligence
                                                Version: 1.0
                                                Revisions: None

                                        """
        self.logger_object.log(self.file_object,
                               'Entered the get_best_model method of the Model_Finder class')
        # create best model for XGBoost
        try:
            self.xgboost= self.get_best_params_for_xgboost(train_x,train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x) # Predictions using the XGBoost Model
            self.xgboost_score=0

            if len(test_y.unique()) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)
                self.logger_object.log(self.file_object, 'Accuracy for XGBoost:' + str(self.xgboost_score))  # Log AUC
            else:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost) # AUC for XGBoost
                self.logger_object.log(self.file_object, 'AUC for XGBoost:' + str(self.xgboost_score)) # Log AUC

            # create best model for Random Forest
            self.random_forest=self.get_best_params_for_random_forest(train_x,train_y)
            self.prediction_random_forest=self.random_forest.predict(test_x) # prediction using the Random Forest Algorithm
            self.random_forest_score=0

            if len(test_y.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.random_forest_score = accuracy_score(test_y,self.prediction_random_forest)
                self.logger_object.log(self.file_object, 'Accuracy for RF:' + str(self.random_forest_score))
            else:
                self.random_forest_score = roc_auc_score(test_y, self.prediction_random_forest) # AUC for Random Forest
                self.logger_object.log(self.file_object, 'AUC for RF:' + str(self.random_forest_score))


            #comparing the two models
            if(self.random_forest_score <  self.xgboost_score):
                # ------------------
                scores_file = config["reports"]["scores"]
                params_file = config["reports"]["params"]

                scores = {
                    "model": "XGBoost",
                    "scores": self.xgboost_score
                    }    
                # score = {key,scores}                
                with open(scores_file, "w") as f:
                    json.dump(scores, f)
                 
                # param = {key,self.json_random_forest}
                with open(params_file, "w") as f:
                    json.dump(self.json_random_forest, f)
                # k=k+1/
   
                # -----------------
                return 'XGBoost',self.xgboost
            else:
                # ------------------
                scores_file = config["reports"]["scores"]
                params_file = config["reports"]["params"]
                scores = {
                    "model": "RandomForest",
                    "scores": self.random_forest_score
                    }
                # score = {key,scores}                    
                with open(scores_file, "w") as f:
                    json.dump(scores, f)
                 
                # param = {key,self.json_random_forest}
                with open(params_file, "w") as f:
                    json.dump(self.json_random_forest, f)
                
                # -----------------
                return 'RandomForest',self.random_forest

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()

