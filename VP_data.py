import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Set up WebDriver
driver_path = "D:/New folder (2)/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # Replace with the correct path
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Open CSV file to store the data
with open('VP_data.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    try:
        # Open the Vidyut Pravah website
        driver.get("https://vidyutpravah.in/")

        # Extract the data
        surplus_power = driver.find_element(By.XPATH, '//*[@id="spanAllIndiaSurplus"]').text
        avg_mcp = driver.find_element(By.XPATH, '//*[@id="UMCP"]').text
        demand_met_current = driver.find_element(By.XPATH, '//*[@id="CurrentDemandMET"]').text
        demand_met_yesterday = driver.find_element(By.XPATH, '//*[@id="PrevDemandMET"]').text
        peak_shortage = driver.find_element(By.XPATH, '//*[@id="spanPeak"]').text
        energy = driver.find_element(By.XPATH, '//*[@id="spanEnergy"]').text
        unconstrained_price = driver.find_element(By.XPATH, '//*[@id="CongestionToday"]').text

        # Get the current timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        # Write the data to CSV
        writer.writerow([timestamp, surplus_power, avg_mcp, demand_met_current, demand_met_yesterday,
                             peak_shortage, energy, unconstrained_price])

        print("Data recorded at", timestamp)

    finally:
        # Close the WebDriver
        driver.quit()


