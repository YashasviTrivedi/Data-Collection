import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ✅ Setup Chrome options for GitHub Actions
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ Start WebDriver (Use system-installed ChromeDriver)
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Website to scrape
web = "https://vidyutpravah.in/"
driver.get(web)
print("✅ Opened website:", web)

# ✅ Define CSV file path
csv_file = "States_data.csv"

# ✅ Extract state links
try:
    state_elements = driver.find_elements(By.CSS_SELECTOR, "a.state-names_en")
    state_links = {element.text.strip(): element.get_attribute("href") for element in state_elements if element.text and element.get_attribute("href")}
    print(f"✅ Found {len(state_links)} states with data.")

    if not state_links:
        print("❌ No state links found! Website structure may have changed.")
        driver.quit()
        exit(1)

except Exception as e:
    print(f"❌ Failed to extract state links: {e}")
    driver.quit()
    exit(1)

# ✅ Write headers to CSV
header = ["Timestamp", "State", "Current Exchange Price (₹/Unit)", "Yesterday Exchange Price (₹/Unit)", "Current Demand Met (MW)", "Yesterday Demand Met (MW)", "Current Power Purchased (MW)", "Energy Shortage Yesterday (MU)", "Peak Energy Shortage Yesterday (MU)"]

with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"✅ Data recorded at {timestamp}")

    for state, url in state_links.items():
        driver.get(url)  # Open state page
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
