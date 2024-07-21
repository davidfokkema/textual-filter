from pathlib import Path

from rapidfuzz import fuzz
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, Label

from textual_filter.filtered_option_list import FilteredOptionList


class DemoApp(App[None]):
    CSS_PATH = "demo.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Type here to filter results...")
        yield FilteredOptionList()
        yield Label()

    def on_mount(self) -> None:
        files = []
        for dirpath, dirnames, filenames in Path().walk():
            dirnames[:] = [name for name in dirnames if not name.startswith(".")]
            files.extend([str(dirpath / name) for name in filenames])
        self.query_one(FilteredOptionList).add_options(files)

    @on(Input.Changed)
    def filter_options(self, event: Input.Changed) -> None:
        self.query_one(FilteredOptionList).filter(
            event.value,
            show_score=True,
            processor=lambda x: x.upper()
            .replace("-", " ")
            .replace("_", " ")
            .replace("/", " "),
            scorer=fuzz.WRatio,
        )

    @on(FilteredOptionList.OptionSelected)
    def show_option(self, event: FilteredOptionList.OptionSelected) -> None:
        self.query_one(Label).update(event.option.prompt)


app = DemoApp
if __name__ == "__main__":
    app().run()
