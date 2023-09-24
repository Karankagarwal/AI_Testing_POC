# File: selfhealingdriver.py
from pathlib import Path

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
        # Create a new row for prediction with the same columns as the training data
        prediction_data = pd.DataFrame(columns=elements_data.columns)

        # Populate the relevant column with the value and leave the others as NaN
        prediction_data.loc[0, by] = value

        # Encode the data using the same LabelEncoder objects
        prediction_encoded = prediction_data.apply(lambda x: self.le[x.name].transform(x.astype(str)))

        # Predict the tag
        predicted_tag = self.model.predict(prediction_encoded)[0]
        predicted_tag = self.le['tag'].inverse_transform([predicted_tag])[0]

        return self.driver.find_element(By.TAG_NAME, predicted_tag)

    def quit(self):
        self.driver.quit()
