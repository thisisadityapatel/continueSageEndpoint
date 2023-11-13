from langchain.chains import LLMChain
from langchain.llms import SagemakerEndpoint
from langchain.prompts import PromptTemplate
from langchain.llms.sagemaker_endpoint import LLMContentHandler
from contentHandler import ContentHandler


class SagemakeChatbot:
    def __init__(self, endpoint_name, region_name, template="{context}"):
        self.endpoint_name = endpoint_name
        self.region_name = region_name
        self.template = template or self._default_prompt_template
        self.llm = self.initiate_llm()
        self.llm_chain = self.initiate_llm_chain()

    def initiate_llm(self):
        content_handler = ContentHandler()
        llm = SagemakerEndpoint(
            endpoint_name=self.endpoint_name,
            region_name=self.region_name,
            model_kwargs={"max_new_tokens": 700, "top_p": 0.9, "temperature": 0.6},
            endpoint_kwargs={"CustomAttributes": "accept_eula=true"},
            content_handler=content_handler,
        )
        return llm

    def initiate_llm_chain(self):
        prompt = PromptTemplate.from_template(self.template)
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)

    def chat(self, question):
        return self.llm_chain.run({f"{question}"})

    @property
    def _default_prompt_template():
        return "{context}"
