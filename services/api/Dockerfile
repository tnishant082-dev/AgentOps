FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY services/api/app /app/app
COPY data/sample_kb /app/data/sample_kb

ENV AGENTOPS_KB_PATH=/app/data/sample_kb
ENV AGENTOPS_HOST=0.0.0.0
ENV AGENTOPS_PORT=8080

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
