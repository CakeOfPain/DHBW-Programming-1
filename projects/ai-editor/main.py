import tkinter
import tkinter.font
import requests
import json
import threading

OLLAMA_URL = "http://127.0.0.1:11434"

class AiEditor(object):
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("AI-Editor")
        
        self.font = tkinter.font.Font(family="Arial", size=10)

        self.editor = tkinter.Text(self.window, bg='#1c1c1c', fg='#ffffff')
        self.editor.tag_config('ai', background='#092b00')
        self.editor.pack(side=tkinter.LEFT, anchor=tkinter.NW, expand=True, fill=tkinter.BOTH)

        
        self.menu = tkinter.Menu(self.window, tearoff=False)
        
        self.ai_menu = tkinter.Menu(self.menu)
        self.ai_menu.add_command(label="generate", command=self.aiGenerate)

        self.menu.add_cascade(label="ai", menu=self.ai_menu)

        self.window.config(menu=self.menu)
        self.window.bind("<Command-g>", lambda _: self.aiGenerate())
        self.window.bind("<Control-g>", lambda _: self.aiGenerate())
        self.window.bind("<Command-+>", lambda _: self.incFont(2))
        self.window.bind("<Command-minus>", lambda _: self.incFont(-2))

    def incFont(self, n):
        self.font = tkinter.font.Font(family=self.font.cget("family"),
                      size=self.font.cget("size")+n)
        self.editor.config(font=self.font)

    def aiGenerate(self):
        # Coming soon

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    aiEditor = AiEditor()
    aiEditor.run()
