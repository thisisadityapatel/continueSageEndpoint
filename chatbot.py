from langchain import LLMChain
from langchain.llms import SagemakerEndpoint
from langchain.prompts import PromptTemplate
from langchain.llms.sagemaker_endpoint import LLMContentHandler
import os
import json
from contentHandler import ContentHandler

# setting up the environment variables
region = os.environ["AWS_REGION"]
endpoint_name = os.environ["MISTRAL_7B_INSTRUCT_ENDPOINT"]

template = "{content}"

prompt = PromptTemplate.from_template(template)

def initiate_llm():
    content_handler = ContentHandler()
    llm=SagemakerEndpoint(
        endpoint_name=endpoint_name, 
        region_name=region, 
        model_kwargs={"max_new_tokens": 700, "top_p": 0.9, "temperature": 0.6},
        endpoint_kwargs={"CustomAttributes": 'accept_eula=true'},
        content_handler=content_handler
    )
    return llm

def initiate_llm_chain(prompt):
    llm_chain = LLMChain(
        llm=initiate_llm(),
        prompt=prompt
    )

def run_llm_chain(llm_chain, question):
    llm_chain.run({f"{question}"})