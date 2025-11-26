# Skaffold Configuration for Metropolia Weather Map

This project now supports local Kubernetes development using Skaffold with Orbstack, providing a production-like environment while preserving the Docker Compose development experience.

## 🚀 Quick Start

### Prerequisites
- [Orbstack](https://orbstack.dev/) running with Kubernetes enabled
- [Skaffold](https://skaffold.dev/) installed (`brew install skaffold`)
- Docker available in your environment

### Start Development Environment

```bash
# Simple startup (uses dev profile by default)
./run-skaffold.sh

# Or specify a profile
./run-skaffold.sh debug

# Or run skaffold directly
skaffold dev --port-forward
```

## 📋 What This Provides

### ✅ **Services Running**
- **PostgreSQL Database**: Available at `localhost:5432`
- **FastAPI Backend**: Available at `localhost:8000` 
- **Next.js Frontend**: Available at `localhost:3000`

### ✅ **Development Features**
- **Hot Reloading**: File changes automatically sync to containers
- **Port Forwarding**: Access services via localhost (just like Docker Compose)
- **Health Checks**: Automatic health monitoring for all services
- **Persistent Storage**: Database data survives pod restarts

### ✅ **Security Improvements**
- Non-root containers (uid: 1001 for client/server, 999 for database)
- Specific base image versions (no more generic `python:3`)
- Resource limits and health checks
- Proper secret management

## 🎯 Available Profiles

| Profile | Description | Use Case |
|---------|-------------|----------|
| `default` | Standard development | Daily development work |
| `dev` | Enhanced file sync | More comprehensive file watching |
| `debug` | Verbose logging | Troubleshooting issues |
| `db-only` | Database only | Database schema work |

## 📁 File Structure

```
├── skaffold.yaml           # Main Skaffold configuration
├── run-skaffold.sh         # Startup helper script
├── k8s/                    # Kubernetes manifests
│   ├── namespace.yaml      # weather-map namespace
│   ├── postgres.yaml       # Database deployment, service, PVC
│   ├── server.yaml         # FastAPI deployment & service
│   ├── client.yaml         # Next.js deployment & service
│   └── configmap.yaml      # Database initialization
├── client/
│   ├── Dockerfile          # Security-hardened Next.js container
│   └── src/app/api/health/ # Health check endpoint
└── server/
    ├── Dockerfile          # Security-hardened FastAPI container
    └── src/main.py         # Includes /health endpoint
```

## 🔧 How File Sync Works

The configuration automatically syncs these file changes to running containers:

### Client (Next.js)
- `src/**/*.{js,jsx,ts,tsx,css,json}` → Hot reload
- `package.json` → Dependency changes
- `*.config.*` → Configuration updates

### Server (FastAPI)
- `src/**/*.py` → Code changes with uvicorn reload
- `requirements.txt` → Python dependency changes

## 🛠 Common Commands

```bash
# Check if configuration is valid
skaffold diagnose

# Build images without deploying
skaffold build

# Deploy without building (if images exist)
skaffold deploy

# Clean up deployment
skaffold delete

# Check deployment status
kubectl get pods -n metropolia-weather-map
kubectl get services -n metropolia-weather-map

# View logs
kubectl logs -f -n metropolia-weather-map deployment/nextjs-client
kubectl logs -f -n metropolia-weather-map deployment/fastapi-server
kubectl logs -f -n metropolia-weather-map deployment/postgres
```

## 📊 Health Checks

All services include health checks:

- **Frontend Health**: `http://localhost:3000/api/health`
- **Backend Health**: `http://localhost:8000/health`
- **Database**: Built-in `pg_isready` checks

## 🔍 Troubleshooting

### Common Issues

1. **"Cannot access Kubernetes cluster"**
   - Ensure Orbstack is running
   - Enable Kubernetes in Orbstack settings
   - Test with `kubectl cluster-info`

2. **"Skaffold not found"**
   ```bash
   brew install skaffold
   ```

3. **Port conflicts**
   - Ensure ports 3000, 8000, 5432 are not in use
   - Stop Docker Compose if running: `docker-compose down`

4. **Image build failures**
   - Check Dockerfile syntax
   - Ensure health endpoints exist
   - Review container logs

### Debug Commands

```bash
# Check pod status
kubectl get pods -n metropolia-weather-map

# Get detailed pod information
kubectl describe pod -n metropolia-weather-map <pod-name>

# View logs
kubectl logs -n metropolia-weather-map <pod-name>

# Access pod shell
kubectl exec -it -n metropolia-weather-map <pod-name> -- /bin/sh
```

## 🔄 Migration from Docker Compose

If you need to switch back to Docker Compose temporarily:

```bash
# Stop Skaffold (Ctrl+C in terminal)
skaffold delete

# Start Docker Compose
docker-compose up
```

## 🎉 Benefits Over Docker Compose

- **Production Parity**: Same deployment method as production
- **Kubernetes Features**: Health checks, resource limits, secrets
- **Security**: Non-root containers, proper isolation
- **Scalability**: Easy to add replicas, load balancers
- **Monitoring**: Better observability and debugging tools
- **Cloud Ready**: Same configuration works in cloud environments

## 📚 Next Steps

1. **Test the setup**: Run `./run-skaffold.sh` and verify all services work
2. **Customize profiles**: Modify `skaffold.yaml` profiles as needed
3. **Add monitoring**: Consider adding Prometheus/Grafana for metrics
4. **Production config**: Create production Kubernetes manifests
5. **CI/CD Integration**: Set up automated deployments

---

The setup preserves your familiar Docker Compose workflow while providing the power and production-readiness of Kubernetes. Happy developing! 🚀