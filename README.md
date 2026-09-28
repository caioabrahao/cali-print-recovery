# Cali: Printer Recovery Assistant

I lost a few prints because of power loss and klippy shutdowns. This app records checkpoint states in your print and saves them to disk, making it easier to recover the print later.

Connection settings are read from `config.toml` in the project root:

```toml
[moonraker]
hostname = "klipper.local"
port = 7125
```

## Run the thing

Make the virtual environment first:

```sh
python -m venv venv

# for cmd
venv\Scripts\activate.bat 

# for power shell
venv\Scripts\Activate.ps1

# for mac or the penguin
source venv/bin/activate 
```

Install the requirements:

```sh
pip install -r requirements.txt
```

Then:

```sh
cd src
python -m cali_pra
```
