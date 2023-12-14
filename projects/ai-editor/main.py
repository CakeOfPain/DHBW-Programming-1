import tkinter
import tkinter.font
import requests
import json
import threading



OLLAMA_URL = "http://127.0.0.1:11434"

class AiEditor(object):
    def __init__(self):

        self.models = []
        self.loadModels()
        self.selected_model = "mistral"

        self.before = ""
        self.stopSignal = False

        self.window = tkinter.Tk()
        self.window.title("AI-Editor")
        
        self.font = tkinter.font.Font(family="Jetbrains mono", size=10)

        self.editor = tkinter.Text(self.window, bg='#1c1c1c', fg='#ffffff')
        self.editor.tag_config('ai', foreground='#00ff00')
        self.editor.pack(side=tkinter.LEFT, anchor=tkinter.NW, expand=True, fill=tkinter.BOTH)

        
        self.menu = tkinter.Menu(self.window, tearoff=False)
        
        self.ai_menu = tkinter.Menu(self.menu)
        self.ai_menu.add_command(label="generate", command=self.aiGenerate)
        self.ai_menu.add_command(label="stop generation", command=self.stopGenerating)
        self.ai_menu.add_command(label="regenerate", command=self.regenerate)
        self.ai_menu.add_separator()

        self.models_menu = tkinter.Menu(self.ai_menu)
        for model in self.models:
            def setModel():
                self.selected_model = model
            self.models_menu.add_radiobutton(label=model, command=setModel)

        self.ai_menu.add_cascade(label="models", menu=self.models_menu)

        self.menu.add_cascade(label="ai", menu=self.ai_menu)

        self.window.config(menu=self.menu)
        self.window.bind("<Command-r>", lambda _: self.regenerate())
        self.window.bind("<Control-r>", lambda _: self.regenerate())
        self.window.bind("<Command-g>", lambda _: self.aiGenerate())
        self.window.bind("<Control-g>", lambda _: self.aiGenerate())
        self.window.bind("<Command-+>", lambda _: self.incFont(2))
        self.window.bind("<Control-+>", lambda _: self.incFont(2))
        self.window.bind("<Command-minus>", lambda _: self.incFont(-2))
        self.window.bind("<Control-minus>", lambda _: self.incFont(-2))
        self.window.bind("<Command-x>", lambda _: self.stopGenerating())
        self.window.bind("<Control-x>", lambda _: self.stopGenerating())
        
    def loadModels(self):
        url = OLLAMA_URL + "/api/tags"
        response = requests.get(url)
        self.models = list(map(lambda x: x['name'], response.json()['models']))
        print(self.models)

    def incFont(self, n):
        self.font = tkinter.font.Font(family=self.font.cget("family"),
                      size=self.font.cget("size")+n)
        self.editor.config(font=self.font)

    def regenerate(self):
        self.stopGenerating()
        self.editor.delete('1.0', tkinter.END)
        self.editor.insert(tkinter.END, self.before)
        self.aiGenerate()

    def stopGenerating(self):
        self.stopSignal = True

    def aiGenerate(self):
        self.stopSignal = False
        def generate():
            url = OLLAMA_URL + "/api/generate"
            template = self.editor.get("1.0",tkinter.END)
            print(template)
            self.before = template
            data = json.dumps({
                "model": self.selected_model,
                "template": template,
                "stream": True
            })
            with requests.post(url=url, data=data, stream=True) as resp:
                for line in resp.iter_lines():
                    if self.stopSignal: break
                    if line:
                        token = json.loads(line)["response"]
                        self.editor.insert(tkinter.END, token, 'ai')
        threading.Thread(target=generate).start()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    aiEditor = AiEditor()
    aiEditor.run()
