# Django_Challenge
가상환경 생성: python -m venv venv

가상환경 활성화: source venv/bin/activate (우분투 기준)

필수 패키지 설치: pip install -r requirements.txt

DB 초기화: python manage.py migrate

app디렉토리 안에 .env파일 만들어서
SECRET_KEY=your_secret_key_here
위 코드 추가해야함 -> settings.py에서 SECRET_KEY를 참조해서 아무값이나 넣긴해아함

코드 스타일 통일 : black project