# Solr Health Check Monitoring Sidecar

A lightweight Python monitoring service that runs alongside your Solr container on each GCP VM and logs health metrics to GCP Cloud Logging.

## Features

- **Container Health**: Verifies the Solr Docker container is running
- **Query Test**: Verifies search functionality with `*:*` query
- **Disk Monitoring**: Alerts if disk usage exceeds 90%
- **Cloud Logging Integration**: All checks logged to GCP Cloud Logging for monitoring and alerting

## Monitoring Interval

Runs health checks every **5 minutes** (300 seconds) and logs results to GCP Cloud Logging.

## Building the Sidecar Image

Build and push using the Makefile:

```bash
cd namex-solr/healthcheck-sidecar

# Build, tag for all envs (dev/test/sandbox/prod), and push
make push

# Or build only
make build
```

See the Makefile for all available targets:
```bash
make help
```

## Deployment on VM

The health check sidecar is automatically started by the VM startup script (`startupscript.txt`) after the Solr container starts. The sidecar runs with:
- `--network=host` — so it can reach Solr on `localhost:8983`
- Docker socket mounted (`/var/run/docker.sock`) — so it can check the Solr container status

The startup script will:
1. Start the health check container
2. Verify it's running
3. Exit with an error if startup fails

## Monitoring

### On the VM (via SSH)

```bash
# Follow logs in real time
docker logs -f solr-healthcheck

# View last 50 lines
docker logs --tail 50 solr-healthcheck

# Check Solr core status directly
curl -s 'http://localhost:8983/solr/admin/cores?action=STATUS'
```

### In GCP Cloud Logging

View the sidecar logs and alerts in GCP Cloud Logging:

```bash
# View recent logs
gcloud logging read "resource.type=gce_instance AND jsonPayload.container.name=solr-healthcheck" \
  --project=<PROJECT> \
  --limit=50 \
  --format=json

# View only failures
gcloud logging read "resource.type=gce_instance AND jsonPayload.container.name=solr-healthcheck AND severity=WARNING" \
  --project=<PROJECT> \
  --limit=20 \
  --format=json
```

Create alerts in Cloud Monitoring based on log patterns:
- Alert on `severity=WARNING` messages for health check failures
- Create metrics from log patterns for SLO tracking

## Environment

The sidecar auto-detects the role (leader/follower) from GCP instance metadata:
- **ROLE**: `leader` or `follower` → determines which core to check (`name_request` or `name_request_follower`)

