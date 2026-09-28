import json
import asyncio
from rich.progress import Progress

from websockets.asyncio.client import connect
import cali_pra.console.logger as logger
from cali_pra.core.bookkeeper import saveIndividualRegistry
from cali_pra.config import load_moonraker_config
from cali_pra.schema import currentPrinterState, update_current_printer_state

from dataclasses import asdict

MOONRAKER_CONFIG = load_moonraker_config()
MOONRAKER_HOSTNAME = MOONRAKER_CONFIG["hostname"]
MOONRAKER_PORT = MOONRAKER_CONFIG["port"]
URL = f"ws://{MOONRAKER_HOSTNAME}:{MOONRAKER_PORT}/websocket"


def _contains_current_layer_update(value):
    if isinstance(value, dict):
        if "current_layer" in value:
            return True
        return any(_contains_current_layer_update(item) for item in value.values())

    return False


async def moonraker_listener():
    
    logger.info(f"Establishing Websocket Connection to: {URL}...")
    
    with Progress() as progress:
        connection_task = progress.add_task("Establishing websocket connection...", total=None)

        async with connect(URL) as websocket:
            progress.update(connection_task, completed=1, total=1)
            progress.stop()

            logger.info("Websocket connected successfully!")

            subscribe_message = {
                "jsonrpc": "2.0",
                "method": "printer.objects.subscribe",
                "params": {
                    "objects": {
                        "print_stats": [
                            "filename",
                            "total_duration",
                            "print_duration",
                            "filament_used",
                            "info"
                        ],
                        "virtual_sdcard": [
                            "file_path",
                            "progress",
                            "is_active",
                            "file_position",
                            "file_size"
                        ],
                        "toolhead": [
                            "homed_axes", 
                            "print_time",
                            "stalls",
                            "estimated_print_time",
                            "position"
                        ],
                        "extruder": [
                            "target",
                            "temperature",
                            "motion_queue",
                            "power"
                        ],
                        "heater_bed": [
                            "target",
                            "temperature",
                            "power",
                        ],
                        "gcode_move": [
                            "speed_factor",
                            "speed",
                            "extrude_factor",
                            "absolute_coordinates",
                            "absolute_extrude",
                            "homing_origin",
                            "position",
                            "gcode_position"
                        ]
                    }
                },
                "id": 1
            }

            await websocket.send(json.dumps(subscribe_message))
            # logger.info("Moonraker Subscription Requested")

            async for message in websocket:
                data = json.loads(message)

                if "status" in data:
                    logger.info("Websocket connection Established.")
                
                if "method" in data and data["method"] == "notify_status_update":
                    status_updates = data["params"][0]
                    update_current_printer_state(status_updates)

                    # Save a registry whenever Moonraker reports a layer update.
                    if _contains_current_layer_update(status_updates):
                        saveIndividualRegistry(status_updates)
                        logger.info("Layer change detected; registry saved.")
                        logger.debugJson(json.dumps(status_updates))
                    # logger.debugJson(json.dumps(asdict(currentPrinterState)))


def start_websocket():
    try:
        asyncio.run(moonraker_listener())
    except KeyboardInterrupt:
        logger.warn("Client Disconnected by User")
    except Exception as e:
        logger.error(f"Runtime Error: {e}")