# SOLR Infrastructure Deployment Script

This repository contains Bash scripts to automate the deployment and management of a SOLR cluster in Google Cloud Platform (GCP) using a leader/follower architecture. The scripts are intentionally split into responsibilities.

[Figma diagram](https://www.figma.com/board/nEjO2J7H63bFBgP2TKmjM0/Firebase-Infra?node-id=0-1&p=f&t=f41Xb5kWQbtkcSFH-0)

## Scripts Overview (Read This First)

| Script | Purpose | When to Run |
|------|--------|------------|
| `gcp-solr-infra.sh` | One-time infrastructure setup | New environment or major infra change / Infrastructure bootstrap |
| `update-solr-base-image.sh` | Create new VM templates with updated COS image | OS / security updates for base image (OS) |
| `new-template.sh` | Full rebuild or template-only update | Dev/test: `--templates-only` for no downtime, `--update-vm` to apply shielded settings to running VMs |
| `deploy-solr.sh` | Deploy Solr + rotate VMs | App changes or after base image update |

> ⚠️ **Important:**
> Updating the base image does **not** affect running VMs until a redeploy is performed.

---

## Prerequisites

Before running the scripts, ensure the following:

- **Google Cloud SDK** installed and authenticated (`gcloud auth login`).
- **`oc` CLI** installed and authenticated (`oc login`) — required for importer job management.
- **Docker** installed — required for building images.
- **`make`** installed — required for building Solr images.
- `gcloud` is configured for your project.
- Proper IAM roles are assigned to your service accounts.
- Artifact Registry and required images exist.
- Startup script file exists at the specified path: `namex-solr/startupscript.txt`.
- **IAP tunneling** access is configured — VMs have no external IPs; the script uses `gcloud compute ssh --tunnel-through-iap` for health checks and replication configuration.

> The `deploy` command verifies both `gcloud` and `oc` authentication before proceeding.

---

# Usage

## Script 1: Infrastructure Bootstrap

Make sure to populate desired variable values correctly, e.g. ENV, LABEL, etc.

```
chmod +x gcp-solr-infra.sh
./documentation/gcp-solr-infra.sh
```
it is important to run this from 1 level higher as the script references location of startup.txt

⚠️ **Important Notes:**

- The script is fragile and may fail if resources are missing or already exist.
- You may need to set up the service account permissions for common project artifact registry manually.
- Zone-specific resource availability may block VM creation; you may need to wait for the resources to become available.
- VM templates enforce **Secure Boot** and **block project-wide SSH keys**. These must be enabled manually on existing VMs via the GCP console if not using the templates.

## Leader/Follower SOLR Replication

Replication is **configured automatically** by `deploy-solr.sh deploy` for test/prod environments. The script:

1. Creates the follower VM and waits for the Solr core to be ready.
2. SSHs into the follower via IAP tunnel and sets `solr.leaderUrl` pointing to the new leader's internal IP.

No manual steps are required.

To **verify** replication after deploy, SSH into the follower and run:

```bash
gcloud compute ssh <FOLLOWER_VM> --zone=<ZONE> --project=<PROJECT_ID> --tunnel-through-iap \
  --command="curl -s 'http://localhost:8983/solr/name_request_follower/config/requestHandler?componentName=/replication'"
```

You should see the leader URL in the response:
```json
{
  "responseHeader": {
    "status": 0,
    "QTime": 29
  },
  "config": {
    "requestHandler": {
      "/replication": {
        "name": "/replication",
        "class": "solr.ReplicationHandler",
        "follower": {
          "leaderUrl": "http://<LEADER_INTERNAL_IP>:8983/solr/name_request",
          "pollInterval": "00:00:30",
          "compression": "internal"
        }
      }
    }
  }
}
```

To verify data has replicated to the follower:
```bash
gcloud compute ssh <FOLLOWER_VM> --zone=<ZONE> --project=<PROJECT_ID> --tunnel-through-iap \
  --command="curl -s 'http://localhost:8983/solr/admin/cores?action=STATUS'"
```

You should see a non-empty follower core:
```json
{
  "responseHeader": {
    "status": 0,
    "QTime": 133
  },
  "initFailures": {},
  "status": {
    "name_request_follower": {
      "name": "name_request_follower",
      "instanceDir": "/var/solr/data/name_request_follower",
      "dataDir": "/var/solr/data/name_request_follower/data/",
      "config": "solrconfig.xml",
      "schema": "managed-schema.xml",
      "startTime": "2025-12-11T18:53:38.144Z",
      "uptime": 8710669,
      "index": {
        "numDocs": 8784132,
        "maxDoc": 8784134,
        "deletedDocs": 2,
        "segmentCount": 31,
        "current": true,
        "hasDeletions": true,
        "sizeInBytes": 3830194266,
        "size": "3.57 GB"
      }
    }
  }
}
```

## Solr Admin UI

To access the Solr admin UI, SSH into a Solr VM with a local port forward, then open the UI in your browser.

1. **Look up the VM name** if needed — names change per deploy, e.g. `namex-solr-leader-dev-2026-07-28--103332`:
   ```bash
   gcloud compute instances list --project=a083gt-$ENV --sort-by=name
   ```

2. **SSH with a local port forward** (adjust VM name / project as needed):
   ```bash
   gcloud compute ssh namex-solr-leader-dev-2026-07-28--103332 --project=a083gt-dev \
     -- -L 8983:localhost:8983
   ```

3. **Open the admin UI** at http://localhost:8983/solr

   The core selector shows `name_request` on the leader VM and `name_request_follower` on the follower VM.

## Script 2: Base Image (COS) & Startup Script Updates

Use this script whenever you need to update the **base OS image** or the **VM startup script** (`namex-solr/startupscript.txt`). The script clones the existing instance template, swaps in the latest COS image and injects a fresh copy of the startup script from the repo.

Examples of changes that require a new template via this script:
- OS / security updates (new COS image)
- Adding or modifying sidecar containers (e.g. starting a a health-check sidecar via startup script)
- Changing Docker run flags, mount paths, or container versions in the startup script

```
chmod +x update-solr-base-image.sh
./documentation/update-solr-base-image.sh
```

Creates new instance templates. Versions templates (e.g. -v2, -v3). Does not touch running VMs — a redeploy (`deploy-solr.sh deploy`) is required for changes to take effect.

## Script 2b: Full VM Rebuild or Template Update

Recreates instance templates (and optionally VMs) from scratch. Useful for applying new template settings like Secure Boot or custom service accounts.

```
chmod +x new-template.sh
./documentation/new-template.sh                  # Full rebuild: delete VMs, recreate templates + VMs
./documentation/new-template.sh --templates-only # Update templates only, leave running VMs untouched
./documentation/new-template.sh --update-vm      # Update templates + enable Secure Boot on running VMs
```

- `--templates-only` skips VM deletion and creation — only replaces the instance templates. Use this when you want to update template settings without downtime or data loss.
- `--update-vm` skips VM deletion and creation, but updates shielded settings (Secure Boot) on running VMs. VMs are stopped, updated, and restarted — expect brief downtime per VM.

## Script 3: Application Deploy & VM Rotation

Update relevant vars at the top of the script: `ENV`, `SOURCE_TAG`, `TEMPLATE_VERSION`.

```bash
chmod +x deploy-solr.sh
./documentation/deploy-solr.sh build                                  # DEV only: build & push images
./documentation/deploy-solr.sh tag                                    # Promote images from SOURCE_TAG → ENV
./documentation/deploy-solr.sh deploy                                 # Blue-green VM rotation
./documentation/deploy-solr.sh deploy-follower                        # Deploy follower only (TEST/PROD)
./documentation/deploy-solr.sh deploy --leader-machine-type=e2-standard-4   # Override leader machine type
./documentation/deploy-solr.sh deploy --follower-machine-type=e2-standard-4 # Override follower machine type
```

### What `deploy` does

1. **Verifies prerequisites** — checks `gcloud`, `docker`, `make`, `oc` are installed and authenticated.
2. **Creates a new leader VM** — tries each zone until one succeeds (zone failover).
3. **Waits for Solr** — polls the leader core via SSH/IAP tunnel until it responds to ping.
4. **Swaps leader backend** — adds new leader to instance group + backend service, waits for health check, then removes old leader from backend. Rolls back if the new leader fails health checks.
5. **Runs the importer job** — sets `REINDEX_CORE=True` in the OpenShift secret, creates a job from the importer CronJob, and waits up to 90 minutes for completion. Resets the flag on exit (via trap).
6. **(test/prod only) Creates a new follower VM** — same zone-failover approach.
7. **Configures replication** — SSHs into follower via IAP tunnel and sets `solr.leaderUrl` to the new leader's internal IP.
8. **Swaps follower backend** — same health-check-then-swap as leader.
9. **Cleans up old VMs** — deletes old leader and follower VMs only after full success.

### What `deploy-follower` does

1. **Resolves leader IP** — finds the current leader VM and reads its internal IP (read-only, no leader disruption).
2. **Creates a new follower VM** — from the follower instance template with zone failover.
3. **Configures replication** — SSHs into follower via IAP tunnel and sets `solr.leaderUrl` to the current leader's IP.
4. **Swaps follower backend** — adds new follower to instance group + backend, waits for health check, then removes old follower.
5. **Cleans up old follower** — deletes the old follower VM after successful swap.

### Machine type overrides

By default, the deploy script uses the machine types defined in the instance templates. To override the machine type for a specific deploy without modifying the base templates:

```bash
# Deploy with a larger leader (4 vCPUs, 16GB RAM)
./deploy-solr.sh deploy --leader-machine-type=e2-standard-4

# Deploy with a custom follower
./deploy-solr.sh deploy --follower-machine-type=e2-standard-4

# Override both
./deploy-solr.sh deploy --leader-machine-type=e2-standard-4 --follower-machine-type=e2-highcpu-8
```

This creates a temporary instance template with the specified machine type (copied from the base template) and uses it for the new VM. The base templates are not modified.

### VM naming convention

VMs are named `namex-solr-{leader|follower}-{ENV}-{timestamp}`, e.g. `namex-solr-leader-prod-2026-03-30--220000`.

### Known limitations

- **Old VM detection** uses `--limit=1` — if multiple orphan VMs exist from failed runs, only the newest is detected and cleaned up. Manually check for orphans with:
  ```bash
  gcloud compute instances list --project a083gt-$ENV --sort-by=name
  ```
- **Subnet IP exhaustion** — the `/28` subnet has only 14 usable IPs. Orphan VMs from failed runs consume IPs. Clean up orphans before redeploying if you hit IP exhaustion errors.
