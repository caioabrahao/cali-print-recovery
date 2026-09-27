from dataclasses import dataclass
from datetime import datetime


@dataclass
class PrinterState:
    timestamp: datetime
    filename: str | None
    layer: int | None
    x: float | None
    y: float | None
    z: float | None
    e: float | None
    hotend: float | None
    bed: float | None
    progress: float | None

@dataclass
class Checkpoint:
    timestamp: datetime
    layer: int
    z: float
