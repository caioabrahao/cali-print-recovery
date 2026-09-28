from dataclasses import dataclass, field, fields, is_dataclass
from datetime import datetime, timezone
from typing import Mapping, Optional

@dataclass
class PrintStats:
    state: Optional[str] = None
    filename: Optional[str] = None
    total_duration: float = 0.0
    print_duration: float = 0.0
    filament_used: float = 0.0
    message: Optional[str] = None
    info: dict = field(default_factory=dict)


@dataclass
class VirtualSdCard:
    progress: float = 0.0
    file_position: int = 0


@dataclass
class Toolhead:
    position: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0])
    homed_axes: str = ""


@dataclass
class GcodeMove:
    gcode_position: list[float] = field(
        default_factory=lambda: [0.0, 0.0, 0.0, 0.0]
    )
    homing_origin: list[float] = field(
        default_factory=lambda: [0.0, 0.0, 0.0]
    )
    absolute_coordinates: bool = True
    absolute_extrude: bool = True
    speed: float = 0.0
    speed_factor: float = 1.0
    extrude_factor: float = 1.0


@dataclass
class Extruder:
    temperature: float = 0.0
    target: float = 0.0


@dataclass
class HeaterBed:
    temperature: float = 0.0
    target: float = 0.0

# MAIN PRINTER STATE
@dataclass
class PrinterState:
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    print_stats: PrintStats = field(default_factory=PrintStats)
    virtual_sdcard: VirtualSdCard = field(default_factory=VirtualSdCard)
    toolhead: Toolhead = field(default_factory=Toolhead)
    gcode_move: GcodeMove = field(default_factory=GcodeMove)
    extruder: Extruder = field(default_factory=Extruder)
    heater_bed: HeaterBed = field(default_factory=HeaterBed)


def _apply_status_update(target: object, values: Mapping[str, object]) -> None:
    valid_fields = {item.name for item in fields(target)} # type: ignore

    for name, value in values.items():
        if name not in valid_fields:
            continue

        current_value = getattr(target, name)
        if is_dataclass(current_value) and isinstance(value, Mapping):
            _apply_status_update(current_value, value)
        else:
            setattr(target, name, value)


def update_current_printer_state(status_updates: Mapping[str, object]) -> None:
    """Merge a Moonraker status update into the shared printer state."""
    _apply_status_update(currentPrinterState, status_updates)
    currentPrinterState.timestamp = datetime.now(timezone.utc)


@dataclass
class Checkpoint:
    timestamp: datetime
    layer: Optional[int]
    z: float
    file_position: int
    filename: Optional[str]


@dataclass
class RecoverySession:
    started_at: datetime
    ended_at: Optional[datetime] = None

    filename: Optional[str] = None

    checkpoints: list[Checkpoint] = field(default_factory=list)

    # Rolling buffer of recent observations.
    recent_states: list[PrinterState] = field(default_factory=list)

currentPrinterState = PrinterState()