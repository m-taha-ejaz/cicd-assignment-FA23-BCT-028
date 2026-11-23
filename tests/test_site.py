import os
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.environ.get(
    "BASE_URL", "http://localhost:8091"
)

@pytest.fixture
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,900")

    browser = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=options
    )

    yield browser
    browser.quit()


def test_page_title(driver):
    driver.get(BASE_URL)

    assert driver.title == (
        "Release Readiness Portal | FA23-BCT-028"
    )


def test_main_heading(driver):
    driver.get(BASE_URL)

    heading = driver.find_element(
        By.ID, "main-heading"
    ).text

    assert heading == (
        "Release Readiness Portal - FA23-BCT-028"
    )

    student = driver.find_element(
        By.ID, "student-info"
    ).text

    assert "Muhammad Taha Ejaz" in student
    assert "FA23-BCT-028" in student


def test_readiness_button(driver):
    driver.get(BASE_URL)

    driver.find_element(
        By.ID, "check-button"
    ).click()

    result = WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element(
            (By.ID, "check-result"),
            "Environment ready"
        )
    )

    assert result is True

    assert driver.find_element(
        By.ID, "check-result"
    ).text == (
        "Environment ready: automated checks enabled."
    )


def test_text_input_submission(driver):
    driver.get(BASE_URL)

    test_message = "CI/CD Automation Verified"

    driver.find_element(
        By.ID, "message-input"
    ).send_keys(test_message)

    driver.find_element(
        By.ID, "submit-button"
    ).click()

    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element(
            (By.ID, "message-result"),
            test_message
        )
    )

    result = driver.find_element(
        By.ID, "message-result"
    ).text

    assert result == "Submitted value: " + test_message

    driver.save_screenshot("screenshot.png")
