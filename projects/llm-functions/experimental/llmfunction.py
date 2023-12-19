import requests
import random
import json

ollama_url = lambda path: "http://127.0.0.1:11434" + path

class LlmFunction(object):
    def __init__(self, model: str, label: str, description: str, stops: list[str] = [], temperature = 0.0, seed = random.randint(0, 2**63)):
        self.model = model
        self.prompt = ""
        self.temperature = temperature
        self.seed  = seed
        self.description = description
        self.label = label
        self.stops = stops
        self.result = ""

    def write(self, message) -> None:
        self.prompt += message
    def writeLine(self, message) -> None:
        self.prompt += message + "\n"
    def run(self):
        data = json.dumps({
            "model": self.model,
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

class EmailWriter(LlmFunction):
    def __init__(self, subject: str, sender: str, receiver: str, context: str = None):
        super().__init__(
            model="mistral:latest",
            label="EmailWriter",
            description="Writes an email from an given subject, sender and receiver",
            stops=["###"]
        )

        if context != None:
            self.writeLine("### context:")
            self.writeLine(context)
        self.writeLine("### subject:")
        self.writeLine(subject)
        self.writeLine("### sender:")
        self.writeLine(sender)
        self.writeLine("### receiver:")
        self.writeLine(receiver)
        self.writeLine("### content:")
