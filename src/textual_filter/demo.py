from faker import Faker
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
        fake = Faker()
        Faker.seed(14)
        self.query_one(FilteredOptionList).add_options(
            [fake.sentence() for _ in range(10_000)]
        )

    @on(Input.Changed)
    def filter_options(self, event: Input.Changed) -> None:
        self.query_one(FilteredOptionList).filter(event.value, show_score=True)

    @on(FilteredOptionList.OptionSelected)
    def show_option(self, event: FilteredOptionList.OptionSelected) -> None:
        self.query_one(Label).update(event.option.prompt)


app = DemoApp
if __name__ == "__main__":
    app().run()
