# TodosGarpix

# Todo_back
Планировщик задач, без Frontend

# Stack
Python==3.8.5
Flask==2.0.1
flask-restx==0.4.0
peewee==3.14.4
Werkzeug==2.0.1

# Позволяет производить действия:
просматривать существующие задачи
создавать задачи
обнавлять задачи
удалять задачи

# Environment
PATH=$PATH:/ap
APP_SETTINGS=config.DevelopmentConfig
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/task

APP_SETTINGS=config.DevelopmentConfig
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/task
SECRET_KEY=secretsecretsecretsecretsecretsecretsecretsecretsecret
POSTGRES_DB=task
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DEBUG=True

# Запустить:
1. git clone https://github.com/SuvorovAV/TODO_not_front.git
2. cd TODO_not_front
3. python -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. docker-compose up -d
7. ./ap/base.py

# примеры команд:
 интерфейс Swagger или утилиту cUrl:
 
 1. Список задач         curl -H 'Content-Type: application/json' -X 'GET' 'http://127.0.0.1:5000/api/task/'
 2. Детальная задача     curl -H 'Content-Type: application/json' -X 'GET' 'http://127.0.0.1:5000/api/task/<ID>'
 3. Добавить задачу      curl -H 'Content-Type: application/json' -d '{"title":"Dinner", "content":"Having Dinner"}' -X 'POST' 'http://127.0.0.1:5000/api/task/'
 4. Удалить задачу       curl -H 'Content-Type: application/json' -X 'DELETE' 'http://127.0.0.1:5000/api/task/<ID>'
  
 # Тесты
  APP_SETTINGS=config.TestingConfig
 
  применены методы тестирования UnitTEST
  для запуска тестирования необходимо выполнить команду
  
  python -m unittest tests/api_test.py
  
  # License
  
  MIT
