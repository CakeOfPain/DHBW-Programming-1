import llmfunction

###############################################
# This llmfunction is made for retrieval data #
# by an knowledge graph                       #
###############################################

class KnowledgeGraphRecaller(llmfunction.LlmFunction):
    def __init__(self, text: str):
        super().__init__(
            model='mistral:latest',
            label=KnowledgeGraphRecaller.__name__,
            description='Use this for retrieving data based on a knowledge graph provided',
            stops=['###']
        )
        self.writeLine('### System:')
        self.writeLine('You are an ai that is generating a knowledge from a given text')

        self.writeLine('### Text:')
        self.writeLine(text)
        self.writeLine('### Knowledge-Graph:')

def main():
    knowledgeGraphRecaller = KnowledgeGraphRecaller(
        text='The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.[4] It is characterised by its bold black-and-white coat and rotund body. The name "giant panda" is sometimes used to distinguish it from the red panda, a neighboring musteloid. Though it belongs to the order Carnivora, the giant panda is a folivore, with bamboo shoots and leaves making up more than 99% of its diet.'
    )
    print(knowledgeGraphRecaller.prompt)
    print(knowledgeGraphRecaller.run())

if __name__ == '__main__':
    main()
