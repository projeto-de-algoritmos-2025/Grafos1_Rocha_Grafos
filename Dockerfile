FROM python:3.10

# Instalar dependências
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app /app
COPY frontend/index.html /app/static/index.html

# Instalar Uvicorn com autoreload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--root-path", "", "--reload-dir", "/app"]
