FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY configs /app/configs
COPY docs /app/docs

ENV PYTHONPATH=/app/src

RUN python -m pip install --upgrade pip && pip install .

CMD ["python", "-m", "agi_platform.main", "demo"]