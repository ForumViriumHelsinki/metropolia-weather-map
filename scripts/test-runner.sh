#!/bin/bash

# Metropolia Weather Map - Modular Test Runner for Skaffold
# This script provides modular test functions that can be called individually
# by Skaffold test configurations or used in CI/CD pipelines

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE="weather-map"

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Health check test - equivalent to quick-health-check.sh
test_health_check() {
    log_info "Running health check tests..."
    
    # Check if namespace exists
    if ! kubectl get namespace "$NAMESPACE" &>/dev/null; then
        log_error "Namespace '$NAMESPACE' not found"
        return 1
    fi
    
    # Check pod status
    local running_pods=$(kubectl get pods -n "$NAMESPACE" --no-headers 2>/dev/null | grep -c "Running" || echo "0")
    local total_pods=$(kubectl get pods -n "$NAMESPACE" --no-headers 2>/dev/null | wc -l || echo "0")
    
    if [ "$running_pods" -eq "$total_pods" ] && [ "$total_pods" -gt 0 ]; then
        log_success "All pods are running ($running_pods/$total_pods)"
    else
        log_error "Not all pods are running ($running_pods/$total_pods)"
        return 1
    fi
    
    # Test service endpoints if port forwarding is available
    local services=(3000 8000)
    for port in "${services[@]}"; do
        if nc -z localhost "$port" 2>/dev/null; then
            log_success "Port $port is accessible"
        else
            log_warning "Port $port is not accessible (port forwarding may not be active)"
        fi
    done
    
    log_success "Health check completed successfully"
}

# Database connectivity test
test_database_connectivity() {
    log_info "Testing database connectivity..."
    
    local postgres_pod=$(kubectl get pods -n "$NAMESPACE" -l app=postgres -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
    
    if [ -n "$postgres_pod" ]; then
        if kubectl exec -n "$NAMESPACE" "$postgres_pod" -- pg_isready -U postgres -d weatherdb >/dev/null 2>&1; then
            log_success "PostgreSQL database is ready"
        else
            log_error "PostgreSQL database is not ready"
            return 1
        fi
    else
        log_error "PostgreSQL pod not found"
        return 1
    fi
}

# API endpoint test
test_api_endpoints() {
    log_info "Testing API endpoints..."
    
    # Test FastAPI health endpoint
    if command -v curl &>/dev/null; then
        if curl -s -f "http://localhost:8000/health" >/dev/null 2>&1; then
            local status=$(curl -s "http://localhost:8000/health" | jq -r '.status' 2>/dev/null || echo "unknown")
            if [ "$status" = "healthy" ]; then
                log_success "FastAPI health endpoint is healthy"
            else
                log_warning "FastAPI responding but status: $status"
            fi
        else
            log_warning "FastAPI health endpoint not accessible"
        fi
        
        # Test Next.js health endpoint
        if curl -s -f "http://localhost:3000/api/health" >/dev/null 2>&1; then
            local status=$(curl -s "http://localhost:3000/api/health" | jq -r '.status' 2>/dev/null || echo "unknown")
            if [ "$status" = "healthy" ]; then
                log_success "Next.js health endpoint is healthy"
            else
                log_warning "Next.js responding but status: $status"
            fi
        else
            log_warning "Next.js health endpoint not accessible"
        fi
    else
        log_warning "curl not available, skipping HTTP endpoint tests"
    fi
}

# Performance test
test_performance() {
    log_info "Running basic performance tests..."
    
    if command -v curl &>/dev/null; then
        local total_time=0
        local requests=5
        
        for i in $(seq 1 $requests); do
            local response_time=$(curl -w "%{time_total}" -o /dev/null -s "http://localhost:3000" 2>/dev/null || echo "0")
            total_time=$(echo "$total_time + $response_time" | bc -l 2>/dev/null || echo "$total_time")
            sleep 1
        done
        
        local avg_time=$(echo "scale=3; $total_time / $requests" | bc -l 2>/dev/null || echo "0")
        log_info "Average response time: ${avg_time}s over $requests requests"
        
        # Check if performance is acceptable (< 2 seconds)
        if (( $(echo "$avg_time < 2.0" | bc -l 2>/dev/null || echo "0") )); then
            log_success "Performance test passed (avg: ${avg_time}s)"
        else
            log_warning "Performance may be degraded (avg: ${avg_time}s)"
        fi
    else
        log_warning "curl not available, skipping performance tests"
    fi
}

# Service connectivity test
test_service_connectivity() {
    log_info "Testing service connectivity..."
    
    # Check if services exist
    local services=("postgres-service" "fastapi-service" "nextjs-service")
    for service in "${services[@]}"; do
        if kubectl get service "$service" -n "$NAMESPACE" &>/dev/null; then
            log_success "Service '$service' exists"
        else
            log_error "Service '$service' does not exist"
            return 1
        fi
    done
}

# Main test function that combines all tests
test_all() {
    log_info "Running comprehensive test suite..."
    
    local failed_tests=0
    
    if ! test_health_check; then
        ((failed_tests++))
    fi
    
    if ! test_database_connectivity; then
        ((failed_tests++))
    fi
    
    if ! test_service_connectivity; then
        ((failed_tests++))
    fi
    
    test_api_endpoints  # Non-critical, doesn't fail the suite
    test_performance   # Non-critical, doesn't fail the suite
    
    if [ $failed_tests -eq 0 ]; then
        log_success "All critical tests passed!"
        return 0
    else
        log_error "$failed_tests critical test(s) failed"
        return 1
    fi
}

# Usage information
usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  health              Run health check tests"
    echo "  database           Test database connectivity"
    echo "  api                Test API endpoints"
    echo "  performance        Run performance tests"
    echo "  connectivity       Test service connectivity"
    echo "  all                Run all tests (default)"
    echo "  help               Show this help message"
}

# Main execution
case "${1:-all}" in
    "health")
        test_health_check
        ;;
    "database")
        test_database_connectivity
        ;;
    "api")
        test_api_endpoints
        ;;
    "performance")
        test_performance
        ;;
    "connectivity")
        test_service_connectivity
        ;;
    "all")
        test_all
        ;;
    "help"|"--help"|"-h")
        usage
        ;;
    *)
        echo "Unknown command: $1"
        usage
        exit 1
        ;;
esac