from textual.widgets import TextArea, Footer
from textual.containers import Container
from textual.binding import Binding
from textual.app import App, ComposeResult

class TextEditor(App):
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="texteditor"):
            yield TextArea()
            yield Footer()

if __name__ == '__main__':
    app = TextEditor()
    app.run()