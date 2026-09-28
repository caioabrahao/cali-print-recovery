#!/bin/bash
set -e

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_NAME="cali-pra"

echo "Installing Cali Print Recovery Assistant..."

echo "Creating virtual environment..."
python3 -m venv "$APP_DIR/.venv"

echo "Installing dependencies..."
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"

echo "Installing systemd service..."

sudo cp "$APP_DIR/cali-pra.service" \
    "/etc/systemd/system/$SERVICE_NAME.service"

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo
echo "Cali PRA installed."
echo

sudo systemctl status "$SERVICE_NAME" --no-pager