# ================= IMPORTS =================
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import smtplib
from email.message import EmailMessage
import os

# ================= CONFIG =================
EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# ================= UTIL =================
def safe_text(soup, selector):
    el = soup.select_one(selector)
    return el.get_text(strip=True) if el else None

# ================= SCRAPER =================
def scrape_amazon(asin, driver):
    try:
        url = f"https://www.amazon.in/dp/{asin}"
        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        price = (
    safe_text(soup, "span.a-price span.a-offscreen") or
    safe_text(soup, "#priceblock_ourprice") or
    safe_text(soup, "#priceblock_dealprice") or
    safe_text(soup, "#priceblock_saleprice")
)
        deal = safe_text(soup, "span.a-badge-text") \
    or safe_text(soup, "#dealBadgeSupportingText") \
    or safe_text(soup, ".dealBadgeText") \
    or "No Deal"
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

# ✅ ADD THESE 2 LINES HERE
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/53736"
)

options.binary_location = "/usr/bin/chromium-browser"
service = Service("/usr/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)

# ================= FULL ASINS =================
asins = [
"B0DNWF3KR9",
"B0DNWFZHV3",
"B0DNZ1V3V7",
"B0DNZ74CPK",
"B0DP45TT1M",
"B0DRD8RPKV",
"B0DRD61X6W",
"B0DRD7B92M",
"B0BV9R1L5T",
"B0FFB8GGG7",
"B0FPF6SZXL",
"B0FPF6PWD8",
"B0FPD4VHV3",
"B0FPD8NZWM",
"B0FJ8MVW2V",
"B0FJ8L53ND",
"B0FPD8FN9K",
"B0D7Q6T4JK",
"B0F2FJNFRM",
"B0F2FKCWCJ",
"B0F2FJ8JWL",
"B0F1TWKRF6",
"B0FGCVXHSM",
"B0FGJ4LHQJ",
"B0FF3Z44X2",
"B0FF44242V",
"B0FF44YFL1",
"B0FF3W1HTN",
"B0FF44WJG2",
"B0FF44YQQ9",
"B0FF43B5CW",
"B0F2FJDW8D",
"B00JII8IQS",
"B0BWNNDTN2",
"B07999DC2C",
"B0799BGYJD",
"B0799567BS",
"B01HID4YYY",
"B0D713H1J3",
"B01JYUU2ZY",
"B07C7GD8WT",
"B0B9CCK9R1",
"B08CSFT62R",
"B09Q8BT91B",
"B0D6GM2FMN",
"B08CBKQ7BT",
"B0828Q57GP",
"B0FMFLB9NW",
"B0FMFL2SWY",
"B0FMFMN6R2",
"B0FMFK868D",
"B0C81N14SN",
"B0C81K4KCF",
"B0C81HD252",
"B08N25NCR4",
"B07CH5QRL5",
"B07CH55JJN",
"B08YRR3LH9",
"B08YRRD6TX",
"B08YRP2WB3",
"B089QS4QGM",
"B08LNZ7176",
"B089QSJ4L7",
"B0CW61QDNQ",
"B0CG972765",
"B08YDZPVQ8",
"B08YDXK93V",
"B08YDRGCKQ",
"B0D6GPBZZ6",
"B0D6GNGRC9",
"B0BPTD79TD",
"B00E1EK8UI",
"B0D6GPFFFX",
"B089N4L1KR",
"B07CKZS244",
"B089NK2W8N",
"B089MJPTFC",
"B089N79HHH",
"B07V7TRZMQ",
"B0822WHNHH",
"B089RC4LYH",
"B08962DGC1",
"B08LPC47M7",
"B08CBJ36WV",
"B08CBGBS5Y",
"B0D22ZRSG5",
"B0D22XRVP9",
"B0D23131KQ",
"B0D22ZG9P9",
"B0D4R37HDR",
"B0D4R5L1XP",
"B0D6ZCLC3T",
"B0D4R4VPJ5",
"B0D6ZFGJQ5",
"B0D6ZCRP3W",
"B0D6ZW44WT",
"B0D6ZR22BB",
"B0D4R62J4J",
"B0D5M2L993",
"B0CRHSKPV5",
"B09DSGQTYY",
"B0DGV31D6W",
"B0D5M3138Q",
"B0D5M37GD7",
"B0DJW2DDKJ",
"B09DSPL1C4",
"B0F446XF78",
"B0F48RNBM4",
"B0F441QYHJ",
"B0F4445DNX",
"B0F441H19G",
"B0F441PSHR",
"B0FMFK8F4Z",
"B0FMFM15M2",
"B0FMFH9C4B",
"B0FMFJVHNB",
"B0FMFGQ3ZM",
"B0FMFJBC2Z",
"B0FMFJ11PJ",
"B0FMFMDHF3",
"B0FMFL5J5N",
"B0FMRS5LTP",
"B0FMXXXYY6",
"B0FMXWWHDK",
"B0FMXVDR7F",
"B0FMXSFBYG",
"B0FW4YL7KH",
"B0FW4ZM9CP",
"B0FMFJSYRV",
"B097JH239S",
"B0FXX322SJ",
"B0FXX5679X",
"B0FYGNDLTZ",
"B0FYGLZ4Z7",
"B0FYGJ79JF",
"B0FYGLS3RF",
"B0D9HPHZQQ",
"B0D9HP9MB4",
"B0D9HM5FXJ",
"B0D9HN7ZD7",
"B0D3V5QN4P",
"B0D3V57Y22",
"B0C6QHH5JV",
"B0C6QDVZCL",
"B0D3V6H12V",
"B0D4DFQTMJ",
"B0DHCYR5K9",
"B0D4DZDHZ1",
"B0DHCX5SJW",
"B0DHCXBPXK",
"B0D4DDSKBK",
"B0D4DM19KF",
"B0D4DS4FC8",
"B0D4D8MY67",
"B0D4DPBKGL",
"B0D4DY9GWG",
"B0D3V61JC8",
"B0DHCVPTNZ",
"B0DHCVV82R",
"B0D3V6TR98",
"B0DHCXM954",
"B0D3V6Y38G",
"B0D3V4V1KD",
"B0D3V4LR5L",
"B0D3V55RC5",
"B0D3V5W3H9",
"B0D3V91CNY",
"B0D3V4RJKG",
"B0DHCXPGK9",
"B0DHCWWCDJ",
"B0DHCXD5Z1",
"B0DHCYFG1F",
"B0DJR3GFCP",
"B0DJR39GQL",
"B0DJR3YDNF",
"B0DJR3MFVW",
"B0F1FWLCMF",
"B0DBLYRDM6",
"B0DBLW6JD4",
"B0DBLZ75J7",
"B0DYVQHLFR",
"B0FBMLPWSV",
"B0FBML7BFQ",
"B0FBMLG39S",
"B0F6YQ7WGL",
"B0F6YNWR7V",
"B0CLGQVFGS",
"B0BFRLN33R",
"B0CQP3HF8Q",
"B0BFRM35PM",
"B0CQP4Q62J",
"B0D5BK6Y38",
"B0D73LWVF9",
"B0FFSX167Y",
"B0DMWWGVL9",
"B0F79S3788",
"B0FPQKL23Z",
"B0DNWC3QTY",
"B0DNWGBCHP",
"B0DNWDC5C2",
"B0DRD84GYR",
"B0FPF9JNH4",
"B0DNZCFSF5",
"B0FPF8YYG1",
"B0DNWGJJZ9",
"B0DNWDR7JV",
"B0DNWGQJJV",
"B0FPF6X319",
"B0DRD6SJDQ",
"B0F1YW9T8N",
"B0DHS41MPF",
"B0DW8Y8191",
"B0F1Z1NSTC",
"B0DHRYQJ91",
"B0DHS54YP7",
"B0DHS3FM9F",
"B0DW8KFSLH",
"B0DW8DGSFT",
"B07DKGCYB9",
"B079967QGC",
"B0FWY6L1P5",
"B0FWY8R9W8",
"B0FWY6J361",
"B0FWY929XM",
"B0FWY6LS2W",
"B0FWY658SY",
"B0FWY5Y7VF",
"B0FWY6WH7Z",
"B0FWY8TT1X",
"B0FWQT87JQ",
"B0GKNN32L5",
"B0GKNCCMHZ",
"B0FWY81CXR",
"B0FYNH6PBR",
"B0FWR2L94K",
"B0FWQRYTMN",
"B0FWQPB8BX",
"B0FWQPMDCY",
"B0FWRTBVBN"
]

# ================= RUN =================
results = []

for asin in asins:
    print("Processing:", asin)
    results.append(scrape_amazon(asin, driver))
    time.sleep(2)

driver.quit()

# ================= SAVE =================
df = pd.DataFrame(results)
df.to_excel("output.xlsx", index=False)

print("Excel file created")

# ================= EMAIL =================
if EMAIL and APP_PASSWORD:
    msg = EmailMessage()
    msg['Subject'] = 'Daily Amazon Report'
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg.set_content('Please find attached report.')

    with open("output.xlsx", "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="xlsx", filename="output.xlsx")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

    print("Email sent successfully")
else:
    print("Email skipped (no credentials)")
