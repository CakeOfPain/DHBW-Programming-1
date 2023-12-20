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
        self.writeLine("- OTHERS-> if the message is NONESENSE or other programms are not an option")
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

request = input("your request: ")
appointmentMaker = AppointmentMaker(request=request)
taskRouter = TaskRouter(request=request, functions=[appointmentMaker], reasoning=False)

route = taskRouter.run()
print(taskRouter.prompt)

if route in appointmentMaker.label:
    appointment = appointmentMaker.run()
    print(appointment)
else:
    print("Sorry, I can't help you with that at the moment!")
