import uvicorn
import certifi, ssl

if __name__ == "main__":
    sslcontext = ssl.create_default_context(cafile=certifi.where())
    uvicorn.run('main:app', port=11434)