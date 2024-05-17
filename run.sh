#!/bin/sh

# Environment variables that must be configured:
#SCANNER_MODEL
#SCANNER_IP

# Environment variables that can be configured if needed:
SCANNER_NAME="${SCANNER_NAME:-Brother}"
BIND_IP="${BIND_IP:-0.0.0.0}"
ADVERTISE_IP="${ADVERTISE_IP:-${BIND_IP}}"
CONFIG_FILE="${CONFIG_FILE:-/brother-scan.yaml}"

RESOLVED_SCANNER_IP=$(python3 -c "import socket; print(socket.gethostbyname('${SCANNER_IP}'))")

# Setup network scanner
brsaneconfig4 -a \
	name="${SCANNER_NAME}" model="${SCANNER_MODEL}" ip="${RESOLVED_SCANNER_IP}"

# Exec into service
exec brscand -c "${CONFIG_FILE}" -A "${ADVERTISE_IP}" \
	"${BIND_IP}" "${SCANNER_IP}"
