# I chose to make LLMHandler a class so that each class/object of the LLM will have its own memory;
import requests
class LLMHandler:
    def __init__(self, api, model):
        # self.memory = {}
        self.api = api
        if api == "OpenAI":
            self.endpoint = "" #TODO: Implement support for different OPENAI endpoints
            return NotImplementedError #TODO: Implement OpenAI support
        self.endpoint = "http://localhost:11434/api/generate"
        self.model = model

    def request(self, prompt):
        # Send the prompt to the LLM
        response = requests.post(self.endpoint, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]