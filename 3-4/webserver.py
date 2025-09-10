from http.server import HTTPServer, BaseHTTPRequestHandler
import http.client
import json


def get_ip_location(ip):
    # ip-api.com 무료 API 활용
    try:
        conn = http.client.HTTPConnection("ip-api.com", timeout=5)
        conn.request("GET", f"/json/{ip}?fields=status,country,regionName,city,query")
        response = conn.getresponse()
        if response.status == 200:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        return {"status": "fail", "message": str(e)}
    return {"status": "fail"}


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('GET 요청이 들어왔습니다.')

        # index.html 파일 읽기
        try:
            with open('3-4/index.html', 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<h1>404 Not Found</h1>')
            return None
        
        # 200 응답 전송
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        # index.html 내용 전송
        self.wfile.write(content.encode('utf-8'))

        client_ip = self.client_address[0]

        # 위치 정보 조회 (로컬호스트는 조회 불가)
        if client_ip != '127.0.0.1':
            location = get_ip_location(client_ip)
            if location:
                print(f"위치 정보: {location['country']} {location['regionName']} {location['city']}")
        else:
            print('[위치 정보] 조회 실패 (로컬호스트)')

    def do_POST(self):
        print('POST 요청이 들어왔습니다.')


def run():
    httpd = HTTPServer(('127.0.0.1', 8080), MyHandler)
    print('Server Start')
    httpd.serve_forever()
    print('Server End')


if __name__ == '__main__':
    run()
