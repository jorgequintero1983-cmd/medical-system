#!/usr/bin/env bash
set -e

is_sonar_configured() {
  if [ -z "$SONAR_TOKEN" ]; then
    return 1
  fi
  if [ -z "$SONAR_HOST_URL" ]; then
    return 1
  fi
  if echo "$SONAR_HOST_URL" | grep -q 'SONAR_HOST_URL'; then
    return 1
  fi
  if ! echo "$SONAR_HOST_URL" | grep -Eq '^https?://'; then
    return 1
  fi
  return 0
}

if ! is_sonar_configured; then
  echo "##vso[task.logissue type=warning]SonarQube no configurado correctamente."
  echo "Configure estas variables en el pipeline de Azure DevOps:"
  echo "  SONAR_TOKEN     (secreto) - token de SonarCloud o SonarQube"
  echo "  SONAR_HOST_URL  (texto)   - ejemplo: https://sonarcloud.io"
  echo "Análisis SonarQube omitido sin error."
  exit 0
fi

echo "=== Análisis de Código (SonarQube) ==="
echo "Servidor: $SONAR_HOST_URL"

wget -q https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip -q sonar-scanner-cli-5.0.1.3006-linux.zip
export PATH="$(pwd)/sonar-scanner-5.0.1.3006-linux/bin:$PATH"

sonar-scanner \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.login="$SONAR_TOKEN"

echo "Análisis SonarQube completado."
