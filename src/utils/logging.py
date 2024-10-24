import logging
from pathlib import Path
from typing import Optional

def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
):
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format,
        handlers=[
            logging.StreamHandler(),
            *([] if not log_file else [logging.FileHandler(log_file)])
        ]
    )