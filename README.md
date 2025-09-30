# Run a solution

This project provides a minimal Python script for running Cosmotech Brewery simulations in CI/CD pipelines.


## Required Environment Variables

```bash
COSMOTECH_API_URL=https://cluster/tenant/version
SERVER_URL=https://cluster/keycloak/
REALM_NAME=code_name
COSMOTECH_CLIENT_ID=automation-client
COSMOTECH_CLIENT_SECRET=your_client_secret
LOG_LEVEL=INFO  # Optional, defaults to INFO
```

## Installation

1. Install the uv package manager:
```bash
pip install uv
```

2. Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

3. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

4. Install dependencies:
```bash
# For production use
uv pip install .

# For development (includes testing dependencies)
uv pip install -e .
```

6. Activate VPN and run the simulation:
```bash
python3 -m run.main
```

Alternatively run with docker:
```bash
docker build -t cosmotech-run .
docker run --env-file .env cosmotech-run
```