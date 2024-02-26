# Messenger_TestTask

## 1. Создание виртуального окружения и установка зависимостей
Для корректной работы рекомендуется использовать интерпретатор версии 3.11 и выше (также можно 3.10)
### Перейдите в директорию, где находится проект
Создание локального окружения:
```
python -m venv venv
```
Активация локального окружения:
```
source venv/bin/activate
```
Установка poetry в локальное окружение:
```
pip install poetry
```
Установка зависимостей проекта:
```
poetry install
```
## 2. Подключение базы данных(PostgreSQL)
База данных разворачивается как локально, так и с помошью docker контейнера

### Локально
В корне проекта нужно создать **.env** файл, где нужно изменить значения **DB_USER**, **DB_PASS** под свои

Пример:
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=messages_test
```
Затем нужно создать базу данных **messages_test**, к примеру, используя pgAdmin или терминал

### Используя docker-compose файл
В docker-compose файле разворачиваются контейнеры: postgres и pgadmin

В корне проекта нужно создать **.env** файл, никакие значения менять не нужно
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=messages_test
```

Команда для запуска контейнеров, определенных в файле docker-compose.yml, в фоновом режиме. 
```
docker compose up -d
```
PgAdmin будет доступен по порту 5050, URL http://localhost:5050

## 3. Запуск приложения
### Для запуска сервера в директории проекта, нужно запустить две команды в разных терминалах

**В первом терминале**
```
uvicorn server.main:app --port 8000
```
**Во втором терминале**
```
uvicorn server.main:app --port 8001
```
### Для запуска клиента нужно ввести команду
```
python client/test_client.py 
```
Затем ждем выполнение скрипта

В ходе выполнения будет выводиться результат выполнения запросов, в конце выведется информация о времени выполнения

Если был запуск docker-compose файла, можно остановить и удалить контейнеры
```
docker compose down
```
