# I chose to make LLMHandler a class so that each class/object of the LLM will have its own memory;
import requests
class LLMHandler:
    def __init__(self, api, model, prompt: str = "You are a helpful AI assistant."):
        self.memory = [{"role": "system", "content": prompt}]
        self.api = api
        if api == "OpenAI":
            self.endpoint = "" #TODO: Implement support for different OPENAI endpoints
            return NotImplementedError #TODO: Implement OpenAI support
        self.endpoint = "http://localhost:11434/api/chat"
        self.model = model

    def request(self, prompt):
        # Add the prompt to memory
        self.memory.append({
            "role": "user",
            "content": prompt
        })

        # Send the request to the LLM
        response = requests.post(self.endpoint, json={
            "model": self.model,
            "messages": self.memory,
            "stream": False
        })

        #Add the LLM's response to memory
        self.memory.append({
            "role": "assistant",
            "content": response.json()["message"]["content"]
        })

        #return the response
        return response.json()["message"]["content"]