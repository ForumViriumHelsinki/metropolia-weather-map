# Database Setup for Weather Map

This document describes the database user configuration for Cloud SQL IAM authentication.

## Current Architecture

The application uses a single IAM service account for both the application and migrations:

- **GCP Service Account**: `weather-map@fvh-project-containers-etc.iam.gserviceaccount.com`
- **Cloud SQL IAM User**: `weather-map@fvh-project-containers-etc.iam`
- **Database**: `weatherdb`
- **Schema**: `weather`

## Required Database Privileges

### For Migrations (DDL + DML)

The migration user needs full control to create/alter schema objects:

```sql
-- Connect to weatherdb
\c weatherdb

-- Schema privileges
GRANT USAGE, CREATE ON SCHEMA weather TO "weather-map@fvh-project-containers-etc.iam";
GRANT USAGE, CREATE ON SCHEMA public TO "weather-map@fvh-project-containers-etc.iam";

-- Table privileges (existing and future)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA weather TO "weather-map@fvh-project-containers-etc.iam";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "weather-map@fvh-project-containers-etc.iam";

-- Default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA weather
GRANT ALL PRIVILEGES ON TABLES TO "weather-map@fvh-project-containers-etc.iam";

-- Sequence privileges (if using SERIAL/BIGSERIAL columns)
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA weather TO "weather-map@fvh-project-containers-etc.iam";
ALTER DEFAULT PRIVILEGES IN SCHEMA weather
GRANT ALL PRIVILEGES ON SEQUENCES TO "weather-map@fvh-project-containers-etc.iam";
```

### For Application (DML only) - Future State

In a least-privilege setup, the application user should only have:

```sql
-- Read/write data, no schema modifications
GRANT USAGE ON SCHEMA weather TO "weather-map-app@fvh-project-containers-etc.iam";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA weather TO "weather-map-app@fvh-project-containers-etc.iam";
ALTER DEFAULT PRIVILEGES IN SCHEMA weather
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO "weather-map-app@fvh-project-containers-etc.iam";
```

## Running Grants Manually

Connect to Cloud SQL as the postgres superuser:

```bash
gcloud sql connect fvh-postgres --user=postgres --database=weatherdb
```

Then run the SQL commands above.

## Automation Roadmap

### Option 1: Terraform PostgreSQL Provider

Add the [cyrilgdn/postgresql](https://registry.terraform.io/providers/cyrilgdn/postgresql/latest) provider to manage grants declaratively:

```hcl
# In infrastructure/gcp/weather_map.tf

provider "postgresql" {
  host     = google_sql_database_instance.main.private_ip_address
  username = "postgres"
  password = data.google_secret_manager_secret_version.postgres_password.secret_data
  sslmode  = "require"
}

resource "postgresql_grant" "weather_map_schema" {
  database    = "weatherdb"
  role        = google_sql_user.weather_map.name
  schema      = "weather"
  object_type = "schema"
  privileges  = ["USAGE", "CREATE"]
}

resource "postgresql_grant" "weather_map_tables" {
  database    = "weatherdb"
  role        = google_sql_user.weather_map.name
  schema      = "weather"
  object_type = "table"
  privileges  = ["SELECT", "INSERT", "UPDATE", "DELETE"]
}

resource "postgresql_default_privileges" "weather_map_tables" {
  database    = "weatherdb"
  role        = google_sql_user.weather_map.name
  schema      = "weather"
  owner       = "postgres"
  object_type = "table"
  privileges  = ["SELECT", "INSERT", "UPDATE", "DELETE"]
}
```

**Challenges:**
- Requires network access from Terraform Cloud to Cloud SQL (via Cloud SQL Auth Proxy or private IP)
- Need to store postgres password securely

### Option 2: Init Container with Grant Script

Add a one-time job or init container that runs grants using a privileged user:

```yaml
# In migrations job or separate setup job
initContainers:
- name: setup-grants
  image: postgres:16-alpine
  command: ["psql"]
  args:
  - "-h"
  - "127.0.0.1"
  - "-U"
  - "postgres"
  - "-d"
  - "weatherdb"
  - "-f"
  - "/scripts/grants.sql"
```

**Challenges:**
- Requires postgres superuser password in Kubernetes
- Less declarative than Terraform

### Option 3: Cloud SQL Database Flags + Startup Script

Use Cloud SQL startup scripts or database flags, though this has limited support for grants.

## Recommended Future Architecture

Split into two service accounts with principle of least privilege:

| Service Account | Purpose | Privileges |
|-----------------|---------|------------|
| `weather-map-migrations` | Schema migrations | ALL on schema, tables, sequences |
| `weather-map-app` | Application runtime | SELECT, INSERT, UPDATE, DELETE |

This requires:
1. Create second GCP service account in Terraform
2. Create second Cloud SQL IAM user
3. Update Helm values to use different users for migrations vs app
4. Grant appropriate privileges to each user

## Related Files

- **Terraform**: `infrastructure/gcp/weather_map.tf` - GCP resources
- **Helm Values**: `deploy/server-values.yaml` - Kubernetes deployment config
- **Migrations**: `db/migrations/` - Database schema migrations
