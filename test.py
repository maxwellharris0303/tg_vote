from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import urllib.request
from pydub import AudioSegment
import whisper

options = webdriver.ChromeOptions()
# options.add_argument('--headless=new')

driver = webdriver.Chrome(options=options)

driver.get("https://rondoniaovivo.com/enquete/comovoceclassificaagestaodoprefeitoivairfernandesemmontenegro/984/")

try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class=\"fc-button fc-cta-consent fc-primary-button\"]"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class=\"btn btn-veja-mais-policia\"]"))).click()
except:
    pass

page_height = driver.execute_script("return document.body.scrollHeight")
print(page_height)
scroll_distance = page_height // 20
driver.execute_script(f"window.scrollTo(0, {scroll_distance});")
sleep(2)
radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type=\"radio\"]")
print(len(radio_buttons))
# radio_buttons[0].click()
driver.execute_script(f"document.querySelectorAll('input[type=\"radio\"]')[0].click()")

sleep(1)
driver.execute_script("arguments[0].scrollIntoView(false);", driver.find_element(By.CSS_SELECTOR, "select[id=\"editorias\"]"))
captcha_frame = driver.find_element(By.CSS_SELECTOR, "iframe[title=\"reCAPTCHA\"]")
driver.switch_to.frame(captcha_frame)

captcha_button = driver.find_element(By.CSS_SELECTOR, "span[class=\"recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox\"]")

captcha_button.click()

sleep(2)
try:
    driver.switch_to.window(driver.window_handles[0])
    scroll_distance = page_height // 30
    driver.execute_script(f"window.scrollTo(0, {scroll_distance});")
    sleep(2)

    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe[title=\"recaptcha challenge expires in two minutes\"]"))
    sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button[id=\"recaptcha-audio-button\"]").click()
    sleep(2)
    audio_link = driver.find_element(By.CSS_SELECTOR, "audio[id=\"audio-source\"]").get_attribute('src')
    print(audio_link)
    sleep(2)
    urllib.request.urlretrieve(audio_link, "111.mp3")

    mp3_audio = AudioSegment.from_mp3('111.mp3')

    # Convert MP3 to WAV
    wav_path = 'audio_file.wav'
    mp3_audio.export(wav_path, format='wav')

    model = whisper.load_model("base")
    result = model.transcribe(wav_path, fp16=False)

    print(result['text'])

    driver.find_element(By.CSS_SELECTOR, "input[id=\"audio-response\"]").send_keys(result['text'])
    sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button[id=\"recaptcha-verify-button\"]").click()
except:
    pass
sleep(2)
driver.switch_to.window(driver.window_handles[0])
sleep(3)
# driver.find_element(By.CSS_SELECTOR, "button[class=\"btn btn-danger btn-lg\"]").click()
driver.execute_script(f"document.querySelectorAll('button[class=\"btn btn-danger btn-lg\"]')[0].click()")
sleep(5)
driver.quit()
