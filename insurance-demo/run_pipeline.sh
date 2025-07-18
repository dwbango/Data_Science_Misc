#!/usr/bin/env bash
# resolve this script’s directory so we can refer to files absolutely
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
set -e

echo "1) Creating schemas..."
sqlcmd -S localhost -U sa -P MyStrongPass123 -d master \
       -i "$BASE_DIR/sql/01_create_schemas.sql"

echo "2) Truncating staging and loading raw data into staging with Python..."
sqlcmd -S localhost -U sa -P MyStrongPass123 -d InsurancePrediction \
       -i "$BASE_DIR/sql/02_load_staging.sql"

# Run the Python loader
cd "$BASE_DIR/src"
python load_staging.py
cd "$BASE_DIR"

echo "3) Cleaning into production..."
sqlcmd -S localhost -U sa -P MyStrongPass123 -d InsurancePrediction \
       -i "$BASE_DIR/sql/03_load_cleaned.sql"

echo "4) Scoring with Python..."
cd "$BASE_DIR/src"
python score.py
cd "$BASE_DIR"

echo "Pipeline completed successfully."
