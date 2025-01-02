### line_provider и bet_maker

Данный проект демонстрирует архитектуру взаимодействия двух микросервисов (**line_provider** и  **bet_maker** ) через RabbitMQ, а также хранение ставок в PostgreSQL.

```
docker-compose up --build
```

После чего:

* line_provider будет доступен на порту **8001**.
* bet_maker будет доступен на порту **8002**.
* RabbitMQ (с веб-интерфейсом) — на порту **15672**.
* PostgreSQL — на порту **5432**.

Далее можно отправлять тестовые запросы через **curl** или Postman, проверять логи сервисов и корректную обработку ставок.

Для прогона **интеграционных** тестов нужно выполнить:

```bash
pytest bet_maker/tests/test_bet_maker_integration.py
```

и

```bash
pytest line_provider/tests/test_line_provider_integration.py
```

при запуске интеграционных тестов докер контейнер должен быть уже развернут, иначе нужные порты на localhost будут недоступны.

при необходимости создается виртуальное окружение, где важно установать **pytest pytest-asyncio anyio** для корректной отработки тестов.


```
bsw-test-line-provider
├─ .git
├─ .gitignore
├─ README.md
├─ bet_maker
│  ├─ Dockerfile
│  ├─ __init__.py
│  ├─ db.py
│  ├─ entrypoint.sh
│  ├─ main.py
│  ├─ models.py
│  ├─ requirements.txt
│  ├─ schemas.py
│  └─ tests
│     └─ test_bet_maker_integration.py
├─ docker-compose.yml
├─ line_provider
│  ├─ Dockerfile
│  ├─ __init__.py
│  ├─ entrypoint.sh
│  ├─ main.py
│  ├─ requirements.txt
│  ├─ schemas.py
│  └─ tests
│     ├─ __init__.py
│     └─ test_line_provider_integration.py
└─ pytest.ini
```
