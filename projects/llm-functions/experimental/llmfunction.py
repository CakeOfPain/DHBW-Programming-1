
class LlmFunction(object):
    def __init__(self, label: str, description: str, stops: list[str] = [], temperature = 0.0, seed = 0):
        self.prompt = ""
        self.temperature = temperature
        self.seed  = seed
        self.description = description
        self.label = label
        self.stops = stops
    def write(self, message) -> None:
        self.prompt += message
    def writeLine(self, message) -> None:
        self.prompt += message + "\n"
    def run(self):
        pass

class EmailWriter(LlmFunction):
    def __init__(self, subject: str, sender: str, receiver: str):
        super().__init__(
            "EmailWriter",
            "Writes an email from an given subject, sender and receiver"
        )
