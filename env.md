python --version
docker --version

python 3.11.7

python -m venv .venv
py -3.11 -m venv .venv

.\.venv\Scripts\Activate.ps1


pip freeze > requirements.txt

uvicorn main:app --reload --port 8010

copy .env.example .env


http://localhost:8010/health

Swagger:
http://localhost:8010/docs