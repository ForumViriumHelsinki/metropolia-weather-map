# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Metropolia Weather Map (Visio) is a full-stack web application that visualizes temperature changes on a map using sensor data. The application fetches data from local sensors and nearby weather stations, storing everything in a PostgreSQL database hosted on Google Cloud.

**Tech Stack:**
- **Frontend**: Next.js 15 with React 19, TypeScript, Leaflet maps
- **Backend**: FastAPI (Python) with asyncpg for database access
- **Database**: PostgreSQL 15
- **Orchestration**: Kubernetes via Skaffold, Docker containers
- **GitOps**: Prepared for deployment via ~/repos/infrastructure ArgoCD pipeline

## Development Commands

### Local Development with Skaffold (Primary Method)

```bash
# Start full development environment with hot reloading
skaffold dev

# Development with enhanced file sync
skaffold dev -p dev

# Run with quick health checks
skaffold dev -p quick-test

# Database only (for migrations/testing)
skaffold dev -p db-only

# Production mode (no file sync)
skaffold dev -p prod

# Debug mode with verbose logging
skaffold dev -p debug
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Database: postgresql://postgres:pass@localhost:5432/weatherdb

### Testing

```bash
# Run all tests
skaffold test

# Quick health checks and linting
skaffold test -p quick-test

# Comprehensive test suite with coverage
skaffold run -p full-test

# Performance benchmarks
skaffold run -p benchmark-test

# Post-deployment verification
skaffold verify

# Backend tests (Python/pytest)
cd server && python -m pytest src/tests/ -v

# Frontend tests (Next.js/Jest)
cd client && npm test -- --watchAll=false

# Single test file
cd client && npm test -- path/to/test.test.tsx
```

### Building and Deployment

```bash
# Build all images
skaffold build

# Force rebuild without cache
skaffold build --no-prune=false --cache-artifacts=false

# Deploy to cluster
skaffold run

# Delete all deployed resources
skaffold delete
```

### Linting and Formatting

```bash
# Frontend linting
cd client && npm run lint

# Backend linting (ruff)
cd server && ruff check src/

# Format backend code
cd server && ruff format src/
```

### Database Operations

```bash
# Access PostgreSQL shell (when running in Skaffold)
kubectl exec -it deployment/postgres -n metropolia-weather-map -- psql -U postgres -d weatherdb

# Initialize database (legacy Docker Compose method)
py ./server/src/api/sql/populate_db.py
```

### Kubernetes Debugging

```bash
# Check pod status
kubectl get pods -n metropolia-weather-map

# View logs
kubectl logs -f deployment/nextjs-client -n metropolia-weather-map
kubectl logs -f deployment/fastapi-server -n metropolia-weather-map
kubectl logs -f deployment/postgres -n metropolia-weather-map

# Describe resources
kubectl describe pod <pod-name> -n metropolia-weather-map

# Access pod shell
kubectl exec -it deployment/fastapi-server -n metropolia-weather-map -- /bin/bash
```

## Architecture

### Service Architecture

The application follows a 3-tier architecture deployed on Kubernetes:

1. **Next.js Frontend (client/)**
   - App Router architecture (`src/app/`)
   - API routes in `src/app/api/` (health checks)
   - Map visualization with React-Leaflet
   - Tag management and sensor data visualization

2. **FastAPI Backend (server/)**
   - Main app: `src/main.py`
   - API routes: `src/api/routes/`
     - `sensors.py` - Sensor CRUD operations
     - `tags.py` - Tag management
     - `sensor_tags.py` - Sensor-tag associations
     - `analysis.py` - Data analysis endpoints
     - `graph_routes.py` - Graph visualization
   - Database models and utilities: `src/utils/`
   - Analysis tools: `src/analysis/`

3. **PostgreSQL Database**
   - Persistent storage via PVC
   - Initialization scripts in ConfigMap
   - PostGIS extension for geospatial data

### Kubernetes Resources (k8s/)

- **namespace.yaml** - `weather-map` namespace
- **Deployments**: `{nextjs,fastapi,postgres}-deployment.yaml`
- **Services**: `{nextjs,fastapi,postgres}-service.yaml`
- **ConfigMaps**: `{nextjs,fastapi,postgres}-configmap.yaml`
- **Secrets**: `{nextjs,fastapi,postgres}-secret.yaml`
- **Storage**: `postgres-pvc.yaml` for persistent data

### File Synchronization (Hot Reloading)

Skaffold automatically syncs changes without rebuilding:

**Frontend:**
- `src/**/*` → All source files (TS, TSX, CSS, JSON) auto-reload
- `package.json` → Dependency updates (requires rebuild)

**Backend:**
- `src/**/*.py` → All Python files auto-reload via Uvicorn
- `requirements.txt` → Dependency updates (requires rebuild)

### Environment Configuration

**Backend (FastAPI):**
- `DB_HOST`: postgres-service (internal K8s DNS)
- `DB_NAME`: weatherdb
- `DB_USER`: postgres
- `DB_PASS`: Stored in fastapi-secret

**Frontend (Next.js):**
- `NEXT_PUBLIC_PYTHON_API`: http://fastapi-service:8000 (internal)
- `NEXT_PUBLIC_CLIENT_API`: http://localhost:8000 (browser)

## Skaffold Profiles

- **default** - Standard development with hot reloading
- **dev** - Enhanced sync including config files
- **prod** - Production builds using Dockerfile.prod
- **debug** - Verbose logging with pod prefixes
- **db-only** - PostgreSQL only for database work
- **quick-test** - Fast health checks for development
- **full-test** - Comprehensive testing with coverage
- **benchmark-test** - Performance and load testing

## GitOps Integration Status

The project is configured for GitOps deployment via the ~/repos/infrastructure repository:

**Current State:**
- Kubernetes manifests in `k8s/` ready for ArgoCD
- Skaffold configuration complete with testing infrastructure
- Dockerfiles have both dev and prod variants
- Health checks configured on all services
- Namespace: `weather-map`
- Default container registry: `ghcr.io/forumviriumhelsinki`

**Next Steps for GitOps:**
1. Add application manifest to ~/repos/infrastructure/argocd/
2. Configure CI/CD pipeline to build and push images to GHCR
3. Update image pull settings in k8s manifests to use GHCR
4. Configure environment-specific overlays (dev/staging/prod)
5. Set up GHCR authentication in the cluster

## Health Checks

All services expose health endpoints:
- Next.js: `GET /api/health` → `{status: "healthy"}`
- FastAPI: `GET /health` → `{status: "healthy", service: "fastapi-server"}`
- PostgreSQL: `pg_isready` liveness/readiness probes

## Resource Limits

Default Kubernetes resource configuration per service:
- **Requests**: 250m CPU, 256Mi memory
- **Limits**: 500m CPU, 512Mi memory

## Security

- All production containers run as non-root users
- Secrets managed via Kubernetes Secrets
- Health checks for automatic recovery
- Namespace isolation (`weather-map`)
- ConfigMaps for non-sensitive configuration

## Common Workflows

### Making Frontend Changes
1. Edit files in `client/src/`
2. Skaffold auto-syncs → Next.js hot reloads
3. View changes at http://localhost:3000

### Making Backend Changes
1. Edit files in `server/src/`
2. Skaffold auto-syncs → Uvicorn reloads
3. Test at http://localhost:8000

### Adding New API Routes
1. Create route file in `server/src/api/routes/`
2. Import and include router in `server/src/main.py`
3. Skaffold syncs automatically

### Database Schema Changes
1. Update schema in database init scripts
2. Delete deployment: `skaffold delete`
3. Redeploy: `skaffold dev`

### Troubleshooting Deployment
1. Check pod status: `kubectl get pods -n metropolia-weather-map`
2. View logs: `kubectl logs -f deployment/<service> -n metropolia-weather-map`
3. Describe issues: `kubectl describe pod <pod-name> -n metropolia-weather-map`
4. Force rebuild: `skaffold dev --force-build`

## Documentation

Key documentation files:
- `README.md` - Project overview and quick start
- `docs/skaffold/SKAFFOLD_GUIDE.md` - Comprehensive Skaffold usage
- `docs/skaffold/TESTING_GUIDE.md` - Testing infrastructure details
- `docs/skaffold/SKAFFOLD_SETUP.md` - Initial setup guide
