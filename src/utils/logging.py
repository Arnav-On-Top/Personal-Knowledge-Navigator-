import os
import logging
import sys
from typing import Optional

_loggers = {}

def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Get a logger instance."""
    if name in _loggers:
        return _loggers[name]
    
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        log_level = level or os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    _loggers[name] = logger
    return logger

# Ensure root logger has a handler
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
