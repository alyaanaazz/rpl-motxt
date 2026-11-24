#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ENV_FOLDER="${ENV_FOLDER:-.venv}"
if [[ ! -x "$ENV_FOLDER/bin/python" ]]; then
    python3 -m venv "$ENV_FOLDER"
fi
PYTHON="$ENV_FOLDER/bin/python"
"$PYTHON" -m pip install -r requirements.txt
"$PYTHON" manage.py check
"$PYTHON" manage.py migrate
exec "$PYTHON" manage.py runserver "${1:-127.0.0.1:8000}"
