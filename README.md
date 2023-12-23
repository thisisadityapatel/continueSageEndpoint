## Continue.dev Sagemaker Endpoint

### Starting the server locally

Cloning the repository
```bash
git clone https://github.com/thisisadityapatel/continuedevSagemakerEndpoint.git
cd continuedevSagemakerEndpoint
```

Setting up the virtual environment
```bash
python3 -m venv env
source env/bin/activate
```

Loading the environment variables
```bash
source .env
```

Initiating the service on port 11434 (local Ollama port)
```bash
python3 server.py
```