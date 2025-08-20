#!/bin/bash

set -e

echo "🚀 Starting Metropolia Weather Map with Skaffold"

# Check if Kubernetes cluster is accessible
if ! kubectl cluster-info &>/dev/null; then
    echo "❌ Cannot access Kubernetes cluster. Please ensure Orbstack is running."
    exit 1
fi

# Check if skaffold is installed
if ! command -v skaffold &>/dev/null; then
    echo "❌ Skaffold not found. Please install Skaffold:"
    echo "   brew install skaffold"
    exit 1
fi

echo "✅ Kubernetes cluster accessible"
echo "✅ Skaffold installed"

# Create namespace if it doesn't exist
kubectl create namespace weather-map --dry-run=client -o yaml | kubectl apply -f -

# Set default profile
PROFILE=${1:-"dev"}

echo "🔧 Using profile: $PROFILE"
echo "📋 This will:"
echo "   - Build Docker images locally"
echo "   - Deploy to weather-map namespace"
echo "   - Forward ports: 3000 (client), 8000 (server), 5432 (database)"
echo "   - Enable hot reloading for source code changes"
echo ""
echo "🌐 Once running, access:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - Database: localhost:5432"
echo ""
echo "Press Ctrl+C to stop..."
echo ""

# Start skaffold
skaffold dev --profile="$PROFILE" --port-forward