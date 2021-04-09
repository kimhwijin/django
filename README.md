#개발용 서버 실행:
- anaconda venv_mysite 프롬프트 관리자 모드 실행
- manage.py 가 있는 곳에서
- python manage.py runserver
운용 서버 실행:
- anaconda venv_mysite 프롬프트 관리자 모드 실행
- runserver.py 가 있는 곳에서
- python runserver.py
- 명령프롬프트 관리자모드 실행
- c:\nginx폴더
- nginx.exe 실행
- 운용 서버 실행시 7일 + 8시간 타이머 작동

#MYSQL :
id : root
password : 1234
db : django_db

#DB 조회 방법 :
- mysql commend line 실행
- 비밀번호 입력
- use django_db
- show tables;
- 1. 



Anaconda3 32bit 환경 설치
------------
 - https://www.anaconda.com/products/individual 아나콘다 설치
 -    anaconda3 prompt 
 -    를 열고
 -    set CONDA_FORCE_32BIT=1'''
 -    conda create -n venv_name python=3.7 anaconda
 -    activate venv_name
 -    conda info 으로 가상환경 설정을 확인한다.

Django, MySQL 개발환경 구축
--------------------
- pip install -r requirements.txt
- mysqlclient 에러가 나올경우 
  * https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python 에서 파이썬 환경에맞는 win32.whl파일을 받은후
  * pip install 파일경로\파일명
  * pip install -r requirements.txt

Django 서버 실행
-------------------
- 프로젝트파일의 settings.py DATABASES를 환경에맞게 설정
- mysql command line 실행후, 위에서 작성한 DB를 생성 : > CREATE DATABASE db_name character set utf8mb4 collate utf8mb4_general_ci; show databases; 로 생성 확인
- anaconda prompt/ manage.py 가 있는 폴더에서 > python manage.py makemigrations , python manage.py migrate 실행
- mysql command line/ use DB_NAME; show tables; 으로 django_migrations 테이블 확인.
- anaconda prompt/ python manage.py runserver
