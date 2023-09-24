# File: example_usage.py
import pytest

from src.models.self_healing_locators_advance.selfhealingdriver import SelfHealingDriver


def test_self_healing_driver():
    sh_driver = SelfHealingDriver()
    sh_driver.driver.get("https://www.google.com")

    search_box = sh_driver.find_element('name', 'q')  # This should succeed
    search_box.send_keys("self-healing locators")

    sh_driver.quit()

# Call the function to test SelfHealingDriver
# test_self_healing_driver()
