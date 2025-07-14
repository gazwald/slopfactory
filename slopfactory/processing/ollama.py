"""
Client: https://github.com/ollama/ollama-python/tree/63ca74762284100b2f0ad207bc00fa3d32720fbd?tab=readme-ov-file#custom-client
Structured Outputs: https://github.com/ollama/ollama-python/blob/63ca74762284100b2f0ad207bc00fa3d32720fbd/examples/structured-outputs.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ollama import Client
from slopfactory.schema import Config, Resume
from slopfactory.utils.logger import logger

if TYPE_CHECKING:
    from ollama import ChatResponse
    from slopfactory.schema import BaseModel


def get_client(config: Config) -> Client:
    logger.info(config.host.as_uri)
    return Client(
        host=config.host.as_uri,
    )


def get_ollama_response(
    config: Config,
    message: str,
    prompt: str | None = None,
    client: Client | None = None,
    model: type[BaseModel] = Resume,
) -> ChatResponse:
    if not client:
        client = get_client(config)

    return client.chat(
        model=config.model,
        messages=[
            {
                "role": "system",
                "content": prompt or config.default_system_prompt,
            },
            {
                "role": "user",
                "content": message or config.default_user_prompt,
            },
        ],
        format=model.model_json_schema(),
    )
