# client.py
import requests

BASE_URL = 'http://127.0.0.1:8000'

def menu():
    print('\n===== TODO CLIENT =====')
    print('1. 전체 조회')
    print('2. 추가')
    print('3. 개별 조회')
    print('4. 수정')
    print('5. 삭제')
    print('0. 종료')

def main():
    while True:
        menu()
        choice = input('선택: ')
        if choice == '1':
            r = requests.get(f'{BASE_URL}/retrieve_todo')
            print(r.json())
        elif choice == '2':
            task = input('할 일: ')
            r = requests.post(f'{BASE_URL}/add_todo', json={'task': task})
            print(r.json())
        elif choice == '3':
            todo_id = input('조회할 ID: ')
            r = requests.get(f'{BASE_URL}/retrieve_todo/{todo_id}')
            print(r.json())
        elif choice == '4':
            todo_id = input('수정할 ID: ')
            task = input('새로운 내용: ')
            r = requests.put(f'{BASE_URL}/update_todo/{todo_id}', json={'id': int(todo_id), 'task': task})
            print(r.json())
        elif choice == '5':
            todo_id = input('삭제할 ID: ')
            r = requests.delete(f'{BASE_URL}/delete_todo/{todo_id}')
            print(r.json())
        elif choice == '0':
            break
        else:
            print('잘못된 선택입니다.')

if __name__ == '__main__':
    main()
