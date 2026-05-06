#!/bin/bash

set -e

APP_NAME="scouting-football-app"
CONTAINER_NAME="samplerunning"

if [ -z "$THESPORTSDB_API_KEY" ]; then
  echo "Error: exporta THESPORTSDB_API_KEY antes de ejecutar build.sh"
  exit 1
fi

if [ -z "$PLAYER_NAME" ]; then
  export PLAYER_NAME="Lionel Messi"
fi

echo "Creando Dockerfile..."

cat > Dockerfile << 'EOF'
FROM python:3.11-slim

ENV PIP_PROGRESS_BAR=off

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
EOF

echo "Construyendo imagen Docker..."
DOCKER_BUILDKIT=0 docker build -t "$APP_NAME" .

echo "Eliminando contenedor previo si existe..."
docker stop "$CONTAINER_NAME" || true
docker rm "$CONTAINER_NAME" || true

echo "Ejecutando contenedor..."
docker run --name "$CONTAINER_NAME" \
  -e THESPORTSDB_API_KEY="$THESPORTSDB_API_KEY" \
  -e PLAYER_NAME="$PLAYER_NAME" \
  "$APP_NAME"

mkdir -p evidencias/docker

echo "Guardando salida en evidencias/docker/output.txt..."
{
  echo "===== docker ps -a ====="
  docker ps -a
  echo ""
  echo "===== docker logs ${CONTAINER_NAME} ====="
  docker logs "$CONTAINER_NAME"
} > evidencias/docker/output.txt

echo "Proceso finalizado correctamente."
