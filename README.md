# Run a solution

This project provides a minimal Python script for running Cosmotech Brewery simulations in CI/CD pipelines.


## Required Environment Variables

```bash
COSMOTECH_API_URL=https://api.cosmotech.com
COSMOTECH_CLIENT_ID=your_client_id
COSMOTECH_CLIENT_SECRET=your_client_secret
ORGANIZATION_ID=your_org_id  # Optional, can create new org
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

## Exit Codes

- 0: Success
- 1: Authentication error
- 2: Template loading error
- 3: Simulation creation error
- 4: Simulation execution error
- 5: Configuration error