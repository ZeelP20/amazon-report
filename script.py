# ================= IMPORTS =================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import smtplib
from email.message import EmailMessage
import os

# ================= CONFIG =================
# ⚠️ Set these in GitHub Secrets OR locally as environment variables
EMAIL = os.getenv("zeelpithva2004@gmail.com")
APP_PASSWORD = os.getenv("gqsg dyxe abvp heyh")

# ================= UTIL =================
def safe_text(soup, selector):
    el = soup.select_one(selector)
    return el.get_text(strip=True) if el else None

# ================= SCRAPER =================
def scrape_amazon(asin, driver):
    try:
        url = f"https://www.amazon.in/dp/{asin}"
        driver.get(url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        price = safe_text(soup, "span.a-price span.a-offscreen")
        deal = safe_text(soup, "span.a-badge-text") or "No Deal"
        coupon = safe_text(soup, "span.a-color-success") or "No Coupon"

        return {
            "ASIN": asin,
            "Price": price,
            "Deal": deal,
            "Coupon": coupon
        }

    except Exception as e:
        return {
            "ASIN": asin,
            "Price": None,
            "Deal": "Error",
            "Coupon": None,
            "Error": str(e)
        }

# ================= DRIVER =================
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Prevent bot detection (important for Amazon)
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
)

# IMPORTANT for GitHub Actions
options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(options=options)

# ================= ASINS =================
asins = [
    "B0DNWF3KR9","B0DNWFZHV3","B0DNZ1V3V7","B0DNZ74CPK","B0DP45TT1M",
    "B0DRD8RPKV","B0DRD61X6W","B0DRD7B92M","B0BV9R1L5T","B0FFB8GGG7"
    # 👉 You can paste your full list here (no issue)
]

# ================= RUN =================
results = []

for asin in asins:
    print("Processing:", asin)
    results.append(scrape_amazon(asin, driver))
    time.sleep(2)

driver.quit()

# ================= SAVE FILE =================
df = pd.DataFrame(results)
df.to_excel("output.xlsx", index=False)

print("Excel file created")

# ================= SEND EMAIL =================
# Only send email if credentials exist
if EMAIL and APP_PASSWORD:

    msg = EmailMessage()
    msg['Subject'] = 'Daily Amazon Report'
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg.set_content('Please find attached report.')

    with open("output.xlsx", "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="xlsx",
            filename="output.xlsx"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

    print("Email sent successfully")

else:
    print("Email credentials not found. Skipping email sending.")
