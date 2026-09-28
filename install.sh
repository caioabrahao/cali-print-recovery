#!/usr/bin/env bash

set -euo pipefail

# ============================================================
# Cali Print Recovery Assistant
# Installer
# ============================================================

APP_NAME="cali-pra"
MODULE_NAME="cali_pra"
SERVICE_NAME="cali-pra.service"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_USER="$(id -un)"
VENV_DIR="$APP_DIR/.venv"
CONFIG_FILE="$APP_DIR/config.toml"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"
DEFAULT_MOONRAKER_URL="ws://localhost:7125/websocket"

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

info() {
	printf " \033[34m→\033[0m %s\n" "$1"
}

success() {
	printf " \033[32m✓\033[0m %s\n" "$1"
}

warning() {
	printf " \033[33m!\033[0m %s\n" "$1"
}

error() {
	printf " \033[31m✗\033[0m %s\n" "$1" >&2
}

die() {
	error "$1"
	exit 1
}

ask() {
	local prompt="$1"
	local default="$2"
	local answer

	read -r -p " $prompt [$default]: " answer
	echo "${answer:-$default}"
}

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

echo
echo "=============================================="
echo " Cali Print Recovery Assistant"
echo " Installer"
echo "=============================================="
echo

# ------------------------------------------------------------
# Detect environment
# ------------------------------------------------------------

info "Detecting environment..."
success "User: $CURRENT_USER"
success "Install directory: $APP_DIR"

# ------------------------------------------------------------
# Check Python
# ------------------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
	die "python3 was not found. Please install Python 3 first."
fi

PYTHON="$(command -v python3)"
PYTHON_VERSION="$("$PYTHON" --version 2>&1)"
success "Python: $PYTHON_VERSION"

# ------------------------------------------------------------
# Check systemd
# ------------------------------------------------------------

if ! command -v systemctl >/dev/null 2>&1; then
	die "systemctl was not found. This installer requires systemd."
fi

success "systemd: available"

# ------------------------------------------------------------
# Check permissions
# ------------------------------------------------------------

if [[ "$CURRENT_USER" == "root" ]]; then
	die "Please run this installer as the user that should run Cali PRA, not root."
fi

if ! sudo -v; then
	die "sudo access is required to install the systemd service."
fi

success "sudo: available"

# ------------------------------------------------------------
# Moonraker configuration
# ------------------------------------------------------------

echo
info "Moonraker configuration"

if [[ -f "$CONFIG_FILE" ]]; then
	success "Existing config.toml found; preserving it."

	# Try to extract the existing URL.
	EXISTING_URL="$(
		sed -nE \
			's/^[[:space:]]*url[[:space:]]*=[[:space:]]*"([^"]+)".*/\1/p' \
			"$CONFIG_FILE" \
			| head -n 1
	)"

	if [[ -n "$EXISTING_URL" ]]; then
		MOONRAKER_URL="$EXISTING_URL"
		success "Moonraker URL: $MOONRAKER_URL"
	else
		warning "Could not detect Moonraker URL from existing config."
		MOONRAKER_URL="$(ask "Moonraker WebSocket URL" "$DEFAULT_MOONRAKER_URL")"
	fi
else
	MOONRAKER_URL="$(ask "Moonraker WebSocket URL" "$DEFAULT_MOONRAKER_URL")"
fi

# ------------------------------------------------------------
# Virtual environment
# ------------------------------------------------------------

echo
info "Python environment"

if [[ ! -d "$VENV_DIR" ]]; then
	info "Creating virtual environment..."
	"$PYTHON" -m venv "$VENV_DIR"
	success "Virtual environment created."
else
	success "Virtual environment already exists."
fi

# ------------------------------------------------------------
# Upgrade pip
# ------------------------------------------------------------

info "Updating pip..."
"$VENV_DIR/bin/python" -m pip install --upgrade pip >/dev/null
success "pip ready."

# ------------------------------------------------------------
# Install dependencies
# ------------------------------------------------------------

if [[ -f "$APP_DIR/requirements.txt" ]]; then
	info "Installing Python dependencies..."
	"$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"
	success "Dependencies installed."
else
	warning "requirements.txt not found; skipping dependency installation."
fi

# ------------------------------------------------------------
# Create configuration
# ------------------------------------------------------------

if [[ ! -f "$CONFIG_FILE" ]]; then
	info "Creating config.toml..."
	cat > "$CONFIG_FILE" <<EOF
[moonraker]
url = "$MOONRAKER_URL"

[logging]
level = "INFO"
rich = true

[recovery]
checkpoint_interval = "layer"
EOF
	success "Created $CONFIG_FILE"
else
	success "Existing config.toml preserved."
fi

# ------------------------------------------------------------
# Generate systemd service
# ------------------------------------------------------------

echo
info "Generating systemd service..."

sudo tee "$SERVICE_FILE" >/dev/null <<EOF
[Unit]
Description=Cali Print Recovery Assistant
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$APP_DIR
ExecStart=$VENV_DIR/bin/python -m $MODULE_NAME
Restart=on-failure
RestartSec=3
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

success "Generated $SERVICE_FILE"

# ------------------------------------------------------------
# Install / reload service
# ------------------------------------------------------------

info "Reloading systemd..."
sudo systemctl daemon-reload
success "systemd configuration reloaded."

# ------------------------------------------------------------
# Enable service
# ------------------------------------------------------------

info "Enabling Cali PRA at boot..."
sudo systemctl enable "$SERVICE_NAME" >/dev/null
success "Service enabled."

# ------------------------------------------------------------
# Start / restart service
# ------------------------------------------------------------

if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
	info "Cali PRA is already running; restarting..."
	sudo systemctl restart "$SERVICE_NAME"
else
	info "Starting Cali PRA..."
	sudo systemctl start "$SERVICE_NAME"
fi

# ------------------------------------------------------------
# Verify
# ------------------------------------------------------------

sleep 1

if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
	success "Cali PRA is running."
else
	error "Cali PRA failed to start."
	echo
	echo "Last service logs:"
	echo "----------------------------------------------"
	sudo journalctl -u "$SERVICE_NAME" -n 30 --no-pager
	echo "----------------------------------------------"
	exit 1
fi

# ------------------------------------------------------------
# Done
# ------------------------------------------------------------

echo
echo "=============================================="
echo " Cali PRA installed!"
echo "=============================================="
echo
echo " User: $CURRENT_USER"
echo " Directory: $APP_DIR"
echo " Python: $VENV_DIR/bin/python"
echo " Moonraker: $MOONRAKER_URL"
echo " Service: $SERVICE_NAME"
echo
echo "Useful commands:"
echo
echo " Status:"
echo " systemctl status $SERVICE_NAME"
echo
echo " Live logs:"
echo " journalctl -u $SERVICE_NAME -f"
echo
echo " Restart:"
echo " sudo systemctl restart $SERVICE_NAME"
echo
echo " Stop:"
echo " sudo systemctl stop $SERVICE_NAME"
echo
echo " Start:"
echo " sudo systemctl start $SERVICE_NAME"
echo
echo "=============================================="
echo