import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ✅ Setup Chrome options for GitHub Actions
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without UI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ Add User-Agent to Mimic a Real Browser
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36")

# ✅ Start WebDriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Try opening the website
web = "https://vidyutpravah.in/"
try:
    driver.get(web)
    print("✅ Successfully opened website:", web)
except Exception as e:
    print(f"❌ ERROR: Failed to open website: {e}")
    driver.quit()
    exit(1)

# ✅ Extract page title (to confirm the website loaded)
page_title = driver.title
print(f"🔍 Page title: {page_title}")

# ✅ Check if website loaded properly
if "403" in page_title or "Access Denied" in page_title or page_title.strip() == "":
    print("❌ ERROR: Website is blocking GitHub Actions. Exiting.")
    driver.quit()
    exit(1)

# ✅ Continue scraping...
driver.quit()
