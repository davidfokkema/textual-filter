from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from typing_extensions import Self

from textual.widgets import OptionList
from textual.widgets._option_list import NewOptionListContent
from textual.widgets.option_list import Option


class FilteredOptionList(OptionList):
    def __init__(self, *content: NewOptionListContent, **kwargs) -> None:
        super().__init__(*content, **kwargs)
        self._all_options: list[Option] = [
            c if isinstance(c, Option) else Option(c) for c in content
        ]
        print(f"{self._all_options=}")

    def add_options(self, items: Iterable[NewOptionListContent]) -> Self:
        self._all_options.extend(
            [c if isinstance(c, Option) else Option(c) for c in items]
        )
        return super().add_options(items)

    def filter(self, query: str) -> None:
        if query:
            self.clear_options().add_options(self._all_options[:5])
        else:
            self.clear_options().add_options(self._all_options)
        self.refresh()
