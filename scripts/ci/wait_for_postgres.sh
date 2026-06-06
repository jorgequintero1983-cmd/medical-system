#!/usr/bin/env bash
set -e

echo "Esperando a que PostgreSQL esté listo..."
for i in {1..30}; do
  if python -c "import socket; s=socket.socket(); s.settimeout(1); s.connect(('127.0.0.1', 5432)); s.close()"; then
    echo "PostgreSQL disponible."
    exit 0
  fi
  echo "Intento $i/30..."
  sleep 2
done

echo "PostgreSQL no respondió a tiempo."
exit 1
