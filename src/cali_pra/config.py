from pathlib import Path
import tomllib


CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.toml"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}

    with CONFIG_PATH.open("rb") as config_file:
        return tomllib.load(config_file)


def load_moonraker_config() -> dict:
    config = {"hostname": "klipper.local", "port": 7125}
    config.update(load_config().get("moonraker", {}))
    return config


def load_verbose_config() -> bool:
    return load_config().get("logger", {}).get("verbose", True)