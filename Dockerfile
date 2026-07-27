FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN uv sync --frozen

COPY . .

EXPOSE 8000

COPY entrypoint.sh .

CMD ["./entrypoint.sh"]