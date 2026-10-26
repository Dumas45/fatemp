import logging
import sys

logger = logging.getLogger(__name__)


def configure_logging(level_name: str) -> None:
    normalized_level = level_name.upper()
    if normalized_level not in logging.getLevelNamesMapping():
        raise ValueError(f"Invalid log level: {level_name}")

    logging.basicConfig(
        level=normalized_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
    logging.getLogger().setLevel(normalized_level)
