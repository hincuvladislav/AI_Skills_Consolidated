#!/bin/bash
# Semantic search over the skills library from any project.
# Usage: search_skills.sh "what you're trying to do" [num_results]
DIR="$(cd "$(dirname "$0")" && pwd)"
PY="/Users/vladislavhincu/Projects/Agents/Agents/infrastructure/venv/bin/python"
exec "$PY" "$DIR/search_skills.py" "$1" -n "${2:-5}"
