# I chose to make LLMHandler a class so that each class/object of the LLM will have its own memory;
from openai import OpenAI
import ollama


class LLMHandler:
    def __init__(
        self,
        api: str,
        base_url: str,
        key: str,
        model: str,
        prompt: str = "You are a helpful AI assistant.",
    ):
        # API can be `OpenAI-like` or `Ollama`. Run .lower() to be safe
        self.memory = [{"role": "system", "content": prompt}]
        self.api = api.lower()
        self.model = model

        match self.api:
            case "openai-like":
                self.client = OpenAI(base_url=base_url, api_key=key)
            case "ollama":
                self.client = ollama.Client(host=base_url)
                # Pull the model if needed
                for model in self.client.list()["models"]:
                    if model["name"] == self.model:
                        break
                else:
                    self.client.pull(model=self.model)
            # If the API is not recognized, raise an error
            case _:
                raise ValueError("API not recognized")

    def request(self, prompt):
        # Add the prompt to memory
        self.memory.append({"role": "user", "content": prompt})

        # Depending on the API, use the respective library
        if self.api == "openai-like":
            completion = (
                self.client.chat.completions.create(
                    model=self.model,
                    messages=self.memory,
                )
                .choices[0]
                .message.content
            )
        elif self.api == "ollama":
            completion = self.client.chat(
                model=self.model,
                messages=self.memory,
            )["message"]["content"]

        # Add the LLM's response to memory
        self.memory.append({"role": "assistant", "content": completion})

        # return the response
        return completion
