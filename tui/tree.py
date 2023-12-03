"""
Code browser example.

Run with:

    python code_browser.py PATH
"""
import json
from rich.syntax import Syntax
from rich.traceback import Traceback

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import var
from textual.widgets import DirectoryTree, Footer, Header, Static, Placeholder

from configs import CONFIG_PATH


class CodeBrowser(App):
    """Textual code browser app."""

    CSS_PATH = "tree.tcss"
    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
        ("q", "quit", "Quit"),
        # ("e", "edit_file", "Edit File"),
        # ("d", "delete_file", "Delete File"),
        ("c", "connect_ssh", "Connect via SSH"),
        ("s", "sftp", "Connect via SFTP"),
        # ("r", "refresh", "Refresh"),
        # ("a", "add_server", "Add Server"),
        # ("g", "make_group", "Make Group"),
        # ("h", "help", "Help"),
    ]

    show_tree = var(True)

    def __init__(self, path: str = CONFIG_PATH, **kwargs) -> None:
        super().__init__(**kwargs)
        self.path = path

    def watch_show_tree(self, show_tree: bool) -> None:
        """Called when show_tree is modified."""
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        yield Header()
        with Container():
            yield DirectoryTree(self.path, id="tree-view")
            with VerticalScroll(id="code-view"):
                yield Static(id="code", expand=True)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(DirectoryTree).focus()

    def on_directory_tree_file_selected(
            self, event: DirectoryTree.FileSelected
    ) -> None:
        """Called when the user click a file in the directory tree."""
        event.stop()
        self.selected_file_path = event.path  # The path of the selected file

        code_view = self.query_one("#code", Static)
        try:
            syntax = Syntax.from_path(
                str(event.path),
                line_numbers=True,
                word_wrap=False,
                indent_guides=True,
                theme="github-dark",
            )
        except Exception:
            code_view.update(Traceback(theme="github-dark", width=None))
            self.sub_title = "ERROR"
        else:
            code_view.update(syntax)
            self.query_one("#code-view").scroll_home(animate=False)
            self.sub_title = str(event.path)

    def action_toggle_files(self) -> None:
        """Called in response to key binding."""
        self.show_tree = not self.show_tree


    def action_connect_ssh(self) -> None:
        """Called in response to 'c' key binding."""
        # Path to the JSON file
        self.selected_file_path

        # Read the JSON file
        with open(self.selected_file_path, "r") as json_file:
            data = json.load(json_file)
            command = f"ssh {data['user']}@{data['host']} -p {data['port']}"
        self.command = command


        # Stop the CodeBrowser app
        self.exit()

        # Print the key-value pair


def main():
    test_path = "/home/matt/.config/test_sshaman"
    app = CodeBrowser(path=test_path)
    app.run()
    dynamic_data = getattr(app, 'command', None)
    if getattr(app, 'command', False):
        print(dynamic_data)


