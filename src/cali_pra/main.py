import asyncio
from cali_pra.api.websocket import moonraker_listener
import cali_pra.console.logger as logger


def start_websocket():
    try:
        asyncio.run(moonraker_listener())
    except KeyboardInterrupt:
        logger.warn("Client Disconnected by User")
    except Exception as e:
        logger.error(f"Connection Error: {e}")
        logger.error("Is the connection properly configured?")

def main ():
    logger.console.print("Cali Print Recovery Bookkeeper Started")
    start_websocket()