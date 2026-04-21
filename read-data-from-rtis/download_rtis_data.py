from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import os
import glob
import shutil   # <-- IMPORTANT


# ==============================
# SETTINGS
# ==============================

DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_opts
)


# ==============================
# LOGIN (MANUAL)
# ==============================

driver.get("https://rtis.indianrail.gov.in/RTISDashboardUI/login")

print("Please login manually (Username + Password + CAPTCHA + OTP)")
print("Do NOT close the browser window...")

TARGET_URL = "https://rtis.indianrail.gov.in/RTISDashboardUI/shed/shedHome"

WebDriverWait(driver, 300).until(
    EC.url_to_be(TARGET_URL)
)

print("\nLogin detected — Dashboard loaded\n")
time.sleep(2)


# ==============================
# NAVIGATE TO SPEED PROFILE
# ==============================

speed_menu = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        By.XPATH,
        '//span[@class="title" and contains(normalize-space(.),"Speed Profile Chart")]'
    ))
)
speed_menu.click()

loco_menu = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "locoSpeedProfileId_beta"))
)
loco_menu.click()

print("Enter From Date, To Date & Loco Number manually, then click SUBMIT\n")


# ==============================
# WAIT FOR TABLE RESULTS
# ==============================

WebDriverWait(driver, 600).until(
    EC.presence_of_element_located((
        By.XPATH,
        "//table[.//th[contains(.,'LOCO_NUMBER')]]//tbody//tr"
    ))
)

print("Data detected — exporting CSV…")


# ==============================
# CLICK CSV BUTTON
# ==============================

csv_btn = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.dt-button.buttons-csv"))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", csv_btn)
time.sleep(1)

try:
    csv_btn.click()
except:
    driver.execute_script("arguments[0].click();", csv_btn)

print("CSV export triggered…")


# ==============================
# WAIT FOR DOWNLOAD TO COMPLETE
# ==============================

def wait_for_download():
    while any(f.endswith(".crdownload") for f in os.listdir(DOWNLOAD_DIR)):
        time.sleep(1)

wait_for_download()
time.sleep(2)


# ==============================
# READ FIELD VALUES
# ==============================

from_input = driver.find_element(By.CSS_SELECTOR, "#fDateDiv input")
to_input   = driver.find_element(By.CSS_SELECTOR, "#tDateDiv input")
loco_input = driver.find_element(By.CSS_SELECTOR, "#tDeviceDiv input")

from_str = from_input.get_attribute("value").strip()
to_str   = to_input.get_attribute("value").strip()
loco     = loco_input.get_attribute("value").strip()

print("\nFROM =", from_str)
print("TO   =", to_str)
print("LOCO =", loco)


# ==============================
# BUILD FILENAME
# ==============================

def build_filename(loco, from_str, to_str):

    f = datetime.strptime(from_str, "%Y-%m-%d %H:%M")
    t = datetime.strptime(to_str, "%Y-%m-%d %H:%M")

    if f.date() == t.date():
        return f"{loco}_{f.date()}_{f.strftime('%H%M')}-{t.strftime('%H%M')}.csv"
    else:
        return f"{loco}_{f.strftime('%Y-%m-%d_%H%M')}_to_{t.strftime('%Y-%m-%d_%H%M')}.csv"


output_name = build_filename(loco, from_str, to_str)


# ==============================
# FIND DOWNLOADED FILE
# ==============================

csv_files = glob.glob(os.path.join(DOWNLOAD_DIR, "*.csv"))
latest_file = max(csv_files, key=os.path.getctime)

dest = os.path.join(os.getcwd(), output_name)

print("\nLatest downloaded file:", latest_file)
print("Renaming to           :", dest)


# ==============================
# MOVE ACROSS DRIVES SAFELY
# ==============================

if os.path.exists(dest):
    os.remove(dest)

shutil.move(latest_file, dest)

print(f"\nCSV successfully saved as:\n{dest}\n")

input("Press ENTER to close browser...")

driver.quit()