# Skaffold Configuration for Weather Map Project

This document provides comprehensive guidance for using Skaffold to develop and deploy the Metropolia Weather Map project on Kubernetes with Orbstack.

## Architecture Overview

The project consists of three main services:
- **PostgreSQL Database** - Weather sensor data storage
- **FastAPI Server** - Python backend API (`localhost:8000`)
- **Next.js Client** - React frontend (`localhost:3000`)

## Prerequisites

1. **Orbstack** installed and running
2. **Kubernetes cluster** configured (Orbstack provides this)
3. **Skaffold** installed (`brew install skaffold`)
4. **kubectl** configured to point to your Orbstack cluster

### Verify Prerequisites

```bash
# Check if kubectl is configured
kubectl cluster-info

# Check if Skaffold is installed
skaffold version

# Verify Orbstack is running
docker context list
```

## Quick Start

### 1. Initial Setup

```bash
# Navigate to project root
cd /path/to/metropolia-weather-map

# Create namespace and deploy all services
skaffold run
```

### 2. Development Mode

```bash
# Start development with hot reloading
skaffold dev

# Or use the explicit dev profile
skaffold dev -p dev
```

### 3. Access Services

Once deployed, services are available at:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **Database**: localhost:5432 (username: postgres, password: pass)

## Available Profiles

### Default Profile (Development)
```bash
skaffold dev
```
- Uses development Dockerfiles
- Enables file synchronization for hot reloading
- Includes port forwarding

### Production Profile
```bash
skaffold dev -p prod
```
- Uses production Dockerfiles with security hardening
- Multi-stage builds for optimized images
- No file sync (immutable deployments)

### Debug Profile
```bash
skaffold dev -p debug
```
- Enhanced logging and debugging features
- Extended port forwarding configuration
- Additional development tools

## File Synchronization

Skaffold automatically syncs file changes to running containers:

### Next.js Client
- `src/**/*` → Auto-reload on code changes
- `public/**/*` → Static asset updates
- `package.json` → Dependency updates (requires restart)
- Config files → Configuration changes

### FastAPI Server
- `src/**/*.py` → Auto-reload on Python code changes
- `requirements.txt` → Dependency updates (requires rebuild)

## Service Configuration

### Environment Variables

**FastAPI Server:**
- `DB_HOST`: postgres-service
- `DB_NAME`: weatherdb
- `DB_USER`: postgres
- `DB_PASS`: pass (from secret)

**Next.js Client:**
- `NEXT_PUBLIC_PYTHON_API`: http://fastapi-service:8000
- `NEXT_PUBLIC_CLIENT_API`: http://localhost:8000

### Health Checks

All services include health check endpoints:
- **Next.js**: `/api/health`
- **FastAPI**: `/health`
- **PostgreSQL**: Built-in `pg_isready`

## Database Initialization

The PostgreSQL service automatically initializes with:
- Weather database schema
- Sensor location data
- Tag classifications (green/gray spaces, sun/shade, coastal/continental)

## Troubleshooting

### Common Issues

1. **Orbstack not running**
   ```bash
   # Start Orbstack
   open -a OrbStack
   ```

2. **Port conflicts**
   ```bash
   # Check what's using the ports
   lsof -i :3000
   lsof -i :8000
   lsof -i :5432
   ```

3. **Image build failures**
   ```bash
   # Force rebuild all images
   skaffold run --force-build
   ```

4. **Sync not working**
   ```bash
   # Check Skaffold logs
   skaffold dev -v info
   ```

### Debug Commands

```bash
# Check pod status
kubectl get pods -n metropolia-weather-map

# View pod logs
kubectl logs -f deployment/nextjs-client -n metropolia-weather-map
kubectl logs -f deployment/fastapi-server -n metropolia-weather-map
kubectl logs -f deployment/postgres -n metropolia-weather-map

# Describe pod issues
kubectl describe pod <pod-name> -n metropolia-weather-map

# Access pod shell
kubectl exec -it deployment/fastapi-server -n metropolia-weather-map -- /bin/bash
```

### Clean Restart

```bash
# Delete everything and restart
skaffold delete
skaffold run
```

## Production Deployment

For production deployment, use the prod profile:

```bash
# Build production images
skaffold build -p prod

# Deploy to production (adjust manifests for prod environment)
skaffold deploy -p prod
```

## Security Considerations

### Development vs Production

**Development:**
- Uses development Dockerfiles with root users for convenience
- File sync enabled for rapid iteration
- Debug logging enabled

**Production:**
- Non-root users in containers
- Multi-stage builds for smaller images
- Health checks and resource limits
- Secrets managed via Kubernetes secrets

### Secrets Management

Currently uses basic secrets for development. For production:
1. Use external secret management (Vault, etc.)
2. Implement proper RBAC
3. Use TLS for inter-service communication

## Performance Optimization

### Resource Limits

Current resource limits are conservative:
- **CPU**: 250m requests, 500m limits
- **Memory**: 256Mi requests, 512Mi limits

Adjust based on your system capabilities and requirements.

### Build Optimization

1. **Layer caching**: Dockerfiles are optimized for layer reuse
2. **Sync over rebuild**: File sync prevents unnecessary rebuilds
3. **Multi-stage builds**: Production images are optimized

## Integration with Existing Workflow

This Skaffold setup maintains compatibility with your existing Docker Compose workflow:

- **Same environment variables**
- **Same port mappings**
- **Same database initialization**
- **Same development experience**

You can still use Docker Compose for simple testing, but Skaffold provides:
- **Better development experience** with file sync
- **Production-ready deployment patterns**
- **Kubernetes-native development**
- **Easy scaling and service mesh integration**

## Advanced Features

### Custom Build Arguments

```bash
# Pass custom build arguments
skaffold dev --build-arg NODE_ENV=staging
```

### Multiple Environment Support

Extend profiles for different environments:
- `dev` - Local development
- `staging` - Staging environment
- `prod` - Production environment

### Integration with CI/CD

The Skaffold configuration can be integrated with CI/CD pipelines:

```bash
# Build and test
skaffold build --file-output=artifacts.json
skaffold test --build-artifacts=artifacts.json

# Deploy
skaffold deploy --build-artifacts=artifacts.json
```

## Next Steps

1. **Monitoring**: Add Prometheus/Grafana for observability
2. **Service Mesh**: Consider Istio for advanced traffic management
3. **GitOps**: Integrate with ArgoCD or Flux for GitOps workflows
4. **Security**: Implement Pod Security Standards and Network Policies
5. **Scaling**: Configure Horizontal Pod Autoscaler (HPA)