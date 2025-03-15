import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ✅ Setup Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ Start WebDriver (No Local Path Needed)
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

with open('VP_data.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    try:
        driver.get("https://vidyutpravah.in/")

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        data = [
            timestamp,
            driver.find_element(By.XPATH, '//*[@id="spanAllIndiaSurplus"]').text,
            driver.find_element(By.XPATH, '//*[@id="UMCP"]').text,
            driver.find_element(By.XPATH, '//*[@id="CurrentDemandMET"]').text,
            driver.find_element(By.XPATH, '//*[@id="PrevDemandMET"]').text,
            driver.find_element(By.XPATH, '//*[@id="spanPeak"]').text,
            driver.find_element(By.XPATH, '//*[@id="spanEnergy"]').text,
            driver.find_element(By.XPATH, '//*[@id="CongestionToday"]').text
        ]

        writer.writerow(data)
        print(f"✅ Data recorded at {timestamp}")

    except Exception as e:
        print(f"⚠️ Error extracting data: {e}")

    finally:
        driver.quit()
