import requests
import random
import json

ollama_url = lambda path: "http://127.0.0.1:11434" + path

class LlmFunction(object):
    def __init__(self,
            model: str,
            label: str,
            description: str,
            stops: list[str] = [],
            temperature = 0.0,
            seed = random.randint(0, 2^64-1)
    ):
        self.model = model
        self.prompt = ""
        self.temperature = temperature
        self.seed  = seed
        self.description = description
        self.label = label
        self.stops = stops

    def write(self, message: str) -> None:
        """ The write method allows you to append text to the prompt """
        self.prompt += message
    def writeLine(self, message: str) -> None:
        """ The writeLine method allows you to append text to the prompt + auto appends a new line"""
        self.prompt += message + "\n"
    def autowrite(self):
        """ The autowrite method allows you to continue the prompt by the ai, without running the llm """
        self.writeLine(self.run())
    def run(self) -> str:
        """ The run method will resolve the function and creates the answer to the generated prompt of the llmfunc """
        data = json.dumps({
            "model": self.model,
            "prompt": " ",
            "template": self.prompt,
            "stream": False,
            "options": {
                "stop": self.stops,
                "temperature": self.temperature,
                "seed": self.seed,
            }
        })
        response = requests.post(ollama_url("/api/generate"), data=data)
        return response.json()['response']
