from __future__ import annotations

import re
from functools import reduce
from typing import TYPE_CHECKING

from slopfactory.processing.ollama import get_ollama_response
from slopfactory.schema import Resume
from slopfactory.utils.io import _load_pdf, _save_model
from slopfactory.utils.logger import logger

if TYPE_CHECKING:
    from re import Pattern
    from typing import Callable

    from pypdf import PageObject

    from slopfactory.schema import BaseModel


regex_filter_patterns: dict[str, Pattern] = {
    "empty": re.compile(r"^$"),
    "page_count": re.compile(
        r"".join(
            [
                r"([Pp]age)",  # Optional Page
                r"\s*\d+\s*",  # Number
                r"(([Oo]f)?\s*\d+)?",  # Optional 'of Number'
            ],
        )
    ),
}

regex_substitution_patterns: dict[str, tuple[Pattern, str]] = {
    "nbsp": (re.compile(r"\xa0"), " "),
}

regex_substitutions: set[Callable[[str], str]] = {
    lambda line: substitution_pattern.sub(repl, line)
    for substitution_pattern, repl in regex_substitution_patterns.values()
}

apply_substitutions: Callable[[str], str] = lambda line: reduce(
    lambda s, f: f(s), regex_substitutions, line
)

filters: Callable[[str], bool] = lambda line: any(
    not pattern.match(line) for pattern in regex_filter_patterns.values()
)


process_pdf: Callable[[list[PageObject]], str] = lambda pages: "\n".join(
    [
        apply_substitutions(line)
        for page in pages
        for line in filter(filters, page.extract_text().split("\n"))
    ]
)


def pdf_to_json(config) -> BaseModel | None:
    response = get_ollama_response(
        config, process_pdf(_load_pdf(config.data.default_resume))
    )
    if response.message.content:
        return _save_model(Resume, response.message.content)

    logger.error("No content in response.message")
    logger.debug(response.message)
