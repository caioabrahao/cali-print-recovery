import asyncio
from cali_prt.api.websocket import moonraker_listener

def start_websocket():
    try:
        # Inicia o loop de eventos assíncrono do Python
        asyncio.run(moonraker_listener())
    except KeyboardInterrupt:
        print("\nCliente desconectado pelo usuário.")
    except Exception as e:
        print(f"Erro na conexão: {e}")

def main ():
    print("Print Recovery Running!")
    start_websocket()