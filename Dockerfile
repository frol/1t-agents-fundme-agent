FROM python:3.9-slim-bookworm

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir nearai requests

CMD ["nearai", "run", "agent/agent.py"]