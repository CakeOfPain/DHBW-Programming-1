import llmfunction

###############################################
# This llmfunction is made for retrieval data #
# by an knowledge graph                       #
###############################################

class FactsExtractor(llmfunction.LlmFunction):
    def __init__(self, text: str):
        super().__init__(
            model='mistral:latest',
            label=FactsExtractor.__name__,
            description='Use this for extracting facts from a text into a list',
            stops=['###']
        )
        self.writeLine('### System:')
        self.writeLine('You are an ai that is generating a list of facts from a given text.')
        self.writeLine('Provide a fact in this format: <subject> <verb> <object>')

        self.writeLine('### Text:')
        self.writeLine(text)
        self.writeLine('### List-of-Facts:')
        self.writeLine("The following list of facts do not contain the word 'it':")

def main():
    knowledgeGraphRecaller = FactsExtractor(
        text='Mermaid can render state diagrams. The syntax tries to be compliant with the syntax used in plantUml as this will make it easier for users to share diagrams between mermaid and plantUml.'
    )
    print(knowledgeGraphRecaller.prompt)
    print(knowledgeGraphRecaller.run())

if __name__ == '__main__':
    main()
