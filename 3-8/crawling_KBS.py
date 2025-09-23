from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def main(user_id, user_pw):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # 네이버 로그인 페이지 열기
        driver.get("https://nid.naver.com/nidlogin.login")

        # 로그인 정보 입력
        driver.find_element(By.XPATH, '//*[@id="id"]').send_keys(user_id) # XPath는 웹페이지에서 요소를 선택하는데 사용되는 경로 표현식
        driver.find_element(By.XPATH, '//*[@id="pw"]').send_keys(user_pw)
        driver.find_element(By.ID, "log.login").click() # ID는 HTML 요소의 고유 식별자

        time.sleep(20)  # 로그인 처리 대기

        # 네이버 메일 페이지로 이동
        driver.get("https://mail.naver.com/")
        time.sleep(3)

        # 메일 제목 크롤링
        titles = []
        mail_elements = driver.find_elements(By.CSS_SELECTOR, 'a.mail_title_link span.text') # CSS 선택자는 HTML 요소를 선택하는데 사용되는 패턴
        for mail in mail_elements[:5]:  # 앞 5개만 가져오기
            titles.append(mail.text)

        return titles

    finally:
        driver.quit()


if __name__ == "__main__":
    user_id = "dlaxoals14"
    user_pw = "qwer1234!"
    mail_titles = main(user_id, user_pw)
    
    print("내 메일 제목 목록:")
    for idx, title in enumerate(mail_titles, start=1):
        print(f"{idx}. {title}")
