from rich.console import Console
from rich.json import JSON
from rich.panel import Panel

console = Console()

def title(text:str):
    console.print(Panel(text))


def info(text: str):
    console.log(text, style="blue")

def warn(text: str):
    console.log(text, style="yellow")

def error(text: str):
    console.log(text, style="red")

def debug(text: str):
    console.log(text, style="white")

def debugJson(json):
    console.log(JSON(json), style="white")