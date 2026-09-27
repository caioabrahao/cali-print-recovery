# Cali: Printer Recovery Assistant

I lost a few prints because of power loss and klippy shutdowns. This app records checkpoint states in your print and saves them to disk, making it easier to recover the print later.

Connection settings are read from `config.toml` in the project root:

```toml
[moonraker]
hostname = "klipper.local"
port = 7125
```