import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Set up WebDriver
driver_path = "D:/New folder (2)/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

web = "https://vidyutpravah.in/"

# Open the page
driver.get(web)

# Locate all state links using the class name
state_elements = driver.find_elements(By.CSS_SELECTOR, "a.state-names_en")

# Extract state names and their URLs
state_links = {}
for element in state_elements:
    state_name = element.text.strip()  # Get the text inside the <a> tag
    state_url = element.get_attribute("href")  # Get the full URL
    if state_name and state_url:
        state_links[state_name] = state_url

# Prepare the CSV file with headers
csv_file = "States_data.csv"
header = ["Timestamp",
          "State",
          "Current Exchange Price (₹/Unit)",
          "Yesterday Exchange Price (₹/Unit)",
          "Current Demand Met (MW)",
          "Yesterday Demand Met (MW)",
          "Current Power Purchased (MW)",
          "Energy Shortage Yesterday (MU)",
          "Peak Energy Shortage Yesterday (MU)"
          ]

# Open the CSV file for writing
with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    print("Data recorded at", timestamp)

    # Loop through each state link to extract data
    for state, url in state_links.items():
        driver.get(url)  # Open the state page

        try:
            # Format the state name to match the expected div ID format
            if state == 'ODISHA':
                state_div_id = 'Orissa_map'
            elif state == 'PUDUCHERRY':
                state_div_id = 'Pondicherry_map'
            elif state == 'MAHARASHTRA':
                state_div_id = 'Maharastra_map'
            elif state == 'ANDHRA PRADESH':
                state_div_id = 'AndraPradesh_map'
            elif state == 'JAMMU & KASHMIR':
                state_div_id = 'JammuKashmir_map'
            else:
                state_div_id = ''.join(
                        [word.capitalize() for word in state.split()]) + "_map"  # Capitalize each word and add '_map'

            current_exchange_price = driver.find_element(By.XPATH,
                                                             f"//div[@id='{state_div_id}']//span[contains(@class, 'value_ExchangePrice_en') and contains(@class, 'value_StateDetails_en')]").text.strip()
            yesterday_exchange_price = driver.find_element(By.XPATH,
                                                               f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PrevExchangePrice_en') and contains(@class, 'value_StateDetails_en')]").text.strip()
            current_demand_met = driver.find_element(By.XPATH,
                                                         f"//div[@id='{state_div_id}']//span[contains(@class, 'value_DemandMET_en') and contains(@class, 'value_StateDetails_en')]").text.strip()
            yesterday_demand_met = driver.find_element(By.XPATH,
                                                           f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PrevDemandMET_en') and contains(@class, 'value_StateDetails_en')]").text.strip()
            current_power_purchased = driver.find_element(By.XPATH,
                                                              f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PowerPurchase_en') and contains(@class, 'value_StateDetails_en')]").text.strip()
            shortage_yesterday = driver.find_element(By.XPATH,
                                                         f"//div[@id='{state_div_id}']//span[contains(@class, 'value_TotalEnergy_en') and contains(@class, 'value_StateDetails_en')]").text.strip()
            peak_shortage_yesterday = driver.find_element(By.XPATH,
                                                              f"//div[@id='{state_div_id}']//span[contains(@class, 'value_PeakDemand_en') and contains(@class, 'value_StateDetails_en')]").text.strip()

            # Write data for this state to the CSV file
            writer.writerow([timestamp,
                                 state,
                                 current_exchange_price,
                                 yesterday_exchange_price,
                                 current_demand_met,
                                 yesterday_demand_met,
                                 current_power_purchased,
                                 shortage_yesterday,
                                 peak_shortage_yesterday
                                 ])

            print(f"Data recorded for {state} at {timestamp}")

        except Exception as e:
                print(f"Error extracting data for {state}: {e}")

driver.quit()
