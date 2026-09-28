from cali_pra.api.websocket import start_websocket
import cali_pra.console.logger as logger


def main ():
    logger.title("Cali Print Recovery Bookkeeper Started")
    start_websocket()