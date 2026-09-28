from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from cali_pra.config import load_verbose_config

console = Console()
VERBOSE = load_verbose_config()

def title(text:str):
    console.print(Panel(text))


def info(text: str):
    console.log(text, style="blue")

def warn(text: str):
    console.log(text, style="yellow")

def error(text: str):
    console.log(text, style="red")

def debug(text: str):
    if not VERBOSE:
        return

    console.log(text, style="white")

def debugJson(json):
    if not VERBOSE:
        return

    console.log(JSON(json), style="white")