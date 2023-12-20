import llmfunction

class EmailWriter(llmfunction.LlmFunction):
    def __init__(self,
            subject: str,
            sender: str,
            receiver: str,
            context: str | None = None
    ):
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
