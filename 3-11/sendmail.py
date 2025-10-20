import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import os
from dotenv import load_dotenv

load_dotenv() # .env 파일에 있는 환경변수 로드

def send_email(sender, password, receivers, subject, body, files_path=None):
    try:
        # 메일 컨테이너 (본문 + 첨부 가능)
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ','.join(receivers) if isinstance(receivers, list) else receivers # 여러 명에게 보낼 때 ,로 구분
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # 첨부파일 추가
        for file_path in files_path or []:  # None이거나 빈 값일 때도 에러 안 나도록 처리
            if file_path and os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    file_data = MIMEBase('application', 'octet-stream') # 모든 종류의 바이너리 파일 가능
                    # file_data = MIMIEBase('application', 'pdf')       # PDF 파일만 가능
                    file_data.set_payload(f.read())                     # 파일 내용을 MIMEBase 객체에 채움
                    encoders.encode_base64(file_data)            # 바이너리 데이터를 텍스트로 인코딩
                    # "이건 첨부파일" 헤더 추가
                    file_data.add_header(
                        'Content-Disposition',
                        f'attachment; filename={os.path.basename(file_path)}'
                    )
                    msg.attach(file_data)           # 메일 컨테이너에 첨부파일 추가
            else:
                print(f'첨부 파일이 없습니다: {file_path}')
                continue

        # Gmail SMTP 서버 연결 (587 포트, TLS)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() # Transport Layer Security (보안 처리)
            server.login(sender, password) # SMTP 서버에 로그인
            server.sendmail(sender, receivers, msg.as_string()) # msg.as_string() : 메일 컨테이너를 문자열로 변환
            """
            server.starttls()
            server.login(user=sender, password=password)
            server.sendmail(
                from_addr=sender,
                to_addrs='email@naver.com',
                msg="Subject:Hello\n\nThis is the body of my email"
            )
            """
        
        print('메일이 발송되었습니다')
        return True

    except smtplib.SMTPAuthenticationError:
        print('로그인 실패: 이메일 주소 또는 비밀번호(App Password)를 확인하세요.')
    except FileNotFoundError:
        print('첨부 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'메일 전송 중 오류 발생: {e}')
    
    return False


if __name__ == '__main__':
    sender_email = 'lim2309043@gmail.com' # 보내는 Gmail 주소
    sender_password = os.getenv('GMAIL_APP_PASSWORD') or getpass.getpass('Password (App Password): ') # 패스워드 입력 (앱 비밀번호)
    receiver_email = ['dlaxoals14@naver.com', 'dlaxoals54@m365.dongyang.ac.kr'] # 받는 사람 이메일
    subject = '파이썬으로 이메일 보내기 제목 테스트'
    body = '안녕하세요! 파이썬으로 이메일을 보내는 테스트입니다.'
    files = ['3-11/test.txt', '3-11/test2.pdf']  # 첨부파일 경로 (없으면 None)

    send_email(sender_email, sender_password, receiver_email, subject, body, files)