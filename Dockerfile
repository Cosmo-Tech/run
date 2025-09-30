FROM ghcr.io/astral-sh/uv:python3.13-trixie

RUN apt-get update && apt-get install -y

WORKDIR /app
COPY . /app

RUN uv venv .venv && \
    . .venv/bin/activate && \
    pip install .

CMD ["python3", "-m", "run.main"]