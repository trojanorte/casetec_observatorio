import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

"""
Script to download ANTAQ data files using Selenium and Requests.

This script:
1. Configures the Chrome WebDriver in headless mode.
2. Navigates to ANTAQ's download page.
3. Removes old files from the download directory.
4. Iterates through the selected years (2021-2023) and downloads the Atracação and Carga files.
5. Saves the files in the appropriate project directory.
"""

# Configure Chrome WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without GUI
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--window-size=1920x1080")  # Simulate full-screen resolution
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath("downloads"),  # Default download directory
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
})

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to ANTAQ download page
url = "https://web3.antaq.gov.br/ea/sense/download.html#pt"
driver.get(url)

# Wait for the page to load completely
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_element_located((By.ID, "anotxt")))

# Set correct directory path within the project
download_path = os.path.join(os.path.dirname(__file__), "../data/downloads")

# Create download folder if it doesn't exist
if not os.path.exists(download_path):
    os.makedirs(download_path)

def clear_old_files():
    """
    Removes all existing files in the download directory before downloading new files.
    """
    for file in os.listdir(download_path):
        file_path = os.path.join(download_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"🗑 File removed: {file}")

def download_files():
    """
    Iterates through the selected years and downloads Atracação and Carga files.
    """
    selected_years = ["2023", "2022", "2021"]
    file_types = {
        "Atracação": "Atracacao.zip",
        "Carga": "Carga.zip"
    }

    for year in selected_years:
        print(f"📆 Processing year: {year}")
        select_year = driver.find_element(By.ID, "anotxt")
        select_year.send_keys(year)
        time.sleep(5)  # Wait for the page to update

        for name, filename in file_types.items():
            download_link = f"https://web3.antaq.gov.br/ea/txt/{year}{filename}"
            destination = os.path.join(download_path, f"{year}_{filename}")

            print(f"📥 Downloading: {name} ({year}) - {download_link}")

            try:
                response = requests.get(download_link, stream=True)
                if response.status_code == 200:
                    with open(destination, "wb") as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            file.write(chunk)
                    print(f"✅ Download completed: {name} ({year})")
                else:
                    print(f"❌ Error downloading {name} ({year}): HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Download failure for {name} ({year}): {e}")

# Execute functions
clear_old_files()
download_files()

# Close browser after downloads
driver.quit()

print(f"🎯 All relevant files have been saved in: {download_path}")
