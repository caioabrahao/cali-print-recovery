import asyncio
from cali_pra.api.websocket import moonraker_listener


def start_websocket():
    try:
        asyncio.run(moonraker_listener())
    except KeyboardInterrupt:
        print("\nCliente desconectado pelo usuário.")
    except Exception as e:
        print(f"Erro na conexão: {e}")

def main ():
    print("Cali Print Recovery Running!")
    start_websocket()