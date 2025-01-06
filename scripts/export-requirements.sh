#!/usr/bin/env bash

set -e

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Exporting requirements using poetry...${NC}"
poetry export --without-hashes --only main -f requirements.txt -o requirements-production.txt
echo -e "${GREEN}Exporting has been done successfully!${NC}"
