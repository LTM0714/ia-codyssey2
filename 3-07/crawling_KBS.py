import requests
from bs4 import BeautifulSoup

def scrape_page():
    # 웹 페이지 요청
    url = 'https://news.kbs.co.kr/news/pc/main/main.html'
    response = requests.get(url)
    response.encoding = 'utf-8'  # 한글 깨짐 방지

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser')

    # 웹 페이지 <title> 태그 내용 출력
    title = soup.title.text 
    print('웹 페이지 제목:', title)

    # div.box-contents 안의 p.title 요소 찾기
    headlines = []
    for item in soup.select('div.box-contents p.title'):
        text = item.get_text(strip=True) # 텍스트만 추출하고 양쪽 공백 제거
        if text:
            headlines.append(text)

    return headlines


def crawl_weather():
    url = "https://www.weather.go.kr/w/weather/forecast/short-term.do"  # 기상청 단기예보 페이지
    response = requests.get(url)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, "html.parser")

    # 웹 페이지 <title> 태그 내용 출력
    title = soup.title.text 
    print('\n웹 페이지 제목:', title)

    weather_list = []
    for item in soup.find('section', class_='page-wrap').find_all('span')[8:-8]:
        text = item.get_text(strip=True)
        if text:
            weather_list.append(text)

    return weather_list



if __name__ == '__main__':
    # 뉴스 헤드라인
    news_list = scrape_page()
    for idx, headline in enumerate(news_list, start=1):
        print(f'{idx}. {headline}')

    # 날씨
    weather = crawl_weather()
    for info in weather:
        print(info)
