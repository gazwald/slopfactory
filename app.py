#!/usr/bin/env python
"""
Client: https://github.com/ollama/ollama-python/tree/63ca74762284100b2f0ad207bc00fa3d32720fbd?tab=readme-ov-file#custom-client
Structured Outputs: https://github.com/ollama/ollama-python/blob/63ca74762284100b2f0ad207bc00fa3d32720fbd/examples/structured-outputs.py
"""

from pprint import pprint

from slopfactory.processing.pdf import pdf_to_json
from slopfactory.schema import Config


def main(config: Config | None = None):
    if not config:
        config = Config()

    result = pdf_to_json(config)
    if result:
        pprint(
            result.model_dump(
                exclude_defaults=True,
                exclude_none=True,
                exclude_unset=True,
            )
        )


if __name__ == "__main__":
    main()
