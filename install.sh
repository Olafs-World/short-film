#!/usr/bin/env bash
# Install script for short-film

set -e

TOOL_NAME="short-film"

echo "🎬 Installing $TOOL_NAME..."

# Detect package manager
if command -v uv &> /dev/null; then
    echo "📦 Using uv..."
    uv tool install $TOOL_NAME
elif command -v pipx &> /dev/null; then
    echo "📦 Using pipx..."
    pipx install $TOOL_NAME
elif command -v pip &> /dev/null; then
    echo "📦 Using pip..."
    pip install --user $TOOL_NAME
else
    echo "❌ No package manager found. Please install uv, pipx, or pip first."
    exit 1
fi

echo "✅ $TOOL_NAME installed successfully!"
echo ""
echo "Try it out:"
echo "  $TOOL_NAME --help"
echo "  $TOOL_NAME generate"
