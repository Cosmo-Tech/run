# Run a solution

This project provides a minimal Python script for running Cosmotech Brewery simulations in CI/CD pipelines.

## Project Structure

```
run/
├── run/
│   ├── __init__.py
│   ├── config.py          # Environment and configuration handling
│   ├── auth.py           # Authentication with Cosmotech platform
│   ├── templates.py      # YAML template loading and validation
│   └── simulation.py     # Core simulation logic
├── templates/            # YAML template files
├── logs/                 # Log output directory
├── tests/               
│   └── test_simulation.py
├── .env.example         # Example environment variables
├── README.md           
└── main.py             # Entry point
```


## Key Features

1. **Logging System**
   - Log to both file and stdout for CI/CD visibility
   - Different log levels for debugging and production
   - Structured logging format with timestamps

2. **Error Handling**
   - Custom exceptions for different failure scenarios
   - Appropriate exit codes for CI/CD pipeline
   - Detailed error messages in logs

3. **Configuration**
   - Environment variables for sensitive data
   - YAML template loading with validation
   - Fallback to default parameters

4. **Authentication**
   - Secure handling of credentials
   - Token management
   - Automatic retry on token expiration

5. **Simulation Management**
   - Progress monitoring
   - Status checking
   - Timeout handling

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
python3 run/main.py
```

## Exit Codes

- 0: Success
- 1: Authentication error
- 2: Template loading error
- 3: Simulation creation error
- 4: Simulation execution error
- 5: Configuration error