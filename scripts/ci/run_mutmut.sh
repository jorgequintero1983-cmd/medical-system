#!/usr/bin/env bash
set -e

export PYTHONPATH="$(pwd)"
export DATABASE_URL="${DATABASE_URL:-postgresql://postgres:postgres@127.0.0.1:5432/medical_db}"

echo "=== Pruebas de Mutación (Mutmut) ==="
python -m mutmut run 2>&1 | tee resultados-mutacion.log
python -m mutmut results | tee resultados-mutacion.txt

echo "Mutación completada. Revise resultados-mutacion.txt"
