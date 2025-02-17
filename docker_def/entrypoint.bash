#!/bin/sh

/dock_env/bin/alembic upgrade head
/dock_env/bin/uvicorn webapp:app --host 0.0.0.0 --port 80 --reload 