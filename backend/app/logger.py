import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, tz=None):
        super().__init__(fmt, datefmt)
        self.tz = tz

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, self.tz)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            s = dt.isoformat()
        return s


# Logger configuration
formatter = CustomFormatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", tz=None
)

# logger configuration 7 days of logs
handler = TimedRotatingFileHandler(
    "app_log.txt", when="midnight", interval=1, backupCount=7
)
handler.setFormatter(formatter)

logger = logging.getLogger("app")
logger.setLevel(logging.WARNING)
logger.addHandler(handler)
