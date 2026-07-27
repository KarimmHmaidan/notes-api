FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv sync --frozen

COPY . .

EXPOSE 8000

COPY entrypoint.sh .

CMD ["./entrypoint.sh"]