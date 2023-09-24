from selenium import webdriver
import pandas as pd

def collect_data():
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")

    script = """
    var elements = document.querySelectorAll('*');
    var data = [];
    for(var i = 0; i < elements.length; i++) {
        var element = elements[i];
        var attributes = {
            tag: element.tagName.toLowerCase(),
            id: element.id,
            name: element.name,
            class: element.className,
            type: element.type,
            value: element.value
        };
        data.push(attributes);
    }
    return data;
    """

    data = driver.execute_script(script)

    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv('elements.csv', index=False)

# Call the function to collect data
collect_data()
