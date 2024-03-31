## Continue.dev Sagemaker Endpoint

Backend server that helps connected LLMs (in my case Mistral-Instruct-7B and Falcon-40B) hosted on AWS Sagameker Cloud Platform to Continue.dev frontend service on local VSCode environment. It mocks a Ollama service connection to continue.dev GUI and streams the LLM response using a SSE (Server Side Events) network streaming.

Scalable to architect personalised RAG infrastructure by leveraging LangChain potential for on-prem enterpise Continue.dev services. (Under development in a different project)

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
