from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from typing_extensions import Self

from rapidfuzz.process import extract
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

    def filter(
        self, query: str, limit=None, score_cutoff=60.0, show_score=False
    ) -> None:
        if query:
            prompts = [option.prompt for option in self._all_options]
            matches = extract(
                query, choices=prompts, limit=limit, score_cutoff=score_cutoff
            )
            if show_score:
                filtered_options = [
                    f"{self._all_options[match[2]].prompt} [red italic]({match[1]:.1f})[/]"
                    for match in matches
                ]
            else:
                filtered_options = [
                    self._all_options[match[2]].prompt for match in matches
                ]

            self.clear_options()

            super().add_options(filtered_options)
        else:
            self.clear_options()
            super().add_options(self._all_options)
        self.refresh()
