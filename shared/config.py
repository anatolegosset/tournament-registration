import os
from datetime import datetime


def get_config_from_env():
    config = {
        "MAX_ENTRIES_PER_DAY": int(os.environ.get("MAX_ENTRIES_PER_DAY", 3)),
        "DEBUG": os.environ.get("DEBUG", False) == "TRUE",
        "FFTT_API_URL": os.environ.get("FFTT_API_URL"),
        "FFTT_SERIAL_NO": os.environ.get("FFTT_SERIAL_NO"),
        "FFTT_APP_ID": os.environ.get("FFTT_APP_ID"),
        "FFTT_PASSWORD": os.environ.get("FFTT_PASSWORD"),
    }

    if dt_str := os.environ.get("TOURNAMENT_REGISTRATION_CUTOFF", None):
        config["TOURNAMENT_REGISTRATION_CUTOFF"] = datetime.fromisoformat(dt_str)

    return config
