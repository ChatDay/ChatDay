# ChatDay
# Project : ChatDay
매일 업데이트 되는 주제로 소통할 수 있는 채팅 커뮤니티 사이트

## Project Introduction
- ChatDay는, 채팅을 중점으로 만들어진 사이트입니다.
- 매일 새로운 주제를 제공합니다, 이 주제는 매 자정마다 업데이트 됩니다.
- 유저들은 매번 바뀌는 주제를 가지고 소통하게 됩니다.

## Development time
2024.10 ~ 2024.11 (1개월)

## Development Environment
- Programming Language : Python 3.10
- Framework : DJANGO, DRF
- Database : PostgreSQL, Redis
- Deployment : AWS, EC2, Docker-compose, Nginx, Ubuntu
- Backend : WebSocket, DRF, Celery
- FrontEnd : vue.js
- Version Control : Git, GitHub, 
- Communication Tool : Notion, Figma, Zep


## Deployment
hsjoo.site

## Installation
1. 깃허브 클론
```
https://github.com/ChatDay/ChatDay.git
```
2. docker 실행
```
docker-compose build
docker-compose up
```
3. Django migration 진행
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```


## API Documentation
<img width="1156" alt="스크린샷 2025-01-07 오후 12 13 49" src="https://github.com/user-attachments/assets/c59f6b22-db96-493c-8a69-62e974f4870f" />

## Apps Description
### 1. accounts
- JWT을 이용한 로그인 및 로그아웃, 회원가입
### 2. chat
- Django channels를 이용한 실시간 채팅 기능
- Celery를 이용해 매일 새로운 주제 업데이트

## ERD
<img width="702" alt="스크린샷 2025-01-07 오후 1 02 33" src="https://github.com/user-attachments/assets/9a194e0a-e626-4190-aa43-c337d79e0082" />
