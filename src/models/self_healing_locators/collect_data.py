from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def collect_data():
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")

    elements = [
        driver.find_element(By.NAME, "q"),
        driver.find_element(By.NAME, "btnK")
    ]

    data = []

    for element in elements:
        attributes = {
            'tag': element.tag_name,
            'id': element.get_attribute('id'),
            'name': element.get_attribute('name'),
            'class': element.get_attribute('class'),
            'type': element.get_attribute('type'),
            'value': element.get_attribute('value')
        }
        data.append(attributes)

    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv('elements.csv', index=False)

# Call the function to collect data
collect_data()
