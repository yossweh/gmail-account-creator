#!/usr/bin/env python3
"""Gmail Account Creator - Fixed + Working Version"""
import random, string, time, sys, os, subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

PROXY = "http://mnfsfxoq:a4iwyu00aimj@86.38.236.148:6432"

def ensure_xvfb():
    if not os.path.exists('/tmp/.X99-lock'):
        subprocess.Popen(['Xvfb', ':99', '-screen', '0', '1920x1080x24'],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
    os.environ['DISPLAY'] = ':99'

class GmailCreator:
    def __init__(self):
        ensure_xvfb()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        # options.add_argument(f'--proxy-server={PROXY}')  # disabled for Google
        uas = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        options.add_argument(f'--user-agent={random.choice(uas)}')
        import undetected_chromedriver as uc
        self.driver = uc.Chrome(options=options, version_main=149)
        self.wait = WebDriverWait(self.driver, 15)
        self.actions = ActionChains(self.driver)

    def generate_credentials(self):
        first_names = ['alex', 'jordan', 'taylor', 'morgan', 'casey', 'riley', 'sage', 'river', 'skyler', 'dakota']
        last_names = ['smith', 'johnson', 'williams', 'brown', 'jones', 'davis', 'miller', 'wilson', 'moore', 'taylor']
        first = random.choice(first_names)
        last = random.choice(last_names)
        suffix = ''.join(random.choices(string.digits, k=4))
        username = f"{first}.{last}{suffix}"
        password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%', k=16))
        return {
            'first_name': first.capitalize(),
            'last_name': last.capitalize(),
            'username': username,
            'password': password,
            'email': f"{username}@gmail.com"
        }

    def _click_next(self):
        for attempt in range(3):
            try:
                btn = self.driver.find_element(By.XPATH, '//span[text()="Next"]/ancestor::button')
                btn.click()
                return
            except:
                try:
                    btn = self.driver.find_element(By.XPATH, '//span[text()="Next"]')
                    btn.click()
                    return
                except:
                    time.sleep(1)
        print("   Could not find Next button")

    def create_account(self, phone_number=None):
        creds = self.generate_credentials()
        print(f"\n{'='*50}")
        print(f"Creating: {creds['email']}")
        print(f"Password: {creds['password']}")
        print(f"{'='*50}")

        try:
            # Step 1: Go to signup
            print("[1] Opening Google SignUp...")
            self.driver.get('https://accounts.google.com/SignUp')
            time.sleep(random.uniform(3, 5))

            # Step 2: First + Last name
            print("[2] Filling name...")
            time.sleep(random.uniform(1, 2))
            first = self.wait.until(EC.presence_of_element_located((By.NAME, 'firstName')))
            last = self.driver.find_element(By.NAME, 'lastName')
            first.send_keys(creds['first_name'])
            last.send_keys(creds['last_name'])
            self._click_next()
            time.sleep(random.uniform(2, 3))

            # Step 3: Birthday & Gender
            print("[3] Filling birthday/gender...")
            self.driver.find_element(By.ID, 'day').send_keys(str(random.randint(1, 28)))
            self.driver.find_element(By.ID, 'year').send_keys(str(random.randint(1985, 2000)))
            # Month: click combobox, HOME + ENTER
            month_cb = self.driver.find_element(By.XPATH, '//div[@role="combobox"][contains(.,"Month")]')
            month_cb.click()
            time.sleep(0.5)
            self.actions.send_keys(Keys.HOME).send_keys(Keys.ENTER).perform()
            time.sleep(1)
            # Gender: click combobox, 2x ARROW_DOWN + ENTER
            gender_cb = self.driver.find_element(By.XPATH, '//div[@role="combobox"][contains(.,"Gender")]')
            gender_cb.click()
            time.sleep(0.5)
            self.actions.send_keys(Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER).perform()
            time.sleep(1)
            self._click_next()
            time.sleep(random.uniform(2, 3))

            # Step 4: Username
            print(f"[4] Setting username: {creds['username']}...")
            uname_input = self.wait.until(EC.presence_of_element_located((By.NAME, 'Username')))
            uname_input.clear()
            uname_input.send_keys(creds['username'])
            self._click_next()
            time.sleep(random.uniform(2, 3))

            # Check if username taken
            try:
                err = self.driver.find_element(By.XPATH, "//div[contains(@role, 'alert')]")
                if err.is_displayed():
                    print(f"   Username taken!")
                    return None
            except: pass

            # Step 5: Password
            print("[5] Setting password...")
            self.driver.find_element(By.NAME, 'Passwd').send_keys(creds['password'])
            self.driver.find_element(By.NAME, 'PasswdAgain').send_keys(creds['password'])
            self._click_next()
            time.sleep(random.uniform(3, 5))

            # Step 6: Phone verification
            print("[6] Phone verification...")
            if phone_number:
                phone_input = self.driver.find_element(By.NAME, 'phoneNumber')
                phone_input.send_keys(phone_number)
                self._click_next()
            else:
                print("   No phone - screenshot")
                self.driver.save_screenshot('/home/ubuntu/gmail_phone_verify.png')
                print("   Screenshot: /home/ubuntu/gmail_phone_verify.png")
                input("Press Enter after manual verification...")
                self._click_next()
            time.sleep(random.uniform(3, 5))

            # Step 7: Recovery email (optional)
            print("[7] Recovery email...")
            try:
                rec_field = self.driver.find_element(By.NAME, 'recoveryEmail')
                rec_field.send_keys("")
                self._click_next()
            except: pass
            time.sleep(random.uniform(2, 3))

            # Step 8: Terms
            print("[8] Terms...")
            try: self.driver.find_element(By.XPATH, "//span[text()='I agree']").click()
            except: pass
            try: self.driver.find_element(By.XPATH, "//span[text()='Accept']").click()
            except: pass

            time.sleep(random.uniform(3, 5))
            current_url = self.driver.current_url

            if 'mail.google.com' in current_url or 'myaccount.google.com' in current_url:
                print(f"\nSUCCESS!")
                print(f"Email: {creds['email']}")
                print(f"Pass:  {creds['password']}")
                with open('/home/ubuntu/gmail_accounts.txt', 'a') as f:
                    f.write(f"\n{'='*50}\n")
                    f.write(f"Email: {creds['email']}\n")
                    f.write(f"Password: {creds['password']}\n")
                    f.write(f"Created: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                return creds
            else:
                print(f"\nURL: {current_url}")
                self.driver.save_screenshot('/home/ubuntu/gmail_result.png')
                return None

        except Exception as e:
            print(f"Error: {e}")
            self.driver.save_screenshot('/home/ubuntu/gmail_error.png')
            return None

    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    PHONE = sys.argv[1] if len(sys.argv) > 1 else ""
    creator = GmailCreator()
    if not PHONE:
        print("No phone provided - will stop at verification screen")
        account = creator.create_account(phone_number=None)
    else:
        account = creator.create_account(phone_number=PHONE)
    if account:
        print(f"\nEmail: {account['email']}")
        print(f"Password: {account['password']}")
    creator.close()
