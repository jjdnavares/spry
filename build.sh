#!/bin/bash

# Build script for Spry Flow Automation

echo "Building Flow Automation assets..."

cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    yarn install
fi

# Build the frontend
echo "Building Flow Automation..."
yarn build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✓ Flow Automation build completed successfully!"
    echo "Assets are available at: ../spry/public/frontend/"
else
    echo "✗ Build failed!"
    exit 1
fi

cd ..

echo ""
echo "Next steps:"
echo "1. Run: bench clear-cache"
echo "2. Run: bench restart"
echo "3. Access Flow Automation at: http://spry.localhost:8002/flow-automation"
