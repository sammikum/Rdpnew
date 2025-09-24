import pyautogui as pag
import time
import requests
import os

# Wait for system/UI readiness
time.sleep(40)

def click_button(image_path, retries=3, interval=5, confidence=0.8):
    for attempt in range(retries):
        coords = pag.locateCenterOnScreen(image_path, confidence=confidence)
        if coords:
            print(f"Found button '{image_path}' at {coords}, clicking...")
            pag.click(coords.x, coords.y, duration=1)
            return True
        else:
            print(f"Button '{image_path}' not found. Retry {attempt+1} of {retries}...")
            time.sleep(interval)
    print(f"Failed to find button '{image_path}' after {retries} retries.")
    return False

img_filename = 'NewAvicaRemoteID.png'

def upload_image_to_gofile(img_filename):
    url = 'https://store1.gofile.io/uploadFile'
    try:
        with open(img_filename, 'rb') as img_file:
            files = {'file': img_file}
            response = requests.post(url, files=files)
            response.raise_for_status()
            result = response.json()
            if result['status'] == 'ok':
                download_page = result['data']['downloadPage']
                with open('show.bat', 'a') as bat_file:
                    bat_file.write(f'\necho Avica Remote ID : {download_page}')
                return download_page
            else:
                print("Upload error:", result.get('status'))
                return None
    except Exception as e:
        print(f"Failed to upload image: {e}")
        return None

print("Waiting for system readiness...")
time.sleep(10)

# Step 1: Click Install button
if not click_button('install_button.png', retries=3, interval=15):
    print("Install button action failed; exiting.")
    exit(1)

# Step 2: Click Launch Avica button
if not click_button('launch_avica.png'):
    print("Launch Avica button not found; continuing anyway.")

# Step 3: Click "Later Update" button (optional)
click_button('later_update.png', retries=2)

# Step 4: Click Allow Remote Access button repeatedly until it's gone or max attempts
max_attempts = 8
for attempt in range(max_attempts):
    if not click_button('allow_rdp.png', retries=1):
        print("Allow Remote Access button not found; assuming granted or not present.")
        break
    time.sleep(1)

# Step 5: Launch Avica executable explicitly
avica_path = r"C:\Program Files (x86)\Avica\Avica.exe"
if os.path.exists(avica_path):
    os.system(f'"{avica_path}"')
    time.sleep(5)
else:
    print(f"Avica executable not found at {avica_path}")

# Re-click Allow Remote Access once after launch
click_button('allow_rdp.png')

time.sleep(10)

# Take screenshot and upload to GoFile.io
pag.screenshot().save(img_filename)
gofile_link = upload_image_to_gofile(img_filename)
if gofile_link:
    print(f"Image uploaded successfully. Link: {gofile_link}")
else:
    print("Failed to upload the image.")

print("Script complete!")
