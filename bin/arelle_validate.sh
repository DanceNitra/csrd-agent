#!/bin/bash
# Arelle validation wrapper — uses official Arelle source + Python 3.11 venv
ARELLE_DIR="/tmp/arelle-official"
VENV_PYTHON="/tmp/arelle311-venv/bin/python3"
PYTHONPATH="$ARELLE_DIR:$PYTHONPATH" exec "$VENV_PYTHON" -m arelle.CntlrCmdLine "$@"