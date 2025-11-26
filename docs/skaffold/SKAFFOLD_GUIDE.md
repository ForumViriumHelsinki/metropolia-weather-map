# Metropolia Weather Map - Skaffold Development Guide

This guide covers the production-ready Skaffold configuration for the Metropolia Weather Map project, optimized for Orbstack local development with Kubernetes.

## Architecture Overview

**3-Service Architecture:**
- **PostgreSQL**: Database with persistent storage
- **FastAPI**: Backend API server with Python
- **Next.js**: Frontend client with React

**Key Features:**
- ✅ Orbstack cluster compatibility with hot reloading
- ✅ Docker Compose-like development workflow
- ✅ Port forwarding for localhost access (3000, 8000, 5432)
- ✅ Security-hardened Dockerfiles with non-root users
- ✅ Health checks for all services
- ✅ Multiple profiles for different scenarios

## Quick Start

### Prerequisites
```bash
# Ensure you have these tools installed
skaffold version  # Should be v2.0+ 
kubectl version   # Should connect to your Orbstack cluster
docker version    # Should connect to Orbstack

# Verify Orbstack cluster is active
kubectl cluster-info
```

### Basic Development Workflow
```bash
# Start the full application (default profile)
skaffold dev

# Or explicitly use the dev profile
skaffold dev -p dev

# Access your application
open http://localhost:3000  # Next.js frontend
open http://localhost:8000  # FastAPI backend
# PostgreSQL available at localhost:5432
```

## Available Profiles

### 1. Default Profile (No flag needed)
**Usage:** `skaffold dev`
- Development-optimized build with hot reloading
- File sync for all source code changes
- Port forwarding for all services
- Non-root containers for security

### 2. Development Profile (`-p dev`)
**Usage:** `skaffold dev -p dev`
- Enhanced hot reloading with broader file sync
- Includes configuration files (*.config.*, *.json)
- Optimized for rapid iteration
- BuildKit enabled for faster builds

### 3. Production Profile (`-p prod`)
**Usage:** `skaffold dev -p prod`
- Uses production Dockerfiles (Dockerfile.prod)
- Multi-stage builds with optimized images
- No file sync (container rebuilds on changes)
- Production environment variables

### 4. Debug Profile (`-p debug`)
**Usage:** `skaffold dev -p debug`
- Verbose logging with pod prefixes
- Enhanced monitoring capabilities
- All development features enabled
- Activate with: `SKAFFOLD_PROFILE=debug skaffold dev`

### 5. Database Only Profile (`-p db-only`)
**Usage:** `skaffold dev -p db-only`
- Only deploys PostgreSQL
- Useful for database development/migrations
- Direct access via localhost:5432
- Minimal resource usage

### 6. Testing Profile (`-p test`)
**Usage:** `CI=true skaffold dev -p test`
- Optimized for CI/CD environments
- Extended timeouts for reliable deployments
- Uses production builds
- Health checks with proper wait conditions

## Development Workflow

### Hot Reloading
File changes are automatically synced to containers:

**Next.js (Frontend):**
- `src/**/*` → Live reload in browser
- `public/**/*` → Static assets updated
- `package.json`, `pnpm-lock.yaml` → Dependencies updated
- Configuration files → Settings applied

**FastAPI (Backend):**
- `src/**/*.py` → Uvicorn auto-reload
- `requirements.txt` → Dependencies updated
- `ruff.toml` → Linting configuration updated

### Port Access
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: postgresql://localhost:5432
- **Health Checks**: 
  - http://localhost:3000/api/health
  - http://localhost:8000/health

### Common Commands

```bash
# Full development environment
skaffold dev

# Run with specific profile
skaffold dev -p prod

# Deploy without file watching
skaffold run

# Build images only
skaffold build

# Delete deployed resources
skaffold delete

# Tail logs from all pods
skaffold dev --tail

# Deploy with custom namespace
skaffold dev --namespace custom-weather-map
```

## Advanced Configuration

### Build Optimization
- **BuildKit enabled**: Faster, more efficient builds
- **Layer caching**: Previous builds cached for speed
- **Multi-stage builds**: Optimized production images
- **Security scanning**: Non-root users in all containers

### Health Monitoring
All services include health checks:
- **PostgreSQL**: `pg_isready` command
- **FastAPI**: `/health` endpoint
- **Next.js**: `/api/health` endpoint

### Resource Management
Default resource limits per service:
- **PostgreSQL**: 256Mi-512Mi RAM, 250m-500m CPU
- **FastAPI**: Configurable based on requirements.txt
- **Next.js**: Configurable based on build size

## File Structure

```
metropolia-weather-map/
├── skaffold.yaml           # Main Skaffold configuration
├── k8s/                    # Kubernetes manifests
│   ├── namespace.yaml
│   ├── postgres-*.yaml     # Database configuration
│   ├── fastapi-*.yaml      # Backend configuration
│   └── nextjs-*.yaml       # Frontend configuration
├── client/                 # Next.js application
│   ├── Dockerfile          # Development build
│   ├── Dockerfile.prod     # Production build
│   └── src/                # Source code
├── server/                 # FastAPI application
│   ├── Dockerfile          # Development build
│   ├── Dockerfile.prod     # Production build
│   └── src/                # Source code
└── data/                   # Initial data and SQL scripts
```

## Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Find and kill processes using ports
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
lsof -ti:5432 | xargs kill -9
```

**2. Image Build Failures**
```bash
# Clean Docker cache
docker system prune -a
# Rebuild without cache
skaffold dev --no-prune=false --cache-artifacts=false
```

**3. Kubernetes Connection Issues**
```bash
# Verify cluster connection
kubectl cluster-info
# Check namespace
kubectl get ns weather-map
# Check pod status
kubectl get pods -n metropolia-weather-map
```

**4. File Sync Not Working**
- Ensure files are within sync paths defined in skaffold.yaml
- Check file permissions (should be readable by non-root user)
- Verify containers are running: `kubectl get pods -n metropolia-weather-map`

### Logs and Debugging

```bash
# View all logs
skaffold dev --tail

# View specific service logs
kubectl logs -n metropolia-weather-map deployment/nextjs
kubectl logs -n metropolia-weather-map deployment/fastapi
kubectl logs -n metropolia-weather-map deployment/postgres

# Debug mode with verbose output
skaffold dev -v debug

# Check resource status
kubectl get all -n metropolia-weather-map
```

## Security Features

### Container Security
- **Non-root users**: All containers run as unprivileged users
- **Read-only filesystem**: Where applicable
- **Minimal base images**: Alpine Linux for reduced attack surface
- **Health checks**: Built-in monitoring for all services

### Network Security
- **Namespace isolation**: Services isolated in weather-map namespace
- **Service-to-service communication**: Internal cluster networking
- **Port forwarding**: Localhost-only access for development

## Performance Optimization

### Build Performance
- **BuildKit**: Enabled for parallel builds and improved caching
- **Layer caching**: Reuses unchanged layers
- **Multi-stage builds**: Smaller final images
- **Dependency caching**: Node modules and Python packages cached

### Runtime Performance
- **Resource limits**: Prevents resource starvation
- **Health checks**: Quick failure detection and recovery
- **Persistent volumes**: Database data persists across restarts

## Migration from Docker Compose

If migrating from docker-compose, here are the key differences:

### Similarities Preserved
- **Same ports**: 3000, 8000, 5432
- **Same environment**: Development experience maintained
- **Same data**: Database data persists
- **Hot reloading**: File changes reflected immediately

### Kubernetes Advantages
- **Better resource management**: CPU/memory limits
- **Health monitoring**: Automatic restart on failures
- **Service discovery**: Reliable inter-service communication
- **Scalability**: Can easily scale services
- **Production parity**: Same orchestration as production

## CI/CD Integration

The testing profile (`-p test`) is designed for CI/CD pipelines:

```yaml
# Example GitHub Actions usage
- name: Test Skaffold deployment
  run: |
    export CI=true
    skaffold run -p test
    # Run tests
    skaffold delete -p test
```

This configuration provides a robust, production-ready development environment that maintains the simplicity of Docker Compose while providing the power and scalability of Kubernetes.