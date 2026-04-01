# ================= IMPORTS =================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import smtplib
from email.message import EmailMessage

# ================= CONFIG =================
EMAIL = "zeelpithva2004@gmail.com"
APP_PASSWORD = "gqsg dyxe abvp heyh"

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

    except Exception:
        return {
            "ASIN": asin,
            "Price": None,
            "Deal": "Error",
            "Coupon": None
        }

# ================= DRIVER =================
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# IMPORTANT: GitHub path
service = Service("/usr/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)

# ================= ASINS =================
asins = [
    "B0DNWF3KR9",
    "B0DNWFZHV3"
]

# ================= RUN =================
results = []

for asin in asins:
    print("Processing:", asin)
    data = scrape_amazon(asin, driver)
    results.append(data)
    time.sleep(2)

driver.quit()

# ================= SAVE FILE =================
df = pd.DataFrame(results)
df.to_excel("output.xlsx", index=False)

print("Excel file created")

# ================= SEND EMAIL =================
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
