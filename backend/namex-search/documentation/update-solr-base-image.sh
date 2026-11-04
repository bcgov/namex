#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

########################################
# CONFIG
########################################

PROJECT="a083gt"
ENV="prod"
PROJECT_ID="${PROJECT}-${ENV}"

APP="namex"
ZONE="northamerica-northeast1-a"
REGION="northamerica-northeast1"

TEMPLATE_VERSION="v3"
BOOT_DISK_IMAGE=$(gcloud compute images list \
  --project=cos-cloud \
  --filter="name~'cos-121'" \
  --sort-by=~name \
  --limit=1 \
  --format="value(name)")

echo "Using COS image: ${BOOT_DISK_IMAGE}"

STARTUP_SCRIPT_PATH="${SCRIPT_DIR}/../namex-solr/startupscript.txt"
if [[ ! -f "$STARTUP_SCRIPT_PATH" ]]; then
    echo "ERROR: Startup script not found at ${STARTUP_SCRIPT_PATH}"
    exit 1
fi
echo "Using startup script: ${STARTUP_SCRIPT_PATH}"
if ! command -v jq &>/dev/null; then
    echo "ERROR: jq is required. Install with: brew install jq"
    exit 1
fi

########################################
# TEMPLATE NAMES
########################################

LEADER_TEMPLATE="${APP}-solr-leader-vm-tmpl-${ENV}-${TEMPLATE_VERSION}"
FOLLOWER_TEMPLATE="${APP}-solr-follower-vm-tmpl-${ENV}-${TEMPLATE_VERSION}"

########################################
# HELPER: Clone template with new boot disk image
# Uses REST API to preserve ALL properties exactly.
########################################

clone_template_with_new_image() {
    local source_template="$1"
    local new_template="$2"
    local new_image="$3"

    echo "  Exporting full template: ${source_template}"

    # Export the full template as JSON
    local template_json
    template_json=$(gcloud compute instance-templates describe "$source_template" \
        --project="$PROJECT_ID" --format=json)

    # Replace boot image and startup script, keep everything else
    local new_source_image="projects/cos-cloud/global/images/${new_image}"
    local startup_script
    startup_script=$(cat "$STARTUP_SCRIPT_PATH")
    local body
    body=$(echo "$template_json" | jq \
        --arg name "$new_template" \
        --arg img "$new_source_image" \
        --arg script "$startup_script" \
        '{
            name: $name,
            properties: .properties
        }
        | .properties.disks[0].initializeParams.sourceImage = $img
        | .properties.metadata.items = [.properties.metadata.items[] | if .key == "startup-script" then .value = $script else . end]')

    echo "  Creating new template via REST API: ${new_template}"

    # Check if template already exists
    if gcloud compute instance-templates describe "$new_template" --project="$PROJECT_ID" &>/dev/null; then
        echo "  ⚠ Template ${new_template} already exists. Delete it first to recreate."
        echo "    gcloud compute instance-templates delete ${new_template} --project=${PROJECT_ID} --quiet"
        return 1
    fi

    local access_token
    access_token=$(gcloud auth print-access-token)

    local response
    response=$(curl -s -w "\n%{http_code}" -X POST \
        "https://compute.googleapis.com/compute/v1/projects/${PROJECT_ID}/global/instanceTemplates" \
        -H "Authorization: Bearer ${access_token}" \
        -H "Content-Type: application/json" \
        -d "$body")

    local http_code
    http_code=$(echo "$response" | tail -1)
    response=$(echo "$response" | sed '$d')

    if [[ "$http_code" -lt 200 || "$http_code" -ge 300 ]]; then
        echo "  ERROR: REST API returned HTTP ${http_code}"
        echo "$response" | jq -r '.error.message // .' 2>/dev/null || echo "$response"
        return 1
    fi

    # Wait for the operation to complete
    local op_name op_status
    op_name=$(echo "$response" | jq -r '.name // empty')
    if [[ -n "$op_name" ]]; then
        echo "  Waiting for operation ${op_name}…"
        while true; do
            op_status=$(gcloud compute operations describe "$op_name" \
                --global --project="$PROJECT_ID" --format="value(status)")
            if [[ "$op_status" == "DONE" ]]; then
                break
            fi
            sleep 2
        done
    fi

    echo "  ✔ Template ${new_template} created."
}

########################################
# CREATE LEADER TEMPLATE
########################################

echo "➤ Creating leader template: $LEADER_TEMPLATE"

clone_template_with_new_image \
    "${APP}-solr-leader-vm-tmpl-${ENV}" \
    "$LEADER_TEMPLATE" \
    "$BOOT_DISK_IMAGE"

########################################
# CREATE FOLLOWER TEMPLATE
########################################

if [[ "$ENV" != "dev" ]]; then
  echo "➤ Creating follower template: $FOLLOWER_TEMPLATE"

  clone_template_with_new_image \
      "${APP}-solr-follower-vm-tmpl-${ENV}" \
      "$FOLLOWER_TEMPLATE" \
      "$BOOT_DISK_IMAGE"
fi

echo "✔ Base image templates created."
echo "Next step: update deploy-solr.sh to reference version ${TEMPLATE_VERSION}"
