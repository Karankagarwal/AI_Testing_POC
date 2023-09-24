from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder


class SelfHealingDriver:
    def __init__(self, driver):
        self.driver = driver
        self.model = joblib.load('/Users/karanaggarwal/PycharmProjects/POC/AI_Demo/src/models/self_healing_locators/model/model.pkl')  # Load the trained model
        self.le = LabelEncoder()  # For encoding attributes
        self.columns = '/Users/karanaggarwal/PycharmProjects/POC/AI_Demo/src/models/self_healing_locators/model/columns.pkl'


    def find_element(self, by, value):
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            return self.handle_no_such_element_exception(by, value)

    def handle_no_such_element_exception(self, by, value):
        # Create a dataframe from the attribute
        test_df = pd.DataFrame([{by: value}])

        # Ensure the test_df has the same columns as the training data, filling missing columns with NaN
        training_columns = joblib.load(self.columns)  # Assuming you saved the column names during training
        for column in training_columns:
            if column not in test_df.columns:
                test_df[column] = None

        # Reorder the columns of test_df to match the order of the columns in the training data
        test_df = test_df[training_columns]

        test_encoded = test_df.apply(self.le.fit_transform)  # Encode attributes

        # Predict the tag of the element
        predicted_tag = self.model.predict(test_encoded)[0]
        predicted_tag = self.le.inverse_transform([predicted_tag])[0]  # Decode back to string

        # Now retry finding the element by tag (this is simplified and may not work in all scenarios)
        return self.driver.find_element_by_tag_name(predicted_tag)


# Usage:
driver = webdriver.Chrome()
sh_driver = SelfHealingDriver(driver)
driver.get("https://www.google.com")

try:
    search_box = sh_driver.find_element('name', 'q')  # This should succeed
    search_box.send_keys("Self healing locators in Selenium")
    search_box.submit()
except NoSuchElementException as e:
    print(f"Element not found: {e}")

driver.quit()
