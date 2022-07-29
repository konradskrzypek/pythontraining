FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app
ENV PYTHONPATH=/app
