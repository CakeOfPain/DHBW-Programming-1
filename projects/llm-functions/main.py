import tkinter
import tkinter.font

class AiAgents(object):
    def __init__(self):
        self.before = ""
        self.stopSignal = False

        self.window = tkinter.Tk()
        self.window.title("AI-Editor")

        self.selected_model = tkinter.StringVar(value="mistral:latest")
        
        self.font = tkinter.font.Font(family="Jetbrains mono", size=10)

        self.editor = tkinter.Text(self.window, bg='#1c1c1c', fg='#ffffff')
        self.editor.tag_config('ai', foreground='#00ff00')
        self.editor.pack(side=tkinter.LEFT, anchor=tkinter.NW, expand=True, fill=tkinter.BOTH)

        
        self.menu = tkinter.Menu(self.window, tearoff=False)

        self.window.config(menu=self.menu)
        self.window.bind("<Command-+>", lambda _: self.incFont(2))
        self.window.bind("<Control-+>", lambda _: self.incFont(2))
        self.window.bind("<Command-minus>", lambda _: self.incFont(-2))
        self.window.bind("<Control-minus>", lambda _: self.incFont(-2))

    def incFont(self, n):
        self.font = tkinter.font.Font(family=self.font.cget("family"),
                      size=self.font.cget("size")+n)
        self.editor.config(font=self.font)
    
    def run(self):
        self.window.mainloop()


def main():
    agents = AiAgents()
    agents.run()

if __name__ == '__main__':
    main()