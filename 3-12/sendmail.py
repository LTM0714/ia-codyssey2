import smtplib
import getpass
import os
import csv
from email.message import EmailMessage
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv


# ---환경변수 관리 클래스---
class Config:
    def __init__(self):
        load_dotenv(find_dotenv())   # .env 파일에 있는 환경변수 로드
        self.GOOGLE_SENDER_EMAIL = os.getenv('GOOGLE_SENDER_EMAIL')
        self.GOOGLE_APP_PASSWORD = os.getenv('GOOGLE_APP_PASSWORD')
        self.NAVER_SENDER_EMAIL = os.getenv('NAVER_SENDER_EMAIL')
        self.NAVER_APP_PASSWORD = os.getenv('NAVER_APP_PASSWORD')

        self.SMTP_SERVERS = {
            'gmail': ('smtp.gmail.com', 587),
            'naver': ('smtp.naver.com', 587)
        }

    def get_smtp_info(self, service_name):
        return self.SMTP_SERVERS.get(service_name)

    
# ---수신자 관리 클래스---
class RecipientManager:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        
    def load_recipients(self):
        recipients = []
        try:
            with open(self.csv_path, encoding='utf-8', newline='')as f:
                reader = csv.DictReader(f) # csv 파일을 딕셔너리 형태로 읽기
                
                skipped = 0 # 잘못된 형식의 수신자 수
                for row in reader:
                    name = (row.get('이름') or '').strip()
                    email = (row.get('이메일') or '').strip()
                    if not name or not email or '@' not in email:
                        skipped += 1
                        continue
                    recipients.append({'name': name, 'email': email})
                if skipped:
                    print(f'잘못된 형식의 수신자 {skipped}명은 건너뜁니다.')
        except FileNotFoundError:
            print(f'CSV 파일을 찾을 수 없습니다: {self.csv_path}')
        except Exception as e:
            print(f'CSV 파일 읽기 오류 발생: {e}')
        return recipients

# ---이메일 전송 클래스---
class EmailSender:
    def __init__(self, smtp_info, sender, password):
        self.smtp_info = smtp_info
        self.sender_email = sender
        self.app_password = password
        self.server = None

    # SMTP 서버 연결
    def connect(self):
        try:
            self.server = smtplib.SMTP(self.smtp_info[0], self.smtp_info[1])
            self.server.starttls() # Transport Layer Security (보안 처리)
            self.server.login(self.sender_email, self.app_password) # SMTP 서버에 로그인
            print('SMTP 서버에 성공적으로 연결되었습니다.')
            return True
        
        except smtplib.SMTPAuthenticationError:
            print('로그인 실패: 이메일 주소 또는 비밀번호(App Password)를 확인하세요.')
        except Exception as e:
            print(f'메일 전송 중 오류 발생: {e}')       
        return False
    
    # SMTP 서버 연결 종료
    def disconnect(self):
        if self.server:
            try:
                self.server.quit()
                print('SMTP 서버 연결이 종료되었습니다.')
            except Exception as e:
                print(f'SMTP 서버 연결 종료 중 오류 발생: {e}')
        else:
            print('SMTP 서버가 연결되어 있지 않습니다.')
    
    # 이메일 메시지 생성
    def create_message(self, recipient_email, subject, body, files_path=None):
        msg = EmailMessage()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        if '<html' in body.lower() or '<body' in body.lower() or '<div' in body.lower():
            # 일부 이메일 클라이언트나 보안 정책 때문에 HTML을 표시하지 못할 때, 사용자는 텍스트 형태의 대체 내용을 봐야 함
            # get_text()는 태그를 제거하면서 텍스트 내용을 유지
            plain_text = BeautifulSoup(body, 'html.parser').get_text(separator='\n', strip=True)
            # 플레인텍스트를 먼저 넣어야 폴백이 제대로 작동
            msg.set_content(plain_text.strip(), subtype='plain', charset='utf-8')
            msg.add_alternative(body, subtype='html', charset='utf-8')
        else:
            msg.set_content(body)

        # 첨부파일 추가
        for file_path in files_path or []:  # None이거나 빈 값일 때도 에러 안 나도록 처리
            if not file_path:
                continue
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    msg.add_attachment(
                        f.read(),
                        maintype='application',
                        subtype='octet-stream',
                        filename=os.path.basename(file_path)
                    )
            else:
                print(f'첨부 파일이 없습니다: {file_path}')
                continue
        return msg


    # 여러 명에게 개별 전송
    def send_individual_emails(self, recipients, subject, body, files_path=None):
        if not self.connect():
            return
        
        for r in recipients:
            recipient_name = r['name']
            recipient_email = r['email']
            personalized_body = body.replace('{name}', recipient_name)
            msg = self.create_message(recipient_email, subject, personalized_body, files_path)
            if msg is None:
                print(f'{recipient_email}에게 보낼 메시지 생성 실패')
                return
            try:
                self.server.send_message(msg)
                print(f'{recipient_name}님, ({recipient_email})으로 메일 발송 성공')
            except Exception as e:
                print(f'{recipient_name}님, ({recipient_email})으로 메일 발송 실패: {e}')

        self.disconnect()

    # 여러 명에게 한 번에 전송
    def send_group_email(self, recipients, subject, body, files_path=None):
        if not self.connect():
            return
        all_emails = [r['email'] for r in recipients]
        msg = self.create_message(', '.join(all_emails), subject, body, files_path)
        try:
            self.server.send_message(msg)
            print(f'전체 {len(all_emails)}명에게 한 번에 메일 발송 완료')
        except Exception as e:
            print(f'전체 메일 발송 실패: {e}')
        self.disconnect()


# ---실행 클래스---
class MainApp:
    def __init__(self):
        self.config = Config()
        self.recipient_manager = RecipientManager(os.path.join(os.path.dirname(__file__), 'mail_target_list.csv'))

    def run(self):
        # 메일 서비스 선택
        for i in range(3):
            service = input('사용할 메일 서비스(gmail/naver): ').strip().lower()
            smtp_info = self.config.get_smtp_info(service)
            if smtp_info:
                break
            print(f'지원하지 않는 서비스입니다. 다시 입력하세요. ({2 - i}회 남음)')
        else:
            print('메일 서비스 선택 실패. 프로그램을 종료합니다.')
            return
        
        # 발신자 정보 설정
        if service == 'gmail':
            sender = self.config.GOOGLE_SENDER_EMAIL or input('Gmail 주소: ')
            password = self.config.GOOGLE_APP_PASSWORD or getpass.getpass('Gmail (App Password): ')
        else: # naver
            sender = self.config.NAVER_SENDER_EMAIL or input('Naver 주소: ')
            password = self.config.NAVER_APP_PASSWORD or getpass.getpass('Naver (App Password): ')
            
        subject = '파이썬으로 이메일 보내기 제목 테스트'
        body = """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color:#4CAF50;">{name}님</h2>
            <p>
                Thank you so much for your heartfelt message. 
                I was deeply touched by your words — please don’t worry too much. 
                I am safe now and slowly recovering, thanks to your thoughts and prayers.
            </p>
            <p>
                With warm regards,<br>
                <b>Dr. Han</b>
            </p>
            <a href="https://mail.google.com">Gmail 열기</a>
        </body>
        </html>
        """
        files = ['3-12/test.txt']  # 첨부파일 경로 (없으면 None)
        recipients = self.recipient_manager.load_recipients()
        if not recipients:
            print('수신자 목록이 비어 있습니다. 프로그램을 종료합니다.')
            return
        
        print(f'총 {len(recipients)}명에게 메일을 발송합니다.')
        choice = input('모두에게 한 번에 보내시겠습니까? (y/n): ').strip().lower()
        sender_instance = EmailSender(smtp_info, sender, password)
        if choice == 'y':
            sender_instance.send_group_email(recipients, subject, body, files)
        else:
            sender_instance.send_individual_emails(recipients, subject, body, files)


if __name__ == '__main__':
    MainApp().run()