import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ✅ Setup Chrome options for headless mode (for GitHub Actions)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without UI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ Start WebDriver (No Local Path Needed)
service = Service("/usr/local/bin/chromedriver")  # Use system-installed ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

web = "https://vidyutpravah.in/"
driver.get(web)

# Locate state links
state_elements = driver.find_elements(By.CSS_SELECTOR, "a.state-names_en")

state_links = {element.text.strip(): element.get_attribute("href") for element in state_elements if element.text and element.get_attribute("href")}

csv_file = "States_data.csv"
header = ["Timestamp", "State", "Current Exchange Price (₹/Unit)", "Yesterday Exchange Price (₹/Unit)", "Current Demand Met (MW)", "Yesterday Demand Met (MW)", "Current Power Purchased (MW)", "Energy Shortage Yesterday (MU)", "Peak Energy Shortage Yesterday (MU)"]

with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    print("Data recorded at", timestamp)

    for state, url in state_links.items():
        driver.get(url)  # Open the state page

        try:
            state_div_id = ''.join([word.capitalize() for word in state.split()]) + "_map"
            if state == 'ODISHA': state_div_id = 'Orissa_map'
            elif state == 'PUDUCHERRY': state_div_id = 'Pondicherry_map'
            elif state == 'MAHARASHTRA': state_div_id = 'Maharastra_map'
            elif state == 'ANDHRA PRADESH': state_div_id = 'AndraPradesh_map'
            elif state == 'JAMMU & KASHMIR': state_div_id = 'JammuKashmir_map'

            data = [
                timestamp, state,
                driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_ExchangePrice_en')]").text.strip(),
                driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PrevExchangePrice_en')]").text.strip(),
                driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_DemandMET_en')]").text.strip(),
                driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PrevDemandMET_en')]").text.strip(),
                driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PowerPurchase_en')]").text.strip(),
                driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_TotalEnergy_en')]").text.strip(),
                driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PeakDemand_en')]").text.strip()
            ]

            writer.writerow(data)
            print(f"✅ Data recorded for {state} at {timestamp}")

        except Exception as e:
            print(f"⚠️ Error extracting data for {state}: {e}")

driver.quit()
