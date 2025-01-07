## Continue.dev Sagemaker Endpoint

Backend LLM inference server (in my case Mistral-Instruct-7B and Falcon-40B) hosted with AWS Sagameker Cloud Platform to Continue.dev VSCode extension. It mocks a Ollama service connection to Continue.dev GUI and streams the LLM response using a SSE (Server Side Events) network streaming.

Scalable to architect personalised RAG infrastructure by leveraging LangChain potential for on-prem enterpise Continue.dev services.

## ContinueDev Demo

The folowing continudev server is running on MISTRAL-7B model on AWS

<div align="center">
  <video src="https://github.com/thisisadityapatel/continueSageEndpoint/assets/79132756/a43126ae-706b-403d-8048-0d4b4eee61a8"></video>
</div>

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
