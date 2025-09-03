from socket import *        # 소켓 모듈(TCP/IP 통신에 사용)
import threading            # 스레드 모듈(멀티스레드에 사용)
import sys                  # 표준 입출력에 사용


class ChatClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.sock = None            # 클라이언트 소켓
        self.is_running = False     # 클라이언트 실행 상태 플래그


    def start(self):
        self.sock = socket(AF_INET, SOCK_STREAM)    # IPv4, TCP 소켓 생성
        try:
            self.sock.connect((self.host, self.port)) # 서버에 연결
        except ConnectionRefusedError:
            print('서버에 연결할 수 없습니다.')
            return

        self.is_running = True

        # 서버로부터 수신하는 스레드
        thread = threading.Thread(target=self.receive_loop, daemon=True)
        thread.start()

        try:
            # 사용자 입력 반복
            while self.is_running:
                msg = sys.stdin.readline().rstrip('\n') # 한 줄 입력 및 개행 문자 제거
                if not msg:
                    continue
                self.sock.sendall((msg + '\n').encode('utf-8'))
                if msg == '/종료':  # 종료 명령어 입력 시
                    self.is_running = False
                    break
        except KeyboardInterrupt:
            self.sock.sendall('/종료\n'.encode('utf-8'))
        finally:
            try:
                self.sock.close()
            except OSError:
                pass

    # 서버로부터 메시지 수신
    def receive_loop(self):
        while self.is_running:
            try:
                data = self.sock.recv(1024)
            except OSError:
                break
            if not data:    # 서버가 종료되었거나 연결이 끊어짐
                break
            sys.stdout.write(data.decode('utf-8'))     # 표준 출력
            sys.stdout.flush()               # 출력 버퍼 비우기
        self.is_running = False


def main():
    client = ChatClient(host='127.0.0.1', port=5000)
    client.start()


if __name__ == '__main__':
    main()
