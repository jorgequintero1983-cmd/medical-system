#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

BACKEND_COVERAGE="${BACKEND_COVERAGE:-coverage.xml}"
FRONTEND_COVERAGE="${FRONTEND_COVERAGE:-frontend/medical-frontend/coverage/cobertura-coverage.xml}"
OUTPUT_DIR="${OUTPUT_DIR:-reportes-html/cobertura-proyecto}"
OUTPUT_XML="${OUTPUT_DIR}/Cobertura.xml"

python scripts/ci/merge_coverage.py \
  --backend "$BACKEND_COVERAGE" \
  --frontend "$FRONTEND_COVERAGE" \
  --output "$OUTPUT_XML"

if command -v dotnet >/dev/null 2>&1; then
  mkdir -p .tools
  dotnet tool install dotnet-reportgenerator-globaltool --tool-path .tools >/dev/null 2>&1 || true
  if [ -x ".tools/reportgenerator" ]; then
    ./.tools/reportgenerator \
      -reports:"${OUTPUT_XML}" \
      -targetdir:"${OUTPUT_DIR}" \
      -reporttypes:"HtmlInline_AzurePipelines" \
      -sourcedirs:"backend/app;frontend/medical-frontend/src"
    echo "Reporte HTML Azure generado en ${OUTPUT_DIR}"
  fi
fi

echo "Cobertura del proyecto lista: ${OUTPUT_XML}"
