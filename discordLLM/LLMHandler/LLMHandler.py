# I chose to make LLMHandler a class so that each class/object of the LLM will have its own memory;
class LLMHandler:
    def __init__(self, api, model):
        # self.memory = {}
        self.api = api
        if api == "OpenAI":
            self.endpoint = "" #TODO: Implement support for different OPENAI endpoints
            return NotImplementedError #TODO: Implement OpenAI support
        self.endpoint = "localhost:11434"
        self.model = model