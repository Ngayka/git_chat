## 👉 Project: `social_api`

A RESTful social media API built with Django REST Framework, PostgreSQL, Celery, and Docker.

---

## 🚀 Getting Started

### 📦 Requirements

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
* (Optional) Make sure port `8000`, `5432`, and `6379` are free

---

## ⚙️ Project Structure

```
social_api/
│
├── social_api/              # Django project settings
├── chat/                     # Main Django app
├── Dockerfile               # Docker config for Django
├── docker-compose.yml       # Services: Django, Postgres, Redis, Celery
├── requirements.txt
└── .env                     # Environment variables
```

---

## ⚒️ Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/social_api.git
cd social_api
```

### 2. Create `.env` file

Use `.env.sample` as a template to create your own `.env` file in the root directory:

```bash
cp .env.sample .env
```

Then edit the `.env` file as needed: a `.env` file in the root directory:

```
DEBUG=1
SECRET_KEY=your-secret-key
POSTGRES_DB=socialdb
POSTGRES_USER=socialuser
POSTGRES_PASSWORD=socialpass
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
```

> Replace values as needed.

---

### Running Tests

To run tests successfully, please use the SQLite database instead of PostgreSQL.
By default, the project is configured to use PostgreSQL for development, but tests require SQLite for simplicity.

Steps:

Comment out or disable the PostgreSQL database settings in your settings.py (or equivalent config).

Uncomment or enable the SQLite3 database settings.

This switch allows the test suite to run quickly and without external dependencies.

### 3. Build and run the project

```bash
docker-compose up --build
```

This command will:

* Build the Django app image
* Start services:

  * Django app (on port 8000)
  * PostgreSQL
  * Redis (for Celery)
  * Celery worker
  * Celery Beat scheduler

---

### 4. Apply migrations and create superuser (in another terminal)

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 📬 API Endpoints

Once the server is running:

* API root: [http://localhost:8000/api/](http://localhost:8000/api/)
* Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🔄 Celery Tasks

Celery is used for asynchronous tasks (e.g., sending notifications, scheduled posts, etc.)

* Worker runs in `celery` service
* Periodic tasks are managed by `celery-beat` service

Logs:

```bash
docker-compose logs -f celery
docker-compose logs -f celery-beat
```

---

## 📂 Media and Static Files

* Static files are served from `/vol/web/static/`
* Uploaded media is stored in `/vol/web/media/`

Mounted using Docker volumes.

---

## ✅ Useful Commands

```bash
# Run tests
docker-compose exec web python manage.py test

# Access Django shell
docker-compose exec web python manage.py shell
```

---

## 🛉 Clean up

To stop all services:

```bash
docker-compose down
```

To remove volumes as well (PostgreSQL data, etc.):

```bash
docker-compose down -v
```

---

## 📌 Notes

* Uses PostgreSQL instead of SQLite
* Uses Redis as the Celery broker
* All services are fully containerized
* For production, you can configure Gunicorn + Nginx and disable `DEBUG`
