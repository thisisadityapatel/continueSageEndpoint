## Continue.dev Sagemaker Endpoint

This backend FastAPI server helps connected LLMs (in my case mistral-instruct-7b and falcon 40b) hosted on AWS Sagameker Cloud Platform to Continue.dev frontend service on local VSCode environment. It mocks a Ollama service connection to continue.dev GUI and streams the LLM response using a SSE (Server Side Events) streaming network connection.

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
