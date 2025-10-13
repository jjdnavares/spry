#!/bin/bash

# Development startup script for Flow Automation

echo "🚀 Starting Flow Automation Development Environment"
echo ""

# Check if we're in the right directory
if [ ! -f "build.sh" ]; then
    echo "❌ Error: Please run this script from /home/jumes/bench/apps/spry/"
    exit 1
fi

echo "📦 Step 1: Building frontend assets..."
cd frontend
yarn build
if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi
cd ..

echo "✅ Frontend built successfully!"
echo ""

echo "🧹 Step 2: Clearing Frappe cache..."
cd /home/jumes/bench
bench --site spry.localhost clear-cache

echo "✅ Cache cleared!"
echo ""

echo "📋 Summary:"
echo "  - Frontend assets: /home/jumes/bench/apps/spry/spry/public/frontend/"
echo "  - Entry point: http://spry.localhost:8002/flow-automation"
echo ""

echo "🎯 Next steps:"
echo "  1. Start bench server: cd /home/jumes/bench && bench start"
echo "  2. Open browser: http://spry.localhost:8002/flow-automation"
echo "  3. Login with your credentials"
echo "  4. Test the overview page!"
echo ""

echo "📚 See TEST.md for detailed testing checklist"
echo ""
echo "✨ Ready to go!"
