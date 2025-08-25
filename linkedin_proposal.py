# linkedin_proposal.py
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json, os, time, random, sys

# ─── Config ─────────────────────────────────────────────
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)
LI_AT = cfg["li_at"]

# ─── Parse arguments ────────────────────────────────────
if len(sys.argv) < 3:
    print("[ERROR] Usage: python linkedin_proposal.py <thread_url> \"<message to send>\"", flush=True)
    sys.exit(1)

THREAD_URL   = sys.argv[1]
MESSAGE_TEXT = sys.argv[2]

# ─── Helpers ─────────────────────────────────────────────
def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def human_sleep(a=1.0, b=2.5):
    time.sleep(random.uniform(a, b))

def human_type(el, text, a=0.02, b=0.07):
    for c in text:
        el.send_keys(c)
        time.sleep(random.uniform(a, b))


# ─── Launch undetected-chromedriver ─────────────────────
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options, headless=False)
wait = WebDriverWait(driver, 30)

try:
    # ─── 1) Set cookie & login ──────────────────────────
    log("1) Opening LinkedIn to set cookie")
    time.sleep(2)
    driver.get("https://www.linkedin.com/feed/")
    driver.delete_all_cookies()
    driver.add_cookie({
        "name":     "li_at",
        "value":    LI_AT,
        "domain":   ".linkedin.com",
        "path":     "/",
        "secure":   True,
        "httpOnly": True
    })
    log("li_at cookie set")

    log(f"2) Navigating to thread: {THREAD_URL}")
    driver.get(THREAD_URL)
    human_sleep(3, 5)

    if "login" in driver.current_url:
        print("login_failed", flush=True)
        sys.exit(1)
    log("Logged in")

    # ─── 3) Click “Submit proposal” with 10 s timeout ────
    log("3) Locating 'Submit proposal' button (10s timeout)")
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                "//button[.//span[contains(text(),'Submit proposal')]]"
            ))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        human_sleep(0.5, 1.5)
        btn.click()
        human_sleep(2, 3)
        log("Clicked 'Submit proposal'")
    except TimeoutException:
        print("submit_proposal_button_not_found", flush=True)
        sys.exit(1)

    # ─── 4) Type proposal message ────────────────────────
    log("4) Typing proposal message")
    ta = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
        "textarea.fb-multiline-text.artdeco-text-input__textarea"
    )))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ta)
    ta.clear()
    human_type(ta, MESSAGE_TEXT)
    human_sleep(1, 2)

    # ─── 5) Send proposal ────────────────────────────────
    log("5) Clicking 'Send proposal'")
    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH,
        "//button[.//span[contains(text(),'Send proposal')]]"
    )))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", send_btn)
    human_sleep(0.5, 1.5)
    send_btn.click()
    human_sleep(2, 3)

    log("Proposal sent successfully.")
    sys.exit(0)

except Exception as e:
    log(f"[ERROR] {e}")
    sys.exit(1)

finally:
    driver.quit()
