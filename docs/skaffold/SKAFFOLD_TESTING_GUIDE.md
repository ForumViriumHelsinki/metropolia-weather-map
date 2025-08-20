# Skaffold Deployment Testing Guide

This guide provides comprehensive testing procedures for validating the Metropolia Weather Map Skaffold deployment before considering it production-ready.

## 📋 Overview

Our testing strategy validates 7 critical areas:
1. **Deployment Validation** - Services start successfully
2. **Connectivity Testing** - Service-to-service communication
3. **Health Check Validation** - Endpoint functionality
4. **Port Forwarding** - Localhost access
5. **Database Persistence** - Data survives restarts
6. **Performance Testing** - Resource usage validation
7. **Hot Reloading** - Development workflow preservation

## 🚀 Quick Start

### Prerequisites Check
```bash
# Verify environment health
./scripts/test-runner.sh health

# Check all systems
./scripts/test-runner.sh all
```

### Complete Validation Workflow
```bash
# 1. Start Skaffold development environment
skaffold dev

# 2. In another terminal, run validation tests
./scripts/test-runner.sh all

# 3. Run specific tests
./scripts/test-runner.sh performance
./scripts/test-runner.sh database
./scripts/test-runner.sh connectivity

# 4. Use Skaffold native testing profiles
skaffold test -p full-test
```

## 🔧 Testing Scripts Overview

### Current Test Runner
**File**: `/Users/lgates/repos/metropolia-weather-map/scripts/test-runner.sh`

**Purpose**: Modular test functions for Skaffold integration

**Usage**:
```bash
# Run all tests
./scripts/test-runner.sh all

# Run specific test functions
./scripts/test-runner.sh health          # Health checks
./scripts/test-runner.sh database        # Database connectivity
./scripts/test-runner.sh api             # API endpoint validation
./scripts/test-runner.sh performance     # Basic performance tests  
./scripts/test-runner.sh connectivity    # Service connectivity
```

### Native Skaffold Testing
**Purpose**: Integrated testing with build/deploy workflow

**Usage**:
```bash
# Test profiles for different scenarios
skaffold test                    # Default tests
skaffold test -p quick-test      # Fast development tests
skaffold test -p full-test       # Comprehensive validation
skaffold test -p benchmark-test  # Performance testing

# Testing with verification
skaffold run -p full-test        # Deploy and test
skaffold verify                  # Post-deployment verification
```

### Legacy Scripts Status
The following scripts have been **removed** and replaced with the current approach:
- ❌ `validate-skaffold-deployment.sh` → Use `./scripts/test-runner.sh all`
- ❌ `performance-benchmark.sh` → Use `./scripts/test-runner.sh performance`  
- ❌ `quick-health-check.sh` → Use `./scripts/test-runner.sh health`
- ❌ `skaffold-dev.sh` → Use native `skaffold dev`

## 📊 Success Criteria

### Deployment Success Criteria
✅ **All Prerequisites Met**
- Skaffold, kubectl, Docker, curl, jq installed
- Kubernetes cluster accessible (Orbstack)
- Ports 3000, 8000, 5432 available

✅ **Deployment Health**
- All pods in `Running` state
- Deployments show `READY` (1/1)
- Services created with ClusterIP assigned
- No pods in error or crash states

✅ **Connectivity Validation**
- Internal service-to-service communication works
- Port forwarding accessible from localhost
- All health endpoints responding correctly

✅ **Performance Benchmarks**
- Next.js: < 2s initial load time
- FastAPI health: < 500ms response
- PostgreSQL startup: < 30s
- FastAPI startup: < 20s
- Next.js startup: < 40s

### Response Time Benchmarks

| Service | Endpoint | Expected Response Time |
|---------|----------|----------------------|
| Next.js | Frontend (/) | < 2.0 seconds |
| FastAPI | Health (/health) | < 0.5 seconds |
| Next.js | Health (/api/health) | < 0.5 seconds |
| PostgreSQL | Simple queries | < 1.0 second |

### Resource Usage Expectations

| Service | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|-------------|-----------|----------------|--------------|
| PostgreSQL | 250m | 500m | 256Mi | 512Mi |
| FastAPI | 100m | 500m | 128Mi | 256Mi |
| Next.js | 100m | 500m | 128Mi | 256Mi |

## 🔍 Detailed Test Procedures

### 1. Environment Setup Validation

**Automated**: `./scripts/test-runner.sh health`

**Manual Steps**:
```bash
# Verify tools
skaffold version
kubectl version --client
docker version

# Check cluster connection
kubectl cluster-info
kubectl get nodes

# Verify port availability
./scripts/skaffold-dev.sh ports
```

### 2. Deployment Validation

**Automated**: `./scripts/validate-skaffold-deployment.sh deployment`

**Manual Verification**:
```bash
# Check all resources
kubectl get all -n weather-map

# Monitor deployment progress
kubectl rollout status deployment/postgres -n weather-map
kubectl rollout status deployment/fastapi -n weather-map
kubectl rollout status deployment/nextjs -n weather-map

# Verify pod readiness
kubectl get pods -n weather-map -o wide
```

### 3. Service Connectivity Testing

**Automated**: `./scripts/validate-skaffold-deployment.sh connectivity`

**Manual Testing**:
```bash
# Test internal connectivity
kubectl run test-pod --image=curlimages/curl --rm -it --restart=Never -n weather-map -- sh

# Inside the test pod:
nc -z postgres-service 5432
curl http://fastapi-service:8000/health
curl http://nextjs-service:3000/api/health
```

### 4. Health Endpoint Validation

**Automated**: `./scripts/validate-skaffold-deployment.sh health`

**Manual Testing**:
```bash
# Test health endpoints via port forwarding
curl http://localhost:8000/health | jq
curl http://localhost:3000/api/health | jq

# Expected FastAPI response:
# {"status": "healthy", "service": "fastapi-server"}

# Expected Next.js response:
# {"status": "healthy", "service": "nextjs-client", "timestamp": "2025-01-13T..."}
```

### 5. Port Forwarding Validation

**Automated**: `./scripts/validate-skaffold-deployment.sh ports`

**Manual Testing**:
```bash
# Test each forwarded port
curl http://localhost:3000        # Next.js frontend
curl http://localhost:8000/health # FastAPI backend
nc -z localhost 5432             # PostgreSQL

# Open in browser
open http://localhost:3000
```

### 6. Database Persistence Testing

**Automated**: `./scripts/validate-skaffold-deployment.sh persistence`

**Manual Testing**:
```bash
# Connect to database
kubectl exec -it $(kubectl get pods -n weather-map -l app=postgres -o jsonpath='{.items[0].metadata.name}') -n weather-map -- psql -U postgres -d weatherdb

# Create test data
CREATE TABLE test_persistence (id SERIAL, data TEXT, created_at TIMESTAMP DEFAULT NOW());
INSERT INTO test_persistence (data) VALUES ('test_before_restart');
SELECT * FROM test_persistence;

# Restart PostgreSQL pod
kubectl delete pod -n weather-map -l app=postgres

# Wait for new pod and verify data
kubectl wait --for=condition=ready pod -n weather-map -l app=postgres --timeout=300s
kubectl exec -it $(kubectl get pods -n weather-map -l app=postgres -o jsonpath='{.items[0].metadata.name}') -n weather-map -- psql -U postgres -d weatherdb -c "SELECT * FROM test_persistence;"
```

### 7. Performance Testing

**Automated**: `./scripts/performance-benchmark.sh`

**Manual Performance Tests**:
```bash
# Response time testing
time curl http://localhost:3000
time curl http://localhost:8000/health

# Concurrent load testing
for i in {1..10}; do
  curl http://localhost:3000 &
done
wait

# Resource monitoring
kubectl top pods -n weather-map
kubectl top nodes
```

### 8. Hot Reloading Validation

**Manual Testing** (requires Skaffold dev mode):
```bash
# Start Skaffold dev mode
./scripts/skaffold-dev.sh dev

# Make a change to frontend
echo "/* Test change $(date) */" >> client/src/app/page.tsx

# Make a change to backend
echo "# Test change $(date)" >> server/src/main.py

# Observe Skaffold logs for file sync activity
# Verify changes appear without full rebuild
```

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

#### Pods Stuck in Pending
```bash
# Diagnose
kubectl describe pod <pod-name> -n weather-map
kubectl get events -n weather-map

# Common solutions
kubectl get pvc -n weather-map  # Check persistent volumes
kubectl describe nodes          # Check resource availability
```

#### Service Connectivity Issues
```bash
# Diagnose
kubectl get endpoints -n weather-map
kubectl get services -n weather-map -o wide

# Test DNS resolution
kubectl run debug --image=busybox --rm -it --restart=Never -n weather-map -- nslookup postgres-service
```

#### Port Forwarding Problems
```bash
# Kill conflicting processes
./scripts/skaffold-dev.sh reset

# Check port usage
lsof -i :3000,8000,5432

# Restart port forwarding
skaffold dev --port-forward
```

#### Database Connection Issues
```bash
# Check PostgreSQL logs
kubectl logs -n weather-map -l app=postgres

# Verify credentials
kubectl get secret postgres-secret -n weather-map -o yaml

# Test connection
kubectl exec -it <postgres-pod> -n weather-map -- pg_isready -U postgres
```

### Performance Issues

#### High Response Times
```bash
# Monitor resource usage
kubectl top pods -n weather-map
kubectl describe pods -n weather-map

# Check application logs
kubectl logs -n weather-map -l app=fastapi --tail=100
kubectl logs -n weather-map -l app=nextjs --tail=100
```

#### Memory/CPU Issues
```bash
# Check resource limits
kubectl describe pods -n weather-map

# Monitor over time
watch kubectl top pods -n weather-map

# Adjust resources if needed (edit k8s manifests)
```

## 📈 Performance Monitoring

### Continuous Monitoring Commands
```bash
# Watch pod status
kubectl get pods -n weather-map -w

# Follow application logs
kubectl logs -f -n weather-map -l app=fastapi
kubectl logs -f -n weather-map -l app=nextjs

# Monitor resource usage
watch kubectl top pods -n weather-map

# Check events continuously
kubectl get events -n weather-map -w
```

### Setting Up Alerts
```bash
# Monitor for pod restarts
kubectl get pods -n weather-map --watch-only | grep -E "(Restarting|Error|CrashLoopBackOff)"

# Monitor resource usage
while true; do
  kubectl top pods -n weather-map | awk 'NR>1 && $3+0 > 80 {print "High CPU: " $0}'
  sleep 30
done
```

## 🔄 Continuous Integration

### Automated Testing in CI/CD
```bash
# Test profile for CI
./scripts/skaffold-dev.sh test

# Validation script in CI
./scripts/validate-skaffold-deployment.sh

# Performance baseline in CI
./scripts/performance-benchmark.sh
```

### Pre-Production Checklist
- [ ] All validation tests pass
- [ ] Performance benchmarks within limits
- [ ] Database persistence confirmed
- [ ] Hot reloading functional
- [ ] No error events in last 24 hours
- [ ] Resource usage stable
- [ ] Health checks responding correctly

## 📝 Next Steps

After successful validation:

1. **Production Preparation**
   - Review security configurations
   - Set up monitoring and alerting
   - Plan backup and disaster recovery
   - Configure production secrets

2. **Documentation Updates**
   - Update deployment procedures
   - Create runbooks for operations
   - Document troubleshooting procedures
   - Set up team training materials

3. **Continuous Improvement**
   - Set up performance monitoring
   - Establish SLA/SLO metrics
   - Plan capacity scaling procedures
   - Create automated health checks

## 🎯 Summary

This comprehensive testing strategy ensures your Skaffold deployment is:
- ✅ **Reliable**: All services start and communicate correctly
- ✅ **Performant**: Response times meet development requirements
- ✅ **Persistent**: Data survives infrastructure changes
- ✅ **Developer-Friendly**: Hot reloading and development workflow preserved
- ✅ **Monitorable**: Health checks and logging functional
- ✅ **Troubleshootable**: Clear procedures for common issues

The deployment is ready for development use and provides a solid foundation for production planning.