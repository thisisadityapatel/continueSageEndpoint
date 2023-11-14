from langchain.chains import LLMChain
from langchain.llms import SagemakerEndpoint
from langchain.prompts import PromptTemplate
from contentHandler import ContentHandler


class SagemakerChatbot:
    def __init__(
        self, endpoint_name, region_name, prompt_template=None, content_handler=None
    ):
        self.endpoint_name = endpoint_name
        self.region_name = region_name
        self.prompt_template = prompt_template or self._default_prompt_template()
        self.content_handler = content_handler or self._default_content_handler()
        self.llm = self.initiate_llm()
        self.llm_chain = self.initiate_llm_chain()

    def initiate_llm(self):
        llm = SagemakerEndpoint(
            endpoint_name=self.endpoint_name,
            region_name=self.region_name,
            model_kwargs={"max_new_tokens": 600, "top_p": 0.9, "temperature": 0.4},
            endpoint_kwargs={"CustomAttributes": "accept_eula=true"},
            content_handler=self.content_handler,
        )
        return llm

    def initiate_llm_chain(self):
        llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        return llm_chain

    def chat(self, chat_context, question):
        output = self.llm_chain.predict(
            continuedev_chat_context=chat_context, question=question
        )
        return output.strip()

    @property
    def _default_prompt_template():
        prompt = """<s>[INST]You are an intelligent programmer bot that is specialized in answering programming questions, writing code, and also helping with documentation. Answer the questions considering the chat history with the user that is provided.[/INST]</s> \n\n Here is the past chat history with the user: {continuedev_chat_context} \n\n Here is the question that is to be answered: {question}"""
        prompt_template = PromptTemplate.from_template(prompt)
        return prompt_template

    @property
    def _default_content_handler():
        return ContentHandler()
