#!/bin/bash

# Development server startup script for Flow Automation
# This runs the Vue dev server on port 8083

echo "🚀 Starting Flow Automation Vue Dev Server"
echo ""

# Check if we're in the right directory
if [ ! -f "build.sh" ]; then
    echo "❌ Error: Please run this script from /home/jumes/bench/apps/spry/"
    exit 1
fi

echo "📦 Installing dependencies (if needed)..."
cd frontend
if [ ! -d "node_modules" ]; then
    yarn install
fi

echo ""
echo "🔥 Starting Vite dev server on port 8083..."
echo "   Access the app at: http://spry.localhost:8002/flow-automation/"
echo "   (Will auto-redirect to http://spry.localhost:8083/flow-automation/)"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

yarn dev
