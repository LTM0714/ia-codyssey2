from socket import *        # 소켓 모듈(TCP/IP 통신에 사용)
import threading            # 스레드 모듈(멀티스레드에 사용)


class ChatServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}               # 접속된 클라이언트 소켓과 닉네임을 매핑 {소켓:닉네임}
        self.lock = threading.Lock()    # 멀티스레드 환경에서 clients 딕셔너리 보호


    def start(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)           # IPv4, TCP 소켓 생성
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 주소 재사용 옵션 설정
        self.server_socket.bind((self.host, self.port))             # 서버 주소/포트 바인딩
        self.server_socket.listen(3)                                # 최대 3개의 클라이언트 대기

        print('%d번 포트로 접속 대기중...'%self.port)

        self.server_socket.settimeout(1.0)  # accept()가 1초마다 타임아웃되도록 설정

        try:
            while True:
                try:
                    connectionSock, addr = self.server_socket.accept()
                    # 클라이언트 처리용 스레드 생성
                    thread = threading.Thread(target=self.handle_client, args=(connectionSock, addr), daemon=True)
                    thread.start()
                except timeout:
                    continue
        except KeyboardInterrupt:
            print('\n서버가 종료됩니다.')
        finally:
            self.shutdown() # 서버 소켓과 클라이언트 소켓 정리


    # 각 클라이언트별로 메시지 처리
    def handle_client(self, conn, addr):
        try:
            conn.sendall('닉네임을 입력하세요: '.encode('utf-8'))
            nickname = conn.recv(1024).decode('utf-8').strip()
            if not nickname:
                nickname = f'{addr[0]}:{addr[1]}'   # 닉네임이 없으면 IP:포트로 설정

            nickname = self.get_unique_nickname(nickname) # 중복 닉네임 처리

            # clients 딕셔너리에 추가 (동기화)
            # 여러 클라이언트가 동시에 접속하거나 종료할 때 문제 방지
            with self.lock:
                self.clients[conn] = nickname

            self.broadcast(f'{nickname}님이 입장하셨습니다.')
            print(f'접속: {nickname} (현재 접속자 {len(self.clients)}명)')

            while True:
                msg = conn.recv(1024).decode('utf-8').strip()
                # msg가 빈 문자열이면 클라이언트가 종료했거나 연결이 끊어진 것
                if not msg:
                    break
                # 종료 명령어 처리
                if msg == '/종료':
                    self.broadcast(f'{nickname}님이 퇴장하셨습니다.')
                    print(f'{nickname}님이 퇴장하셨습니다.')
                    break
                 # 귓속말 처리, /귓속말 [닉네임] [메시지]
                if msg.startswith('/귓속말'):
                    parts = msg.split(' ', 2)
                    if len(parts) < 3:
                        conn.sendall('사용법: /귓속말 [닉네임] [메시지]\n'.encode('utf-8'))
                        continue
                    target_name, private_msg = parts[1], parts[2]
                    target_conn = None
                    # 대상 클라이언트 찾기
                    with self.lock:
                        for c, n in self.clients.items():
                            if n == target_name:
                                target_conn = c
                                break
                    if target_conn:
                        # 귓속말 전송
                        self.broadcast(f'(귓속말) {nickname}> {private_msg}', target_conn=target_conn)
                    else:
                        conn.sendall(f'{target_name}님을 찾을 수 없습니다.\n'.encode('utf-8'))
                    continue
                # 일반 메시지 브로드캐스트
                self.broadcast(f'{nickname}> {msg}')
        except ConnectionResetError:
            # 클라이언트가 종료했을 때 예외 처리
            pass
        finally:
            with self.lock:
                if conn in self.clients:
                    left_user = self.clients.pop(conn)
                    print(f'종료: {left_user} (현재 접속자 {len(self.clients)}명)')
            try:
                conn.close()
            except OSError:
                pass
    
    
    # 전체 또는 특정 클라이언트에게 메시지 전송
    def broadcast(self, message, target_conn=None):
        data = (message + '\n').encode('utf-8')
        with self.lock:
            dead = []  # 연결 끊긴 클라이언트 목록
            for conn in self.clients:
                # target_conn이 None이면 전체, 아니면 특정 클라이언트에게만 전송
                if target_conn is None or conn == target_conn:
                    try:
                        conn.sendall(data)
                    except OSError:
                        dead.append(conn)
            # 연결 끊긴 소켓 제거, 없으면 None 반환
            for conn in dead:
                self.clients.pop(conn, None)


    # 중복 닉네임 처리
    def get_unique_nickname(self, nickname):
        original = nickname
        count = 1
        with self.lock:
            existing_name = set(self.clients.values())
            while nickname in existing_name:
                count += 1
                nickname = f"{original}({count})"
        return nickname


    # 서버 종료 시 모든 소켓 정리
    def shutdown(self):
        with self.lock:
            # 모든 클라이언트 소켓 닫기
            for conn in list(self.clients.keys()):
                try:
                    conn.close()
                except OSError:
                    pass
            self.clients.clear()    # 딕셔너리 초기화
        # 서버 소켓 정리
        if self.server_socket:
            try:
                self.server_socket.close()
            except OSError:
                pass
        print('서버 종료 완료.')


def main():
    server = ChatServer(host='0.0.0.0', port=5000)
    server.start()


if __name__ == '__main__':
    main()
