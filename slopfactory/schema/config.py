import os
from pathlib import Path

from pydantic import Field

from slopfactory.schema.base import BaseModel


class HostConfig(BaseModel):
    scheme: str = os.getenv("OLLAMA_API_SCHEME", "http")
    host: str = os.getenv("OLLAMA_API_HOST", "localhost")
    port: str = os.getenv("OLLAMA_API_PORT", "11434")
    path: str = os.getenv("OLLAMA_API_PATH", "v1")

    @property
    def as_uri(self) -> str:
        # TODO: Use urllib
        return f"{self.scheme}://{self.host}:{self.port}"


class DataConfig(BaseModel):
    default_resume: Path = Path("inputs/resume.pdf")
    default_output: Path = Path("outputs/resume.json")
    symlink: bool = True


class Config(BaseModel):
    model: str = os.getenv("OLLAMA_MODEL", "qwen3:8b")
    default_system_prompt: str = "Process this resume"
    default_user_prompt: str = (
        "Generate the resume of "
        "a goat farmer who has had three different roles across at least two megacorps "
        "and has started their own boutique goat farm"
    )
    host: HostConfig = Field(default_factory=lambda: HostConfig())
    data: DataConfig = Field(default_factory=lambda: DataConfig())
