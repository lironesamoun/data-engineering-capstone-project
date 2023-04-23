
# config/config.py
import os
import logging.config
import sys
from pathlib import Path
from rich.logging import RichHandler
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", os.environ.get("TF_VAR_GCP_CREDS"))

# Directories
BASE_DIR = Path(__file__).parent.parent.absolute()
CONFIG_DIR = Path(BASE_DIR, "conf")
DATA_DIR = Path(BASE_DIR, "data")
LOGS_DIR = Path(BASE_DIR, "logs")

DATASET_EXCEL_LINKS = [
    "https://github.com/lironesamoun/data-engineering-capstone-project/releases/download/assets/globalterrorismdb_0522dist.xlsx",
    "https://github.com/lironesamoun/data-engineering-capstone-project/releases/download/assets/globalterrorismdb_2021Jan-June_1222dist.xlsx"
]
DATASET_CSV_LINKS = "https://github.com/lironesamoun/data-engineering-capstone-project/releases/download/assets/globalterrorismdb.csv"

# Create dirs
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Logger
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "event": {"format": "%(asctime)s;%(message)s"},
        "standard": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
        "detailed": {
            "format": "%(levelname)s %(asctime)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)d]\n%(message)s\n"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "event",
            "level": logging.DEBUG,
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "info.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.INFO,
        },
        "error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "error.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.ERROR,
        },
    },
    "root": {
        "handlers": ["console", "info", "error"],
        "level": logging.INFO,
        "propagate": True,
    },
}
logging.config.dictConfig(logging_config)
logger = logging.getLogger()
logger.handlers[0] = RichHandler(markup=True)