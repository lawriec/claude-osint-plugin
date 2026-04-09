#!/bin/bash
set -e

echo "=== OSINT Plugin Agent Container ==="
echo "Node: $(node --version)"
echo "Python: $(python3 --version)"
echo "uv: $(uv --version)"
echo ""

# Check for required API keys
if [ -z "$TAVILY_API_KEY" ]; then
    echo "WARNING: TAVILY_API_KEY not set. Web search will be limited."
fi
if [ -z "$GEMINI_API_KEY" ]; then
    echo "WARNING: GEMINI_API_KEY not set. Image/video analysis will be unavailable."
fi

echo "Starting Claude Code..."
echo ""

# Start Claude Code with the OSINT plugin
exec claude --dangerously-skip-permissions "$@"
