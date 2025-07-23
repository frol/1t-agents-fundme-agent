FROM python:3.11-slim-bookworm

WORKDIR /app

COPY agent/ ./agent/

RUN pip install requests nearai

CMD ["python", "-u", "agent/agent.py"]