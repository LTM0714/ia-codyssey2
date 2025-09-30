from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def main(user_id, user_pw):
    # 웹 드라이버의 버전 관리를 자동으로 해주는 ChromeDriverManager 사용
    # Service 객체를 통해 드라이버 경로 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # 네이버 로그인 페이지 열기
    driver.get('https://nid.naver.com/nidlogin.login')

    # 로그인 정보 입력
    driver.find_element(By.XPATH, '//*[@id="id"]').send_keys(user_id) # XPath는 웹페이지에서 요소를 선택하는데 사용되는 경로 표현식
    driver.find_element(By.XPATH, '//*[@id="pw"]').send_keys(user_pw)
    driver.find_element(By.ID, "log.login").click() # ID는 HTML 요소의 고유 식별자

    input('로그인 완료 후 Enter 키를 누르세요...')

    nickname = driver.find_element(By.CSS_SELECTOR, '[class*="MyView-module__nickname"]').text
    email = driver.find_element(By.CSS_SELECTOR, '[class*="MyView-module__desc_email"]').text
    print(f'로그인된 닉네임: {nickname}')
    print(f'이메일 주소: {email}\n')

    # 네이버 메일 페이지로 이동
    driver.get('https://mail.naver.com/')
    time.sleep(3)

    # 메일 제목 크롤링
    titles = []
    mail_elements = driver.find_elements(By.CSS_SELECTOR, 'a.mail_title_link span.text') # CSS 선택자는 HTML 요소를 선택하는데 사용되는 패턴
    for mail in mail_elements[:5]:  # 앞 5개만 가져오기
        titles.append(mail.text)

    driver.quit()

    return titles


if __name__ == '__main__':
    id = 'my_id'
    pw = 'my_pw'
    mail_titles = main(id, pw)
    
    print('내 메일 제목 목록:')
    for idx, title in enumerate(mail_titles, start=1):
        print(f"{idx}. {title}")
