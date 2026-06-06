#!/usr/bin/env bash
set -e

export PYTHONPATH="$(pwd)"
export DATABASE_URL="${DATABASE_URL:-postgresql://postgres:postgres@127.0.0.1:5432/medical_db}"

bash scripts/ci/wait_for_postgres.sh
python scripts/seed_database.py

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

for i in {1..30}; do
  if curl -sf http://127.0.0.1:8000/ > /dev/null; then
    echo "Backend disponible."
    break
  fi
  echo "Esperando backend $i/30..."
  sleep 2
done

cd frontend/medical-frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173 &
FRONTEND_PID=$!
cd ../..

for i in {1..30}; do
  if curl -sf http://127.0.0.1:5173/ > /dev/null; then
    echo "Frontend disponible."
    break
  fi
  echo "Esperando frontend $i/30..."
  sleep 2
done

echo "BACKEND_PID=$BACKEND_PID" >> "${BASH_ENV:-/dev/null}"
echo "FRONTEND_PID=$FRONTEND_PID" >> "${BASH_ENV:-/dev/null}"
