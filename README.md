# Gmail Account Creator

Automated Gmail account creation tool using Selenium + undetected-chromedriver with anti-bot bypass. Supports custom dropdown handling, keyboard navigation, and manual QR verification.

## What is this tool?

This is a **semi-automated Gmail account creation** tool. It automates 5 out of 8 Google signup steps:

1. ✅ Navigate to signup page
2. ✅ Fill first & last name
3. ✅ Fill birthday & gender (via keyboard navigation for custom dropdowns)
4. ✅ Select username (auto-retry if taken)
5. ✅ Fill password & confirm password
6. ⚠️ Phone verification (stops at QR code)
7. ⏭️ Recovery email (skip)
8. ⏭️ Terms & conditions (auto-accept)

## Why semi-automated?

Google uses a verification system that **cannot be fully bypassed via automation**:

- **QR Code Verification**: Google displays a QR code that must be scanned with a physical phone. This is a security mechanism to verify the user is human, not a bot.
- **Device Fingerprinting**: Google analyzes browser fingerprint, IP address, and behavior patterns to detect automation.
- **No Skip Option**: There is no "skip" or "try another way" button on the verification page.

**Conclusion**: The tool automates as much as possible, but **phone verification must be done manually** by scanning the QR code with your own phone.

## Features

- **Undetected ChromeDriver** — bypass bot detection with `undetected-chromedriver`
- **Custom Combobox Navigation** — Google's new UI uses custom React dropdowns instead of standard `<select>`. This tool uses keyboard navigation (ArrowDown + Enter) to select options
- **Manual QR Verification** — stops at QR code, requires phone scan to continue
- **Random Credential Generation** — names, usernames, and passwords generated randomly
- **Screenshot Capture** — screenshots at each step for debugging
- **Auto-retry** — username auto-regenerates if already taken (max 5 attempts)
- **Xvfb Headless** — runs on VPS/headless environments

## Requirements

```bash
# Python 3.11+
pip install selenium undetected-chromedriver

# Xvfb for headless display (if running on VPS)
sudo apt install xvfb
```

## Installation

```bash
git clone https://github.com/yossweh/gmail-account-creator.git
cd gmail-account-creator
pip install -r requirements.txt
```

## Usage

### Basic (stops at QR verification)

```bash
python3 gmail_creator.py
```

The script runs until the phone verification step, then displays a QR code. **You must scan this QR code with your phone to continue.**

### With phone number (auto-submit)

```bash
python3 gmail_creator.py +628****7890
```

If a phone number is provided, the script auto-fills and submits it. However, SMS verification still requires manual completion.

### Output

- **Screenshots**: Saved at `/home/ubuntu/gmail_*.png` at each step
- **Account Info**: Saved at `/home/ubuntu/gmail_accounts.txt` if account is successfully created
- **Console Output**: Progress at each step (1-8)

## Workflow Detail

```
Step 1: Navigate to accounts.google.com/SignUp
  └─ Chrome browser launched (headless via Xvfb)

Step 2: Fill Name (First + Last)
  └─ Random names from preset: alex.smith, jordan.wilson, taylor.brown, etc.
  └─ Click "Next" to continue

Step 3: Birthday + Gender
  └─ Day/Year: filled via text input (ID: day, year)
  └─ Month: custom dropdown → click → HOME → ENTER (January)
  └─ Gender: custom dropdown → click → ARROW_DOWN x2 → ENTER (Rather not say)
  └─ Click "Next"

Step 4: Username
  └─ Format: firstname.lastnameXXXX (XXXX = random 4 digits)
  └─ If username taken → auto regenerate (max 5 attempts)
  └─ Click "Next"

Step 5: Password
  └─ 16 characters: random letters + numbers + special chars (!@#$%)
  └─ Fields: Passwd + PasswdAgain
  └─ Click "Next"

Step 6: Phone Verification ⚠️
  └─ QR CODE appears — MUST scan manually with phone
  └─ No skip or alternative options available
  └─ Script stops here

Step 7: Recovery Email (skip)
Step 8: Terms Accept (auto)
```

## Technical Details

### ChromeDriver Version

```python
# Chromium v149 installed on system
# undetected-chromedriver needs version_main=149
self.driver = uc.Chrome(options=options, version_main=149)
```

### Custom Dropdown Handling

Google's signup form uses **custom React combobox** (not standard `<select>`):

```python
# Month dropdown — select January (first option)
month_cb = driver.find_element(By.XPATH, '//div[@role="combobox"][contains(.,"Month")]')
month_cb.click()
actions.send_keys(Keys.HOME).send_keys(Keys.ENTER).perform()

# Gender dropdown — select "Rather not say" (3rd option)
gender_cb = driver.find_element(By.XPATH, '//div[@role="combobox"][contains(.,"Gender")]')
gender_cb.click()
actions.send_keys(Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER).perform()
```

### Anti-Bot Measures Bypassed

| Measure | How Bypassed |
|---------|-------------|
| `navigator.webdriver` flag | `delete navigator.__proto__.webdriver` via init script |
| Automation controlled | `--disable-blink-features=AutomationControlled` |
| Random delays | `time.sleep(random.uniform(2, 5))` between actions |
| User agent | Random UA from preset list |
| Autocomplete overlay | JS remove + keyboard navigation |
| ChromeDriver version | `version_main=149` matched to system Chrome |

## Troubleshooting

### ChromeDriver Version Mismatch

```
SessionNotCreatedException: ChromeDriver v150 vs Chrome v149
```

**Fix**: Ensure `version_main=149` in `uc.Chrome()`

### Xvfb Required for Headless

```
Error: cannot open display
```

**Fix**:
```bash
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
python3 gmail_creator.py
```

### Phone Verification Has No Bypass

The script **cannot bypass** phone verification. This is a Google security feature with no reliable public bypass API.

**Alternatives to try**:
1. Use your own Indonesian phone number (QR scan takes ~30 seconds)
2. Use Google Voice / VoIP number (weak against Google detection)
3. Use Gmail Workspace trial (14 days, no phone required)
4. Buy pre-verified Gmail accounts

## Limitations

- ❌ Cannot bypass phone verification (QR code required)
- ❌ Cannot bypass CAPTCHA if it appears early in signup
- ❌ No batch creation (1 account per run)
- ⚠️ Username generation is simple — possible collisions
- ⚠️ VPS proxy IP can be blacklisted by Google

## Disclaimer

This tool is for **educational and research purposes only**. Any use for spam, abuse, or violation of Google Terms of Service is the user's own responsibility.

- Google actively blocks automated signups from VPS/datacenter IP ranges
- Phone verification is a security feature that cannot be fully bypassed
- Abuse may result in permanent IP ban

## Roadmap

- [ ] Batch creation support with delays between accounts
- [ ] 2captcha API integration for CAPTCHA solving
- [ ] Better username generation (reduce collision rate)
- [ ] Proxy rotation pool
- [ ] Session state persistence (resume from failed step)

## License

MIT

---

> **⭐ Star this repo & follow [yossweh](https://github.com/yossweh) for more tools and updates!**
