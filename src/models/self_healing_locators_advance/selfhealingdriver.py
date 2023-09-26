# File: selfhealingdriver.py
from pathlib import Path

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from sklearn.ensemble import RandomForestClassifier
import joblib

class SelfHealingDriver:

    filepath = str(Path(__file__).resolve().parent)

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.model = joblib.load(SelfHealingDriver.filepath + '/model/model.pkl')
        self.le = {column: joblib.load(f'{SelfHealingDriver.filepath}/model/labelencoder_{column}.pkl') for column in ['tag', 'id', 'name', 'class', 'type', 'value']}

    def find_element(self, by, value):
        try:
            if by == 'name':
                return self.driver.find_element(By.NAME, value)
            elif by == 'id':
                return self.driver.find_element(By.ID, value)
            # ... Add other cases as needed
        except:
            return self.handle_no_such_element_exception(by, value)

    def handle_no_such_element_exception(self, by, value):
        elements_data = pd.read_csv(self.filepath + '/elements.csv')
        
        # filter for rows that has value==<value> in <by> column
        is_search = elements_data[by] == value
        prediction_data = elements_data[is_search].copy()
        
        # take one row in case of multiple rows
        prediction_data = prediction_data.iloc[0:1, :]
        
        # Make the value NaN because NaN is a valid input value to model encoder (this is valid for only this training data)
        # TODO: Should be handled in a generic way during training
        prediction_data[by] = np.NaN
        
        # ---- Prep for prediction ------
        # Remove target column
        prediction_data_x = prediction_data.drop(columns=["tag"])
        # encode
        prediction_encoded = prediction_data_x.apply(lambda x: self.le[x.name].transform(x.astype(str)))
        
        # predict
        predictions = self.model.predict(prediction_encoded)
        predictions_decoded = self.le['tag'].inverse_transform(predictions)
        predicted_tag = predictions_decoded[-1]

        return self.driver.find_element(By.TAG_NAME, predicted_tag)

    def quit(self):
        self.driver.quit()
