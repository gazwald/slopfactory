from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING

from pypdf import PdfReader

from slopfactory.utils.logger import logger

if TYPE_CHECKING:
    from typing import Literal

    from pypdf import PageObject

    from slopfactory.schema import BaseModel

OUTPUT_DIR = Path("outputs")


def _read_file(path: Path) -> str | None:
    if not path.exists():
        logger.error(f"{path} does not exist")
        return

    if not path.is_file():
        logger.error(f"{path} is not a file")
        return

    logger.info("Reading %s", path)
    return path.read_text()


def _load_data(path: str | None = None) -> str | None:
    if path is None and len(sys.argv) == 2:
        path = sys.argv[1]

    if path is not None:
        return _read_file(Path(path))

    logger.info("No path provided")
    return None


def _load_pdf(path: str = "inputs/resume.pdf") -> list[PageObject]:
    logger.info("Reading PDF %s", path)
    reader = PdfReader(path)
    return reader.pages


def _write_file(path: Path, data: str) -> Exception | None:
    try:
        logger.info("Writing %s", path)
        with path.open("w") as f:
            f.write(data)
    except Exception as e:
        logger.error("Exception occured writing file")
        return e
    else:
        return None


def _symlink(path: Path, symlink: Path):
    symlink.unlink(missing_ok=True)
    logger.info("Creating symlink %s", symlink)
    symlink.symlink_to(path.resolve())


def _save_model(
    model: type[BaseModel],
    data: str,
    file_format: Literal["json"] = "json",
) -> BaseModel:
    model_instance = model.model_validate_json(data)
    model_json = model_instance.model_dump_json(indent=2)

    model_name = model.__name__.casefold()
    path = OUTPUT_DIR / Path(f"{time.time_ns()}_{model_name}.{file_format}")
    symlink = OUTPUT_DIR / Path(f"{model_name}.latest.{file_format}")

    _write_file(path, model_json)
    _symlink(path, symlink)

    return model_instance
