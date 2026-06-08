#!/bin/bash

set -e

FRONTEND_DIR="frontend"
SRC_DIR="$FRONTEND_DIR/src"

create_file_if_missing() {
  local file_path="$1"

  if [ ! -f "$file_path" ]; then
    touch "$file_path"
    echo "Created file: $file_path"
  fi
}

echo "Creating frontend test views structure..."

# Check frontend exists
if [ ! -d "$FRONTEND_DIR" ]; then
  echo "Error: frontend directory does not exist."
  echo "Please run this script from the project root."
  exit 1
fi

# Create test folders
mkdir -p "$SRC_DIR/testviews"
mkdir -p "$SRC_DIR/testapi"
mkdir -p "$SRC_DIR/testcomponents"

echo "Frontend test views structure created successfully."