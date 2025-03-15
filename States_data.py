import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36")

# ✅ Start WebDriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Open the website
web = "https://vidyutpravah.in/"
try:
    driver.get(web)
    print("✅ Successfully opened website:", web)
except Exception as e:
    print(f"❌ ERROR: Failed to open website: {e}")
    driver.quit()
    exit(1)

# ✅ Wait for state elements to load (Max 15 seconds)
try:
    wait = WebDriverWait(driver, 15)
    state_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.state-names_en")))
    state_links = {element.text.strip(): element.get_attribute("href") for element in state_elements if element.text and element.get_attribute("href")}
    print(f"✅ Found {len(state_links)} states with data.")
except Exception as e:
    print(f"❌ ERROR: State elements did not load in time: {e}")
    driver.quit()
    exit(1)

# ✅ If no states are found, retry after a delay
if not state_links:
    print("⚠️ No state links found, retrying in 5 seconds...")
    time.sleep(5)
    try:
        state_elements = driver.find_elements(By.CSS_SELECTOR, "a.state-names_en")
        state_links = {element.text.strip(): element.get_attribute("href") for element in state_elements if element.text and element.get_attribute("href")}
    except Exception as e:
        print(f"❌ ERROR: Could not retrieve state links after retry: {e}")
        driver.quit()
        exit(1)

# ✅ If still no states, exit
if not state_links:
    print("❌ ERROR: No state links found! Website structure may have changed.")
    driver.quit()
    exit(1)

# ✅ Define CSV file path
csv_file = "States_data.csv"

# ✅ Write headers to CSV
header = ["Timestamp", "State", "Current Exchange Price (₹/Unit)", "Yesterday Exchange Price (₹/Unit)",
          "Current Demand Met (MW)", "Yesterday Demand Met (MW)", "Current Power Purchased (MW)",
          "Energy Shortage Yesterday (MU)", "Peak Energy Shortage Yesterday (MU)"]

with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"✅ Data recorded at {timestamp}")

    for state, url in state_links.items():
        driver.get(url)
        print(f"🔍 Extracting data for {state}...")

        try:
            state_div_id = ''.join([word.capitalize() for word in state.split()]) + "_map"
            if state == 'ODISHA': state_div_id = 'Orissa_map'
            elif state == 'PUDUCHERRY': state_div_id = 'Pondicherry_map'
            elif state == 'MAHARASHTRA': state_div_id = 'Maharastra_map'
            elif state == 'ANDHRA PRADESH': state_div_id = 'AndraPradesh_map'
            elif state == 'JAMMU & KASHMIR': state_div_id = 'JammuKashmir_map'

            # ✅ Extracting values
            current_price = driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_ExchangePrice_en')]").text.strip()
            prev_price = driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PrevExchangePrice_en')]").text.strip()
            demand_met = driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_DemandMET_en')]").text.strip()
            prev_demand_met = driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PrevDemandMET_en')]").text.strip()
            power_purchased = driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PowerPurchase_en')]").text.strip()
            total_energy = driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_TotalEnergy_en')]").text.strip()
            peak_demand = driver.find_element(By.XPATH, f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PeakDemand_en')]").text.strip()

            # ✅ Print extracted data
            print(f"✅ Data for {state}: {current_price}, {prev_price}, {demand_met}, {prev_demand_met}, {power_purchased}, {total_energy}, {peak_demand}")

            # ✅ Write to CSV
            writer.writerow([timestamp, state, current_price, prev_price, demand_met, prev_demand_met, power_purchased, total_energy, peak_demand])

        except Exception as e:
            print(f"⚠️ Error extracting data for {state}: {e}")

# ✅ Close WebDriver
driver.quit()
print("✅ Web scraping completed!")
