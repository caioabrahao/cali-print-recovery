import json
import tomllib
from pathlib import Path

from websockets.asyncio.client import connect
from cali_pra.core.bookkeeper import saveIndividualRegistry

CONFIG_PATH = Path("config.toml")


def load_moonraker_config():
    config = {"hostname": "klipper.local", "port": 7125}

    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("rb") as config_file:
            moonraker_config = tomllib.load(config_file).get("moonraker", {})
            config.update(moonraker_config)

    return config


MOONRAKER_CONFIG = load_moonraker_config()
MOONRAKER_HOSTNAME = MOONRAKER_CONFIG["hostname"]
MOONRAKER_PORT = MOONRAKER_CONFIG["port"]
URL = f"ws://{MOONRAKER_HOSTNAME}:{MOONRAKER_PORT}/websocket"

async def moonraker_listener():
    print(f"Establishing Websocket Connection to: {URL}...")
    
    async with connect(URL) as websocket:
        print("Websocket connected successfully!")

        subscribe_message = {
            "jsonrpc": "2.0",
            "method": "printer.objects.subscribe",
            "params": {
                "objects": {
                    "print_stats": None,
                    "virtual_sdcard": None,
                    "toolhead": None,
                    "extruder": None,
                    "heater_bed": None,
                    "gcode_move": None
                }
            },
            "id": 1
        }

        await websocket.send(json.dumps(subscribe_message))
        print("Moonraker Subscription Requested")


        async for message in websocket:
            data = json.loads(message)
            
            if "method" in data and data["method"] == "notify_status_update":
                status_updates = data["params"][0]
                print(f"Update: {status_updates}")
                saveIndividualRegistry(status_updates)

            # else:
            #     print(f"Mensagem do sistema: {data}")
            #     saveIndividualRegistry(data)

