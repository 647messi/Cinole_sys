#!/bin/bash

set -e

BACKEND_DIR="backend"
APP_DIR="$BACKEND_DIR/app"

DOMAINS=(
  "master"
  "procurement"
  "inventory"
  "production"
  "finance"
  "system"
)

MASTER_MODULES=(
  "supplier"
  "material"
  "customer"
  "warehouse"
)

create_file_if_missing() {
  local file_path="$1"

  if [ ! -f "$file_path" ]; then
    touch "$file_path"
    echo "Created file: $file_path"
  fi
}

echo "Creating backend base structure..."

# Backend root
mkdir -p "$BACKEND_DIR"

# Backend root files
create_file_if_missing "$BACKEND_DIR/main.py"
create_file_if_missing "$BACKEND_DIR/requirements.txt"
create_file_if_missing "$BACKEND_DIR/.env"
create_file_if_missing "$BACKEND_DIR/.gitignore"

# App base directories
mkdir -p "$APP_DIR"
mkdir -p "$APP_DIR/api/v1"
mkdir -p "$APP_DIR/core"
mkdir -p "$APP_DIR/db"
mkdir -p "$APP_DIR/middleware"

# Domain-based directories
for domain in "${DOMAINS[@]}"; do
  mkdir -p "$APP_DIR/api/v1/$domain"
  mkdir -p "$APP_DIR/schemas/$domain"
  mkdir -p "$APP_DIR/models/$domain"
  mkdir -p "$APP_DIR/repositories/$domain"
  mkdir -p "$APP_DIR/services/$domain"
done

# Create __init__.py for all Python package directories
while IFS= read -r dir; do
  create_file_if_missing "$dir/__init__.py"
done < <(find "$APP_DIR" -type d)

# Core infrastructure files
create_file_if_missing "$APP_DIR/api/v1/router.py"
create_file_if_missing "$APP_DIR/core/config.py"
create_file_if_missing "$APP_DIR/core/logging.py"
create_file_if_missing "$APP_DIR/db/base.py"
create_file_if_missing "$APP_DIR/db/session.py"
create_file_if_missing "$APP_DIR/middleware/request_log.py"

# Master modules
for module in "${MASTER_MODULES[@]}"; do
  create_file_if_missing "$APP_DIR/api/v1/master/${module}.py"
  create_file_if_missing "$APP_DIR/schemas/master/${module}.py"
  create_file_if_missing "$APP_DIR/models/master/${module}.py"
  create_file_if_missing "$APP_DIR/repositories/master/${module}_repository.py"
  create_file_if_missing "$APP_DIR/services/master/${module}_service.py"
done

echo "Backend project structure created successfully."