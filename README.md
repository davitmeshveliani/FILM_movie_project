#  Movie Search & Analytics System


**[EN]** A professional Python CLI application that integrates relational (MySQL)
            and NoSQL (MongoDB) databases for movie searching, logging, and analytics.

**[RU]** Профессиональное Python CLI-приложение, объединяющее реляционные (MySQL) 
        и NoSQL (MongoDB) базы данных для поиска фильмов, ведения логов и аналитики.

##  Features / Возможности

-  Live MySQL Search** — Real-time queries from the Sakila database.  
  *(Поиск в реальном времени в базе данных Sakila)*

-  MongoDB Logging** — Logs all searches and system errors to MongoDB Atlas.  
   (Логирование запросов и ошибок в MongoDB Atlas)*

-- Smart Analytics — View trending searches using MongoDB aggregation.  
   (Аналитика популярных поисковых запросов)*

- **Pagination** — Clean CLI data display (10 results per page).  
  *(Удобная пагинация данных)*

---

##  Project Architecture / Архитектура проекта

| Module                | Description (EN) | Описание (RU) |

| 'main.py'             |	Core application logic              |	          Основная логика приложения
| 'app_orchestrator.py' |	Handles high-level logic and flow	|  Управление бизнес-логикой и потоками
| 'db_manager.py'	    |    Database operations (MySQL)        |	Операции с базой данных (MySQL)
 'ui_handlers.py'       |   CLI user interface logic	        |   Логика пользовательского интерфейса

| `log_stats.py`         | Analytics processing                 | Обработка аналитики |
| `formatter.py`         | CLI data styling                     | Стилизация вывода в CLI |
| `config.py`            | Environment loader                   | Загрузка конфигурации |

---
##   Installation / Установка

1. Clone the repository / Клонируйте репозиторий

git clone <your-repository-url>

cd FILM_movie_project

# 2. Setup on Windows (PowerShell) / Настройка в Windows (PowerShell)
# Create and activate virtual environment / Создайте и активируйте виртуальное окружение:

#  Windows (PowerShell):

python -m venv venv .\venv\Scripts\Activate.ps1

.\venv\Scripts\pip install -r requirements.txt

##  Run the Project / Запуск проекта

.\venv\Scripts\python main.py





# 3. Setup on Mac / Linux / Настройка в Mac / Linux
# Create and activate virtual environment / Создайте и активируйте виртуальное окружение:

##    Mac / Linux (Bash):


python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

##  Run the Project / Запуск проекта

python main.py
---
#   Testing / Тестирование

pytest -v

---
-- Example Functionality // Пример возможностей

- Search movies by title
- Store search history in MongoDB
-  Display trending searches
- Paginated CLI output
- Error logging and monitoring

--  Technologies Used / Используемые технологии

- Python 3
- MySQL
- MongoDB Atlas
- PyMongo
- mysql-connector-python

