# Skaffold Testing Guide

This guide explains how to use Skaffold's integrated testing capabilities for the Metropolia Weather Map application, replacing traditional shell scripts with declarative test configurations.

## Overview

The project now uses Skaffold's native testing features to provide:

- **Automated testing** during development and deployment
- **Container structure validation** for built images
- **Profile-based test suites** for different environments
- **Post-deployment verification** of running services

## Test Types

### 1. Custom Tests

Custom tests run commands against built images to validate application functionality.

```bash
# Run all tests
skaffold test

# Run tests for specific image
skaffold test --images=weather-map-server
```

### 2. Container Structure Tests

Validates that container images are built correctly with proper dependencies, files, and configuration.

```bash
# Structure tests run automatically with custom tests
# Or run explicitly:
container-structure-test test --image weather-map-server:latest --config tests/structure/server-structure-test.yaml
```

### 3. Verify Tests

Post-deployment validation that ensures services are responding correctly.

```bash
# Run verification tests
skaffold verify

# Run verification with specific build artifacts
skaffold verify --build-artifacts=build.json
```

## Test Profiles

### Quick Test Profile

Fast health checks suitable for development loops:

```bash
skaffold dev -p quick-test
```

**Includes:**
- Basic health checks
- Linting
- Fast validation

### Full Test Profile

Comprehensive testing for staging/production validation:

```bash
skaffold run -p full-test
```

**Includes:**
- Complete health checks
- Unit tests with coverage
- Build validation
- Code quality checks

### Benchmark Test Profile

Performance and load testing:

```bash
skaffold run -p benchmark-test
```

**Includes:**
- Performance benchmarks
- Load testing
- Resource utilization checks

## Test Scripts

### Modular Test Runner

The `scripts/test-runner.sh` provides modular test functions:

```bash
# Individual test functions
./scripts/test-runner.sh health          # Health checks
./scripts/test-runner.sh database        # Database connectivity
./scripts/test-runner.sh api             # API endpoint validation
./scripts/test-runner.sh performance     # Basic performance tests
./scripts/test-runner.sh connectivity    # Service connectivity
./scripts/test-runner.sh all             # All tests combined
```

### Usage in Skaffold

Tests are automatically triggered based on file changes:

```yaml
test:
  - image: weather-map-server
    custom:
      - command: ./scripts/test-runner.sh health
        dependencies:
          paths:
            - "src/**/*.py"
            - "scripts/test-runner.sh"
```

## Development Workflow

### Local Development

1. **Start development with testing:**
   ```bash
   skaffold dev
   ```

2. **Quick validation during development:**
   ```bash
   skaffold dev -p quick-test
   ```

3. **Test specific changes:**
   ```bash
   skaffold test
   ```

### CI/CD Pipeline

1. **Build and test:**
   ```bash
   skaffold build --file-output=build.json
   skaffold test --build-artifacts=build.json
   ```

2. **Deploy and verify:**
   ```bash
   skaffold deploy --build-artifacts=build.json
   skaffold verify --build-artifacts=build.json
   ```

3. **Full pipeline with profiles:**
   ```bash
   skaffold run -p full-test
   ```

## Test Configuration

### Adding New Tests

1. **Custom tests** - Add to `skaffold.yaml`:
   ```yaml
   test:
     - image: your-image
       custom:
         - command: your-test-command
           timeoutSeconds: 60
           dependencies:
             paths:
               - "relevant/files/**"
   ```

2. **Structure tests** - Create YAML configuration:
   ```yaml
   schemaVersion: '2.0.0'
   commandTests:
     - name: "Test description"
       command: "test-command"
       expectedOutput: ["expected"]
   ```

3. **Verify tests** - Add to `skaffold.yaml`:
   ```yaml
   verify:
     - name: test-name
       container:
         name: test-container
         image: test-image
         command: ["test-command"]
   ```

### Test Dependencies

Specify file dependencies to trigger test re-runs:

```yaml
dependencies:
  paths:
    - "src/**/*.py"        # Python source files
    - "package.json"       # Node.js dependencies
    - "requirements.txt"   # Python dependencies
    - "test/**/*"          # Test files
```

## Migration from Shell Scripts

### Replaced Scripts

All legacy shell script wrappers have been replaced with native Skaffold commands:

| Old Script (Removed) | New Approach | Native Command |
|---------------------|-------------|----------------|
| `quick-health-check.sh` | Modular test-runner.sh functions | `./scripts/test-runner.sh health` |
| `validate-skaffold-deployment.sh` | Full test profile | `skaffold run -p full-test` |
| `performance-benchmark.sh` | Benchmark profile | `skaffold run -p benchmark-test` |
| `skaffold-dev.sh` | Native skaffold commands | `skaffold [command] -p [profile]` |

**Only `scripts/test-runner.sh` remains - it provides modular test functions used by Skaffold.**

### Benefits

- **Integrated workflow**: Tests run automatically with build/deploy
- **File watching**: Tests re-run when relevant files change
- **Better error handling**: Built-in timeouts and retries
- **Profile management**: Different test suites for different environments
- **CI/CD ready**: Native integration with pipelines

## Troubleshooting

### Common Issues

1. **Tests not running:**
   - Check that the image name matches the artifact name
   - Verify test commands are executable
   - Check timeout values

2. **Structure tests failing:**
   - Ensure container-structure-test is installed
   - Verify test configurations match actual image structure
   - Check file paths and permissions

3. **Verify tests failing:**
   - Ensure services are deployed and ready
   - Check service names and endpoints
   - Verify network connectivity between test containers and services

### Debug Commands

```bash
# Verbose output
skaffold test -v debug

# Test specific profile
skaffold test -p full-test

# Skip tests during development
skaffold dev --skip-tests

# Run only verification
skaffold verify --build-artifacts=build.json
```

## Best Practices

1. **Keep tests fast**: Use appropriate timeouts and efficient test commands
2. **Use profiles**: Separate quick development tests from comprehensive CI tests
3. **Test dependencies**: Specify file dependencies to avoid unnecessary test runs
4. **Modular scripts**: Use the test-runner.sh functions for consistency
5. **Document tests**: Add clear descriptions and expected outcomes
6. **Monitor performance**: Use benchmark profiles to track performance regressions

## Examples

See the `examples/` directory for additional test configurations and the `tests/structure/` directory for container structure test examples.