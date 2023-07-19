FROM python:3.10-slim

WORKDIR unit-test-service

COPY ./requirements.txt .

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY server .

WORKDIR ../

CMD ["uvicorn", "unit-test-service.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
