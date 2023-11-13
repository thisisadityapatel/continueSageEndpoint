from langchain.chains import LLMChain
from langchain.llms import SagemakerEndpoint
from langchain.prompts import PromptTemplate
from contentHandler import ContentHandler


class SagemakeChatbot:
    def __init__(
        self, 
        endpoint_name, 
        region_name, 
        prompt_template=None, 
        content_handler=None
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
            model_kwargs={"max_new_tokens": 700, "top_p": 0.9, "temperature": 0.6},
            endpoint_kwargs={"CustomAttributes": "accept_eula=true"},
            content_handler=self.content_handler,
        )
        return llm

    def initiate_llm_chain(self):
        llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        return llm_chain

    def chat(self, question):
        output = self.llm_chain.run({f"{question}"})
        return output

    @property
    def _default_prompt_template():
        prompt = """
        <s>You are an intelligent coding assitant who's job is to help with programming problems, understanding code, documentation and explaination of software engineering concepts and frameworks. If you do not understand the question, feel free to ask questions, or simply say `Apologies, I do not understand the question`</s>

        Here is the past chat history: {continuedev_chat_history}

        Here is the current question: {question}
        """
        prompt_template = PromptTemplate.from_template(prompt)
        return prompt_template

    @property
    def _default_content_handler():
        return ContentHandler()
