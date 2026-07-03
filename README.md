# Gmail Account Creator

Automated Gmail account creation tool using Selenium + undetected-chromedriver with anti-bot bypass. Supports custom dropdown handling, keyboard navigation, and proxy rotation.

## What is this tool?

Ini tool untuk **otomatisasi pembuatan akun Gmail** secara semi-otomatis. Tool ini mengotomasi 5 dari 8 tahap signup Google:

1. ✅ Navigasi ke halaman signup
2. ✅ Isi nama depan & belakang
3. ✅ Isi tanggal lahir & gender (via keyboard navigation untuk custom dropdown)
4. ✅ Pilih username (auto-retry jika sudah terpakai)
5. ✅ Isi password & confirm password
6. ⚠️ Verifikasi HP (berhenti di QR code)
7. ⏭️ Email recovery (skip)
8. ⏭️ Terms & conditions (auto-accept)

## Why semi-automatic?

Google menggunakan sistem verifikasi yang **tidak bisa di-bypass sepenuhnya via automation**:

- **QR Code Verification**: Google menampilkan QR code yang harus discan menggunakan HP fisik. Ini adalah mekanisme keamanan untuk memverifikasi bahwa user adalah manusia, bukan bot.
- **Device Fingerprinting**: Google menganalisis browser fingerprint, IP address, dan behavior pattern untuk mendeteksi automation.
- **No Skip Option**: Tidak ada tombol "skip" atau "try another way" di halaman verifikasi.

**Kesimpulan**: Tool ini mengotomasi sebanyak mungkin, tapi **verifikasi HP harus dilakukan manual** dengan scan QR code dari HP Anda sendiri.

## Features

- **Undetected ChromeDriver** — bypass bot detection dengan `undetected-chromedriver`
- **Custom Combobox Navigation** — Google's new UI menggunakan custom React dropdowns, bukan `<select>` standar. Tool ini menggunakan keyboard navigation (ArrowDown + Enter) untuk memilih option
- **Proxy Support** — EU residential proxy (Frankfurt) untuk meningkatkan acceptance rate
- **Random Credential Generation** — nama, username, dan password digenerate secara random
- **Screenshot Capture** — screenshot di setiap step untuk debugging
- **Auto-retry** — username otomatis generate ulang jika sudah terpakai
- **Xvfb Headless** — bisa jalan di VPS/headless environment

## Requirements

```bash
# Python 3.11+
pip install selenium undetected-chromedriver

# Xvfb untuk headless display (jika jalankan di VPS)
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

Script akan jalan sampai tahap verifikasi HP, lalu menampilkan QR code. **Anda harus scan QR code ini dengan HP Anda untuk melanjutkan.**

### With phone number (auto-submit)

```bash
python3 gmail_creator.py +6281234567890
```

Jika nomor HP diberikan, script akan otomatis mengisi dan submit nomor HP. Namun verifikasi SMS tetap perlu dilakukan manual.

### Output

- **Screenshot**: Disimpan di `/home/ubuntu/gmail_*.png` di setiap step
- **Account Info**: Disimpan di `/home/ubuntu/gmail_accounts.txt` jika akun berhasil dibuat
- **Console Output**: Progress di setiap step (1-8)

## Workflow Detail

```
Step 1: Navigate ke accounts.google.com/SignUp
  └─ Chrome browser launched (headless via Xvfb)
  └─ Proxy: 86.38.236.148:6432 (EU residential)

Step 2: Isi Nama (First + Last)
  └─ Random nama dari preset: alex.smith, jordan.wilson, taylor.brown, etc.
  └─ Klik "Next" untuk lanjut

Step 3: Tanggal Lahir + Gender
  └─ Day/Year: diisi via text input (ID: day, year)
  └─ Month: dropdown custom → click → HOME → ENTER (January)
  └─ Gender: dropdown custom → click → ARROW_DOWN x2 → ENTER (Rather not say)
  └─ Klik "Next"

Step 4: Username
  └─ Format: firstname.lastnameXXXX (XXXX = random 4 digit)
  └─ Jika username taken → auto generate ulang (max 5 attempts)
  └─ Klik "Next"

Step 5: Password
  └─ Panjang 16 karakter: random letters + numbers + special chars (!@#$%)
  └─ Field: Passwd + PasswdAgain
  └─ Klik "Next"

Step 6: Phone Verification ⚠️
  └─ QR CODE appears — MUST scan manually with phone
  └─ Tidak ada opsi skip atau alternative
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

### Proxy Configuration

```python
# EU Residential Proxy (Frankfurt)
PROXY = "http://mnfsfxoq:a4iwyu00aimj@86.38.236.148:6432"
# NOTE: Proxy DISABLED for Google (causes issues)
# Google lebih baik tanpa proxy dari VPS
```

### Custom Dropdown Handling

Google's signup form menggunakan **custom React combobox** (bukan standard `<select>`):

```python
# Month dropdown
month_cb = driver.find_element(By.XPATH, '//div[@role="combobox"][contains(.,"Month")]')
month_cb.click()
actions.send_keys(Keys.HOME).send_keys(Keys.ENTER).perform()  # Select January

# Gender dropdown
gender_cb = driver.find_element(By.XPATH, '//div[@role="combobox"][contains(.,"Gender")]')
gender_cb.click()
actions.send_keys(Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER).perform()  # Rather not say
```

### Anti-Bot Measures Bypassed

| Measure | How Bypassed |
|---------|-------------|
| `navigator.webdriver` | `delete navigator.__proto__.webdriver` |
| Automation flag | `--disable-blink-features=AutomationControlled` |
| Random delays | `time.sleep(random.uniform(2, 5))` |
| User agent | Random UA dari preset |
| Autocomplete overlay | JS remove + keyboard nav |
| ChromeDriver version | `version_main=149` match system Chrome |

## Troubleshooting

### ChromeDriver Version Mismatch

```
SessionNotCreatedException: ChromeDriver v150 vs Chrome v149
```

**Fix**: Pastikan `version_main=149` di `uc.Chrome()`

### Xvfb Required

```
Error: cannot open display
```

**Fix**: 
```bash
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
python3 gmail_creator.py
```

### No CAPTCHA/Phone Verification Bypass

Script **tidak bisa bypass** verifikasi HP. Ini adalah security feature Google yang tidak memiliki public API atau bypass method yang reliable.

**Alternatif yang bisa dicoba**:
1. Gunakan nomor HP Indonesia sendiri (scan QR cepat, 30 detik)
2. Gunakan Google Voice / VoIP number (lemah ke Google)
3. Gunakan Gmail Workspace trial (14 hari, no phone required)
4. Beli akun Gmail yang sudah terverifikasi

## Limitations

- ❌ Tidak bisa bypass phone verification (QR code required)
- ❌ Tidak bisa bypass CAPTCHA jika muncul di tahap awal
- ❌ Tidak support batch creation (1 akun per run)
- ⚠️ Username generation sederhana — kemungkinan collision
- ⚠️ Proxy di-VPS bisa di-blacklist oleh Google

## Disclaimer

Tool ini dibuat untuk **educational and research purposes only**. Penggunaan untuk spam, abuse, atau melanggar Google Terms of Service adalah tanggung jawab pengguna sendiri.

- Google actively blocks automated signups dari IP range VPS/datacenter
- Phone verification adalah security feature yang tidak mungkin di-bypass sepenuhnya
- Abuse bisa menyebabkan IP ban permanen

## Future Improvements

- [ ] Support untuk batch creation dengan delay
- [ ] Integrasi dengan 2captcha API untuk CAPTCHA solving
- [ ] Better username generation (less collision)
- [ ] Proxy rotation pool
- [ ] Session state persistence (resume dari step yang gagal)

## License

MIT

---

> **⭐ Star this repo & follow [yossweh](https://github.com/yossweh) for more tools and updates!**
