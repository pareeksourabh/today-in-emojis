#!/bin/bash
# Load and export environment variables from .env.local
# Usage: source scripts/load_env.sh

if [ ! -f .env.local ]; then
    echo "Error: .env.local not found"
    echo "Copy .env.example to .env.local and fill in your values"
    return 1
fi

# Read .env.local and export each variable
set -a  # Automatically export all variables
source .env.local
set +a  # Turn off auto-export

echo "Environment variables loaded from .env.local"
echo "GOOGLE_CLOUD_PROJECT: $GOOGLE_CLOUD_PROJECT"
echo "CLOUD_STORAGE_BUCKET: $CLOUD_STORAGE_BUCKET"
echo "CLOUD_DRY_RUN: $CLOUD_DRY_RUN"
