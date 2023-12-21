import llmfunction

class TaskRouter(llmfunction.LlmFunction):
    def __init__(self,
        request: str,
        functions: list[llmfunction.LlmFunction],
        reasoning: bool = False
    ):
        super().__init__(
            model="mistral:latest",
            label="taskrouter",
            description="Looks at a request and decides to which function to route the request",
            stops=["###"]
        )

        self.writeLine("### SYSTEM:")
        self.writeLine("You are a Task-Router. You are responseable to reason about to which program the request should go to.")
        self.writeLine("### REQUEST:")
        self.writeLine(request)
        self.writeLine("### PROGRAMS:")
        for function in functions:
            self.writeLine(f"- {function.label} -> {function.description}")
        self.writeLine("- OTHERS -> if the message is NONESENSE or other programms are not an option")
        if reasoning:
            self.writeLine("### REASONING:")
            self.autowrite()
        self.writeLine("### CHOOSEN PROGRAM:")

class AppointmentMaker(llmfunction.LlmFunction):
    def __init__(self,
        request: str
    ):
        super().__init__(
            model="mistral:latest",
            label="Appointment-maker",
            description="Use this for making appointments",
            stops=["###"]
        )

        self.writeLine("### SYSTEM:")
        self.writeLine("This is an appointment maker assistent")
        self.writeLine("### CUSTOMER:")
        self.writeLine(request)
        self.writeLine("### appointment maker:")

class QASession(llmfunction.LlmFunction):
    def __init__(self,
            question: str,
            facts: str,
            topic: str | None = None
    ):
        super().__init__(
            model="mistral:latest",
            label="Q&A-Session",
            description="Use this for Questions",
            stops=["###"]
        )

        self.writeLine("### System:")
        self.writeLine("This is an Q&A Session")
        self.writeLine(f"### Facts{(' about '+topic) if topic != None else ''}:")
        self.writeLine(facts)
        self.writeLine("### Question:")
        self.writeLine(question)
        self.writeLine("### Answer:")
class FactsExtractor(llmfunction.LlmFunction):
    def __init__(self, text):
        super().__init__(
            model="mistral:latest",
            label="Facts-Extractor",
            description="Use this for extracting facts from a text"
        )

        self.writeLine("### System:")
        self.writeLine("This is an facts extractor, which extracts facts from a given text, and summarizes them in a list")
        self.writeLine("### Text:")
        self.writeLine(text)
        self.writeLine("### Facts:")


text = """
# Bechtle AG
With more than 85 IT system houses and IT trading companies in 14 European countries, we are close to our customers. The combination of direct sales of IT products with comprehensive system house services makes Bechtle a future-oriented IT partner for SMEs, corporations and public sector clients. Regionally on site, in Europe and worldwide through IT alliance partners on all continents.

As a service provider with strong implementation capabilities for future-proof IT architectures, traditional IT infrastructure is just as important to us as the current topics of digitalization, cloud, modern workplace, security and IT as a service. Around 40,000 hardware and software products are available via online stores, on customized e-procurement platforms and via telesales. Experts in 94 Competence Centers across the Group also deal with a wide range of IT topics requiring intensive consulting.

A comprehensive IT life cycle also means that we use professional IT remarketing to ensure the economic reuse of used IT. And when it comes to intelligent financing services, we are on hand with Bechtle Financial Services AG.
"""

factsExtractor = FactsExtractor(text=text)
facts = factsExtractor.run()
facts += "\n+++ You are an ai working for Bechtle. +++"
while True:
    request = input("your request: ")
    appointmentMaker = AppointmentMaker(request=request)
    qAndASession = QASession(question=request, facts=facts, topic="Bechtle")
    taskRouter = TaskRouter(request=request, functions=[appointmentMaker, qAndASession], reasoning=True)

    route = taskRouter.run()

    if route in appointmentMaker.label:
        print(appointmentMaker.run())
    elif route in qAndASession.label:
        print(qAndASession.run())
    else:
        print("Sorry, I can't help you with that at the moment!")
