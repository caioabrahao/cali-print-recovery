from pathlib import Path
import json
import time
from datetime import datetime, timezone
import cali_pra.console.logger as logger

currentDir = Path(__file__).resolve()
REGISTRY_DIR = currentDir.parent.parent.parent.parent / "bookkeeper" / "registry"


def _get_nested(data, *keys):
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def normalize_registry(registry_data):
    toolhead_position = _get_nested(registry_data, "toolhead", "position") or []
    print_stats = registry_data.get("print_stats", {})
    print_info = print_stats.get("info", {}) if isinstance(print_stats, dict) else {}

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "filename": print_stats.get("filename") if isinstance(print_stats, dict) else None,
        "layer": (
            print_stats.get("current_layer", print_info.get("current_layer"))
            if isinstance(print_stats, dict)
            else None
        ),
        "x": toolhead_position[0] if len(toolhead_position) > 0 else None,
        "y": toolhead_position[1] if len(toolhead_position) > 1 else None,
        "z": toolhead_position[2] if len(toolhead_position) > 2 else None,
        "e": toolhead_position[3] if len(toolhead_position) > 3 else None,
        "hotend": _get_nested(registry_data, "extruder", "temperature"),
        "bed": _get_nested(registry_data, "heater_bed", "temperature"),
        "progress": _get_nested(registry_data, "virtual_sdcard", "progress"),
    }


def saveIndividualRegistry(registryData):
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

    timestamp_id = int(time.time() * 1000)
    fileName = REGISTRY_DIR / f"reading_{timestamp_id}.json"

    with open(fileName, "w", encoding="utf-8") as arquivo:
        json.dump(normalize_registry(registryData), arquivo, ensure_ascii=False, indent=4)

    logger.debug(f"Registry created at: {REGISTRY_DIR.resolve()}")
    clearOldRegistries()


def clearOldRegistries():
    arquivos = [f for f in REGISTRY_DIR.iterdir() if f.is_file()]
    arquivos.sort(key=lambda f: f.stat().st_mtime)

    while len(arquivos) > 5:
        arquivo_mais_antigo = arquivos.pop(0)
        arquivo_mais_antigo.unlink()  
