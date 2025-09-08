import logging
import os

class Logger:
    def __init__(self, name: str = "fastapi_server", log_dir: str = "logs"):
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(self.name)
        self._configure_logger()

    def _configure_logger(self):
        """Configure logger only once to prevent duplicate handlers."""
        if self.logger.handlers:
            return

        self.logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler
        os.makedirs(self.log_dir, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(self.log_dir, "agent_manager.log"))
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

# Global logger
logger = Logger().get_logger()