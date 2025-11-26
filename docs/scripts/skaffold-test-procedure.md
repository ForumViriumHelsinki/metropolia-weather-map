# Skaffold Deployment Testing Strategy

This document provides a comprehensive testing strategy for validating the Metropolia Weather Map Skaffold deployment. The strategy ensures all components work correctly before considering the deployment production-ready.

## Overview

The testing strategy validates:
- **Deployment Validation**: All services start successfully
- **Connectivity Testing**: Service-to-service communication works
- **Hot Reloading Validation**: File sync functionality operates correctly
- **Port Forwarding Testing**: Localhost access is functional
- **Database Persistence**: Data survives pod restarts
- **Health Check Validation**: Health endpoints respond correctly
- **Performance Testing**: Resource usage is within expected bounds

## Quick Start

### Prerequisites
- Orbstack with Kubernetes enabled
- Skaffold installed
- kubectl configured for your cluster
- curl and jq installed

### Run Complete Validation
```bash
# Navigate to project root
cd /Users/lgates/repos/metropolia-weather-map

# Start Skaffold development environment
skaffold dev

# In another terminal, run validation tests
./scripts/test-runner.sh all

# Or use Skaffold test profiles
skaffold test -p full-test
```

## Detailed Testing Procedures

### 1. Environment Setup Validation

**Objective**: Ensure all prerequisites are met before testing

**Steps**:
1. Verify tool installation and health:
   ```bash
   ./scripts/test-runner.sh health
   ```

2. Check cluster connectivity:
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

3. Verify port availability:
   ```bash
   lsof -i :3000,8000,5432
   ```

**Success Criteria**:
- All required tools are installed and accessible
- Kubernetes cluster is reachable
- Required ports (3000, 8000, 5432) are available

### 2. Deployment Validation

**Objective**: Verify all services deploy and reach ready state

**Automated Test**:
```bash
./scripts/test-runner.sh connectivity
```

**Manual Verification**:
```bash
# Check namespace creation
kubectl get namespace weather-map

# Verify all deployments are ready
kubectl get deployments -n metropolia-weather-map

# Check pod status
kubectl get pods -n metropolia-weather-map -o wide

# Monitor deployment progress
kubectl rollout status deployment/postgres -n metropolia-weather-map
kubectl rollout status deployment/fastapi -n metropolia-weather-map
kubectl rollout status deployment/nextjs -n metropolia-weather-map
```

**Success Criteria**:
- Namespace `weather-map` exists
- All deployments show `READY` status
- All pods are in `Running` state
- Replica counts match desired state

### 3. Service Connectivity Testing

**Objective**: Validate internal service-to-service communication

**Automated Test**:
```bash
./scripts/test-runner.sh connectivity
```

**Manual Verification**:
```bash
# Check service creation
kubectl get services -n metropolia-weather-map

# Test internal connectivity using a debug pod
kubectl run debug-pod --image=curlimages/curl:latest --rm -it --restart=Never -n metropolia-weather-map -- sh

# Inside the debug pod:
# Test PostgreSQL connectivity
nc -z postgres-service 5432

# Test FastAPI health endpoint
curl http://fastapi-service:8000/health

# Test Next.js health endpoint
curl http://nextjs-service:3000/api/health
```

**Success Criteria**:
- All services are created and have ClusterIP assigned
- PostgreSQL accepts connections on port 5432
- FastAPI health endpoint responds with `{"status": "healthy"}`
- Next.js health endpoint responds with `{"status": "healthy"}`

### 4. Health Check Validation

**Objective**: Verify application health endpoints function correctly

**Automated Test**:
```bash
./scripts/test-runner.sh api
```

**Manual Verification**:
```bash
# Test FastAPI health endpoint via port forward
curl http://localhost:8000/health | jq

# Expected response:
# {
#   "status": "healthy",
#   "service": "fastapi-server"
# }

# Test Next.js health endpoint
curl http://localhost:3000/api/health | jq

# Expected response:
# {
#   "status": "healthy",
#   "service": "nextjs-client",
#   "timestamp": "2025-01-13T09:30:00.000Z"
# }
```

**Success Criteria**:
- FastAPI health endpoint returns expected JSON structure
- Next.js health endpoint returns expected JSON structure
- Both endpoints respond within reasonable time (< 5 seconds)

### 5. Port Forwarding Testing

**Objective**: Confirm localhost access to all services

**Automated Test**:
```bash
./scripts/test-runner.sh api
```

**Manual Verification**:
```bash
# Check port forwarding status
kubectl get services -n metropolia-weather-map

# Test each port
curl http://localhost:3000  # Next.js frontend
curl http://localhost:8000/health  # FastAPI backend
nc -z localhost 5432  # PostgreSQL database

# Test application functionality
open http://localhost:3000  # Should show the weather map application
```

**Success Criteria**:
- Port 3000 serves Next.js application
- Port 8000 serves FastAPI application
- Port 5432 accepts PostgreSQL connections
- Applications are fully functional via localhost

### 6. Database Persistence Testing

**Objective**: Validate data survives pod restarts

**Automated Test**:
```bash
./scripts/test-runner.sh database
```

**Manual Verification**:
```bash
# Connect to database and create test data
kubectl exec -it $(kubectl get pods -n metropolia-weather-map -l app=postgres -o jsonpath='{.items[0].metadata.name}') -n metropolia-weather-map -- psql -U postgres -d weatherdb

-- Inside PostgreSQL:
CREATE TABLE test_persistence (id SERIAL, data TEXT, created_at TIMESTAMP DEFAULT NOW());
INSERT INTO test_persistence (data) VALUES ('test_data_' || extract(epoch from now()));
SELECT * FROM test_persistence;
\q

# Restart PostgreSQL pod
kubectl delete pod -n metropolia-weather-map -l app=postgres

# Wait for new pod to be ready
kubectl wait --for=condition=ready pod -n metropolia-weather-map -l app=postgres --timeout=300s

# Verify data persistence
kubectl exec -it $(kubectl get pods -n metropolia-weather-map -l app=postgres -o jsonpath='{.items[0].metadata.name}') -n metropolia-weather-map -- psql -U postgres -d weatherdb -c "SELECT * FROM test_persistence;"
```

**Success Criteria**:
- Test data can be inserted into database
- Data survives pod restart
- Database connections work after restart
- No data corruption occurs

### 7. Performance and Resource Usage Testing

**Objective**: Validate resource usage is within acceptable bounds

**Automated Test**:
```bash
./scripts/test-runner.sh performance
```

**Manual Verification**:
```bash
# Check resource usage (requires metrics-server)
kubectl top pods -n metropolia-weather-map
kubectl top nodes

# Check resource requests and limits
kubectl describe pods -n metropolia-weather-map

# Monitor for a period
watch kubectl get pods -n metropolia-weather-map
```

**Success Criteria**:
- No pods are in `CrashLoopBackOff` or `Error` state
- Memory usage is within configured limits
- CPU usage is reasonable for development workload
- No excessive pod restarts

### 8. Hot Reloading Validation

**Objective**: Test file synchronization and hot reloading

**Manual Test Procedure**:
1. Start Skaffold in development mode:
   ```bash
   skaffold dev
   ```

2. Make a visible change to the frontend:
   ```bash
   # Edit a React component
   echo "// Test change $(date)" >> client/src/app/page.tsx
   ```

3. Observe Skaffold logs for file sync activity

4. Verify the change appears in the browser without rebuilding

5. Make a change to the backend:
   ```bash
   # Edit a Python file
   echo "# Test change $(date)" >> server/src/main.py
   ```

6. Observe backend restart and verify functionality

**Success Criteria**:
- Skaffold detects file changes within 5 seconds
- Frontend changes sync without container rebuild
- Backend changes trigger container restart
- Applications remain functional after changes

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Pods Stuck in Pending State

**Symptoms**: Pods show `Pending` status for extended periods

**Diagnosis**:
```bash
kubectl describe pod <pod-name> -n metropolia-weather-map
kubectl get events -n metropolia-weather-map
```

**Solutions**:
- Check resource availability: `kubectl describe nodes`
- Verify persistent volume claims: `kubectl get pvc -n metropolia-weather-map`
- Check image pull issues: `docker images | grep weather-map`

#### 2. Service Connectivity Issues

**Symptoms**: Services cannot reach each other

**Diagnosis**:
```bash
kubectl get endpoints -n metropolia-weather-map
kubectl get services -n metropolia-weather-map -o wide
```

**Solutions**:
- Verify service selectors match pod labels
- Check network policies: `kubectl get networkpolicies -n metropolia-weather-map`
- Test DNS resolution from inside pods

#### 3. Health Check Failures

**Symptoms**: Health endpoints return errors or timeouts

**Diagnosis**:
```bash
kubectl logs <pod-name> -n metropolia-weather-map
curl -v http://localhost:8000/health
```

**Solutions**:
- Check application startup logs
- Verify environment variables: `kubectl get configmap -n metropolia-weather-map -o yaml`
- Test endpoints directly from pods

#### 4. Port Forwarding Issues

**Symptoms**: Cannot access services via localhost

**Diagnosis**:
```bash
kubectl get services -n metropolia-weather-map
lsof -i :3000,8000,5432
```

**Solutions**:
- Kill conflicting processes: `lsof -ti :3000,8000,5432 | xargs kill`
- Check Skaffold port forwarding configuration
- Verify service ports match skaffold.yaml

#### 5. Database Connection Problems

**Symptoms**: Applications cannot connect to PostgreSQL

**Diagnosis**:
```bash
kubectl logs <postgres-pod> -n metropolia-weather-map
kubectl exec -it <postgres-pod> -n metropolia-weather-map -- pg_isready
```

**Solutions**:
- Check PostgreSQL logs for startup errors
- Verify database credentials in secrets
- Test connection from application pods

#### 6. File Sync Not Working

**Symptoms**: Code changes don't reflect in running containers

**Diagnosis**:
```bash
# Check Skaffold logs for sync activity
skaffold dev -v info
```

**Solutions**:
- Verify file paths in skaffold.yaml sync configuration
- Check file permissions on host system
- Restart Skaffold development session

## Performance Benchmarks

### Expected Resource Usage (Development Environment)

| Service | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|-------------|-----------|----------------|--------------|
| PostgreSQL | 250m | 500m | 256Mi | 512Mi |
| FastAPI | 100m | 500m | 128Mi | 256Mi |
| Next.js | 100m | 500m | 128Mi | 256Mi |

### Expected Response Times

| Endpoint | Expected Response Time |
|----------|----------------------|
| Next.js Frontend | < 2 seconds (initial load) |
| FastAPI Health | < 500ms |
| Next.js Health | < 500ms |
| Database Queries | < 1 second (simple queries) |

### Startup Times

| Service | Expected Startup Time |
|---------|----------------------|
| PostgreSQL | 15-30 seconds |
| FastAPI | 10-20 seconds |
| Next.js | 20-40 seconds |

## Success Criteria Summary

A successful Skaffold deployment validation requires:

✅ **All Prerequisites Met**
- Required tools installed and functional
- Kubernetes cluster accessible
- Required ports available

✅ **Successful Deployment**
- All pods reach `Running` state
- Deployments show `READY` status
- Services are created and accessible

✅ **Working Connectivity**
- Internal service-to-service communication
- External access via port forwarding
- Health endpoints responding correctly

✅ **Data Persistence**
- Database operations work correctly
- Data survives pod restarts
- No data corruption

✅ **Acceptable Performance**
- Resource usage within limits
- Response times meet benchmarks
- No excessive restarts or errors

✅ **Development Features**
- Hot reloading functional
- File sync working correctly
- Development workflow preserved

## Next Steps

After successful validation:

1. **Document any environment-specific configurations**
2. **Create monitoring and alerting for production deployment**
3. **Establish backup and disaster recovery procedures**
4. **Plan production security hardening**
5. **Set up CI/CD integration with validation tests**

This comprehensive testing strategy ensures the Skaffold deployment is robust, reliable, and ready for development use while providing a foundation for production deployment planning.