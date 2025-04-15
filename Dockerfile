FROM python:3.10

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY app /app
COPY frontend/index.html /app/static/index.html

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--root-path", "", "--reload-dir", "/app"]
