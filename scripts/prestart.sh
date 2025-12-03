#!/usr/bin/env nash

set -e
set -x

alembic upgrade head

python app/initial_data.py