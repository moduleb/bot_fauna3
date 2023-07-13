# Настройки логгера
from dataclasses import dataclass


@dataclass
class LoggerConfig:
    LOGFILE: str = 'log.log'
    CLEAR_PERIOD_DAYS: int = 30
    LOG_IN_FILE: bool = False
    LEVEL: str = "DEBUG"
    # LEVEL: str = "INFO"
    # LEVEL: str = "WARN"
    # LEVEL: str = "CRITICAL"
    # LEVEL: str = "ERROR"