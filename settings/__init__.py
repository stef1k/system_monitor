import json
from pathlib import Path

config_path = Path(__file__)

with open(config_path.with_name("logging_config.json")) as config_file:
    logger_config = json.load(config_file)

with open(config_path.with_name("token.json")) as config_file:
    token = json.load(config_file)
