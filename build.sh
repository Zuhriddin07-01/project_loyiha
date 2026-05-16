#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

pip install -r requirements.txt

# Seed the database with sample data
python seed_data.py || true
