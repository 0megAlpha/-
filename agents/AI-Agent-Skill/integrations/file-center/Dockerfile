FROM python:3.12-slim
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY app /app/app
COPY config /app/config
RUN mkdir -p /app/storage
EXPOSE 8890
CMD ["uvicorn","app.server:app","--host","127.0.0.1","--port","8890"]
