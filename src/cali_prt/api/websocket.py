import json
from websockets.asyncio.client import connect
from cali_prt.core.bookkeeper import saveIndividualRegistry

# Configurações do Moonraker
MOONRAKER_HOSTNAME = "klipper.local"  
MOONRAKER_PORT = 7125
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
                    "heater_bed": ["temperature", "target"],
                    "extruder": ["temperature", "target"],
                    "print_stats": ["filename", "state", "progress"],
                    "toolhead": ["position", "estimated_print_time"]
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
            
            else:
                print(f"Mensagem do sistema: {data}")
                saveIndividualRegistry(data)

