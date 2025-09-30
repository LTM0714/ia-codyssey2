from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
import pyperclip
import time
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def main(user_id, user_pw):
    # 웹 드라이버의 버전 관리를 자동으로 해주는 ChromeDriverManager 사용
    # Service 객체를 통해 드라이버 경로 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://nid.naver.com/nidlogin.login')
    time.sleep(2)

    # ClipBoard 복사/붙이기
    driver.find_element(By.XPATH, '//*[@id="id"]').click()
    pyperclip.copy(user_id)
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    
    pw_input = driver.find_element(By.XPATH, '//*[@id="pw"]')
    pw_input.click()
    pyperclip.copy(user_pw)
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    
    pw_input.send_keys(Keys.RETURN)
    time.sleep(3)
   
    nickname = driver.find_element(By.CSS_SELECTOR, '[class*="MyView-module__nickname"]').text
    email = driver.find_element(By.CSS_SELECTOR, '[class*="MyView-module__desc_email"]').text
    print(f'로그인된 닉네임: {nickname}')
    print(f'이메일 주소: {email}\n')

    driver.get('https://mail.naver.com/')
    time.sleep(3)

    titles = []
    mail_elements = driver.find_elements(By.CSS_SELECTOR, 'a.mail_title_link span.text')
    for mail in mail_elements[:5]:
        titles.append(mail.text)

    driver.quit()

    return titles


if __name__ == '__main__':
    id = os.getenv('NAVER_ID')  # 또는 os.environ.get('NAVER_ID')
    pw = os.getenv('NAVER_PW')
    
    if not id or not pw:
        print("환경변수 NAVER_ID 또는 NAVER_PW가 설정되지 않았습니다.")
    else:
        mail_titles = main(id, pw)
        print('내 메일 제목 목록:')
        for idx, title in enumerate(mail_titles, start=1):
            print(f"{idx}. {title}")
