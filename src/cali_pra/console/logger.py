from rich import print
from rich.console import Console

console = Console()

def info(text: str):
    console.log(text, style="blue")

def warn(text: str):
    console.log(text, style="yellow")

def error(text: str):
    console.log(text, style="red")

def debug(text: str):
    console.log(text, style="white")