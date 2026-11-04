#!/usr/bin/env bash
set -euo pipefail
set -o errtrace  # ensure ERR traps fire inside functions/subshells

########################################
# CONFIGURATION
########################################

ENV="dev"   # dev / test / prod
SOURCE_TAG="dev"

PROJECT="a083gt"
PROJECT_ID="${PROJECT}-${ENV}"
ARTIFACT_REGISTRY_PROJECT="c4hnrd-tools"
OC_NAMESPACE="cbaab0-${ENV}"
IMPORTER_SECRET="namex-solr-importer-${ENV}-secret"

SCHEDULERS_PAUSED=0

LEADER_BACKEND="namex-solr-leader-backend"
FOLLOWER_BACKEND="namex-solr-follower-backend"

ZONES=("northamerica-northeast1-a" "northamerica-northeast1-b" "northamerica-northeast1-c")
REGION="northamerica-northeast1"
REPO_PATH="${REGION}-docker.pkg.dev/${ARTIFACT_REGISTRY_PROJECT}/vm-repo"

# Template versions must match what update-solr-base-image.sh created
LEADER_TEMPLATE_VERSION=""       # e.g., "v2" or "v3"
FOLLOWER_TEMPLATE_VERSION=""  # e.g., "v8cpu"

LEADER_TEMPLATE="namex-solr-leader-vm-tmpl-${ENV}${LEADER_TEMPLATE_VERSION:+-$LEADER_TEMPLATE_VERSION}"
FOLLOWER_TEMPLATE="namex-solr-follower-vm-tmpl-${ENV}${FOLLOWER_TEMPLATE_VERSION:+-$FOLLOWER_TEMPLATE_VERSION}"


########################################
# HELPER FUNCTIONS
########################################

log() { echo -e "\n[$(date -u +%H:%M:%S)] 🔹  $1\n"; }

require() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "ERROR: Missing required command: $1"
        exit 1
    fi
}

check_prereqs() {
    log "Checking required tools…"
    require gcloud

    log "Verifying gcloud authentication…"
    if ! gcloud auth print-access-token &>/dev/null; then
        echo "ERROR: gcloud is not authenticated. Run: gcloud auth login"
        exit 1
    fi
}

check_build_prereqs() {
    check_prereqs
    require docker
    require make
}

check_deploy_prereqs() {
    check_prereqs
    require oc

    log "Verifying oc authentication…"
    if ! oc whoami &>/dev/null; then
        echo "ERROR: oc is not authenticated. Run: oc login"
        exit 1
    fi
}

create_vm_in_available_zone() {
    local vm_name="$1"
    local template="$2"
    local machine_type="${3:-}"

    for zone in "${ZONES[@]}"; do
        log "Trying to create ${vm_name} in ${zone}…" >&2
        local create_args=(
            gcloud compute instances create "${vm_name}"
            --source-instance-template "${template}"
            --zone "${zone}"
            --project "${PROJECT_ID}"
        )
        if [[ -n "${machine_type}" ]]; then
            create_args+=(--machine-type "${machine_type}")
        fi
        if timeout 120 "${create_args[@]}" >&2; then
            echo "${zone}"
            return 0
        fi
        log "Zone ${zone} unavailable, trying next…" >&2
    done

    echo "ERROR: All zones exhausted. Could not create ${vm_name}." >&2
    exit 1
}

ensure_instance_group() {
    local group_name="$1"
    local zone="$2"

    if ! gcloud compute instance-groups unmanaged describe "${group_name}" \
        --zone "${zone}" --project "${PROJECT_ID}" &>/dev/null; then
        log "Creating instance group ${group_name} in ${zone}…"
        gcloud compute instance-groups unmanaged create "${group_name}" \
            --zone "${zone}" --project "${PROJECT_ID}"
        gcloud compute instance-groups unmanaged set-named-ports "${group_name}" \
            --zone "${zone}" --project "${PROJECT_ID}" \
            --named-ports=http:8983
    fi
}

add_to_backend() {
    local backend_name="$1"
    local group="$2"
    local zone="$3"
    log "Adding instance group ${group} (${zone}) to backend ${backend_name}…"
    gcloud compute backend-services add-backend "${backend_name}" \
        --instance-group="${group}" \
        --instance-group-zone="${zone}" \
        --region="${REGION}" \
        --project="${PROJECT_ID}" 2>/dev/null || true
}

remove_old_backend() {
    local backend_name="$1"
    local new_group="$2"
    local new_zone="$3"
    local old_group="${4:-}"
    local old_zone="${5:-}"

    if [[ -n "${old_group}" && -n "${old_zone}" ]]; then
        if [[ "${old_group}" != "${new_group}" || "${old_zone}" != "${new_zone}" ]]; then
            if instance_group_exists "${old_group}" "${old_zone}"; then
                log "Removing old instance group ${old_group} (${old_zone}) from backend ${backend_name}…"
                gcloud compute backend-services remove-backend "${backend_name}" \
                    --instance-group="${old_group}" \
                    --instance-group-zone="${old_zone}" \
                    --region="${REGION}" \
                    --project="${PROJECT_ID}"
            else
                log "Old instance group ${old_group} does not exist in ${old_zone}, skipping removal."
            fi
        fi
    fi
}

rollback_backend() {
    local backend_name="$1"
    local group_name="$2"
    local zone="$3"
    log "ROLLBACK: Removing ${group_name} (${zone}) from backend ${backend_name}…"
    gcloud compute backend-services remove-backend "${backend_name}" \
        --instance-group="${group_name}" \
        --instance-group-zone="${zone}" \
        --region="${REGION}" \
        --project="${PROJECT_ID}" 2>/dev/null || true
}

get_instance_zone() {
    local vm_name="$1"
    gcloud compute instances list \
        --filter "name=${vm_name}" \
        --format "value(zone)" \
        --project "${PROJECT_ID}" | xargs basename
}

instance_group_exists() {
    local group_name="$1"
    local zone="$2"
    gcloud compute instance-groups unmanaged describe "${group_name}" \
        --zone="${zone}" --project="${PROJECT_ID}" &>/dev/null
}

retry() {
    local max_attempts="${1}"
    shift
    for i in $(seq 1 "${max_attempts}"); do
        if "$@"; then
            return 0
        fi
        log "Attempt ${i}/${max_attempts} failed, retrying in 5s…"
        sleep 5
    done
    echo "ERROR: Command failed after ${max_attempts} attempts: $*"
    return 1
}

wait_for_solr_ready() {
    local vm_name="$1"
    local zone="$2"
    local core="${3:-name_request}"
    local max_attempts="${4:-60}"
    log "Waiting for Solr core ${core} to be ready on ${vm_name}…"
    for i in $(seq 1 "${max_attempts}"); do
        if gcloud compute ssh "${vm_name}" \
            --zone="${zone}" --project="${PROJECT_ID}" \
            --tunnel-through-iap \
            --command="curl -sf http://localhost:8983/solr/${core}/admin/ping" \
            >/dev/null 2>&1; then
            log "Solr core ${core} is ready on ${vm_name}."
            return 0
        fi
        sleep 10
    done
    echo "ERROR: Solr core ${core} not ready on ${vm_name} after ${max_attempts} attempts."
    return 1
}

wait_for_healthy_backend() {
    local backend_name="$1"
    local instance_name="$2"
    local max_attempts="${3:-30}"
    log "Waiting for ${instance_name} to be healthy in backend ${backend_name}…"
    for i in $(seq 1 "${max_attempts}"); do
        local health
        health=$(gcloud compute backend-services get-health "${backend_name}" \
            --region="${REGION}" \
            --project="${PROJECT_ID}" \
            --flatten="status.healthStatus[]" \
            --format="csv[no-heading](status.healthStatus.instance,status.healthStatus.healthState)" \
            2>/dev/null || true)
        if echo "${health}" | grep "/instances/${instance_name}," | grep -q "HEALTHY"; then
            log "Instance ${instance_name} is healthy in backend ${backend_name}."
            return 0
        fi
        sleep 10
    done
    echo "ERROR: ${instance_name} did not become healthy in ${backend_name} after ${max_attempts} attempts."
    return 1
}

json_field() {
    # json_field <json> <key> [default]
    # Extracts the value of a JSON key (string, integer, or boolean) with grep/sed.
    # Keys are unique in the Solr payloads this script inspects.
    local json="$1" key="$2" default="${3:-}" value
    value=$(printf '%s' "${json}" \
        | grep -oE "\"${key}\"[[:space:]]*:[[:space:]]*(\"[^\"]*\"|[0-9]+|true|false)" \
        | head -1 \
        | sed -E 's/^[^:]*:[[:space:]]*"?//; s/"$//')
    if [[ -n "${value}" ]]; then
        echo "${value}"
    else
        echo "${default}"
    fi
}

wait_for_replication() {
    local follower_vm="$1"
    local follower_zone="$2"
    local leader_vm="${3:-}"
    local leader_zone="${4:-}"
    local follower_core="${5:-name_request_follower}"
    local leader_core="${6:-name_request}"
    local max_attempts="${7:-120}"
    local interval=5

    local expected_gen=0
    local leader_attempts=5
    local leader_retry_interval=10
    local leader_details

    log "Getting target generation from leader ${leader_vm}…"

    # Capture the leader generation once. The leader may continue receiving
    # writes after this point; the follower only needs to reach this generation
    # or anything newer.
    for attempt in $(seq 1 "${leader_attempts}"); do
        leader_details=$(gcloud compute ssh "${leader_vm}" \
            --zone="${leader_zone}" --project="${PROJECT_ID}" \
            --tunnel-through-iap \
            --command="curl -sf 'http://localhost:8983/solr/${leader_core}/replication?command=indexversion&wt=json'" \
            2>/dev/null || echo '{}')

        expected_gen=$(json_field "${leader_details}" generation 0)

        # Numeric hygiene
        [[ "${expected_gen}" =~ ^[0-9]+$ ]] || expected_gen=0

        if [[ "${expected_gen}" -gt 0 ]]; then
            break
        fi

        if [[ "${attempt}" -lt "${leader_attempts}" ]]; then
            log "Leader generation unavailable (attempt ${attempt}/${leader_attempts}); retrying in ${leader_retry_interval}s…"
            sleep "${leader_retry_interval}"
        fi
    done

    if [[ "${expected_gen}" -le 0 ]]; then
        echo "ERROR: Could not obtain a valid leader generation from ${leader_vm}."
        return 1
    fi

    log "Target leader generation=${expected_gen}. Waiting for ${follower_vm} to replicate…"

    for i in $(seq 1 "${max_attempts}"); do
        local follower_details
        follower_details=$(gcloud compute ssh "${follower_vm}" \
            --zone="${follower_zone}" --project="${PROJECT_ID}" \
            --tunnel-through-iap \
            --command="curl -sf 'http://localhost:8983/solr/${follower_core}/replication?command=details&wt=json'" \
            2>/dev/null || echo '{}')

        local is_replicating follower_gen times_replicated err_msg

        is_replicating=$(json_field "${follower_details}" isReplicating "true")
        follower_gen=$(json_field "${follower_details}" generation 0)
        times_replicated=$(json_field "${follower_details}" timesIndexReplicated 0)
        err_msg=$(json_field "${follower_details}" errMsg "")

        # Numeric hygiene
        [[ "${follower_gen}" =~ ^[0-9]+$ ]] || follower_gen=0
        [[ "${times_replicated}" =~ ^[0-9]+$ ]] || times_replicated=0

        if [[ -n "${err_msg}" ]]; then
            log "Replication cycle error on ${follower_vm}: ${err_msg}"
        fi

        if [[ "${is_replicating}" == "false" ]] \
            && [[ "${times_replicated}" -ge 1 ]] \
            && [[ "${follower_gen}" -ge "${expected_gen}" ]]; then
            log "Follower fully replicated (generation=${follower_gen}, target=${expected_gen}, timesIndexReplicated=${times_replicated})."
            return 0
        fi

        log "Replication in progress… isReplicating=${is_replicating}, follower_gen=${follower_gen}, target_gen=${expected_gen}, timesIndexReplicated=${times_replicated}"

        sleep "${interval}"
    done

    echo "ERROR: Follower did not reach target generation ${expected_gen} within $((max_attempts * interval))s."
    return 1
}

reset_reindex_flag() {
    log "Resetting REINDEX_CORE in secret…"
    oc -n "${OC_NAMESPACE}" patch secret "${IMPORTER_SECRET}" \
        -p '{"stringData":{"REINDEX_CORE":"False"}}' 2>/dev/null || true
}

pause_solr_schedulers() {
    local job
    log "Pausing solr sync schedulers…"
    for job in "namex-solr-api-sync-${ENV}" "namex-solr-api-heartbeat-${ENV}"; do
        if gcloud scheduler jobs describe "${job}" \
            --location="${REGION}" --project="${PROJECT_ID}" &>/dev/null; then
            log "Pausing scheduler job ${job}…"
            gcloud scheduler jobs pause "${job}" \
                --location="${REGION}" --project="${PROJECT_ID}" >/dev/null
        fi
    done
    SCHEDULERS_PAUSED=1
}

resume_solr_schedulers() {
    local job
    [[ "${SCHEDULERS_PAUSED}" -eq 1 ]] || return 0
    log "Resuming solr sync schedulers…"
    for job in "namex-solr-api-sync-${ENV}" "namex-solr-api-heartbeat-${ENV}"; do
        if gcloud scheduler jobs describe "${job}" \
            --location="${REGION}" --project="${PROJECT_ID}" &>/dev/null; then
            log "Resuming scheduler job ${job}…"
            gcloud scheduler jobs resume "${job}" \
                --location="${REGION}" --project="${PROJECT_ID}" >/dev/null
        fi
    done
    SCHEDULERS_PAUSED=0
}

cleanup_on_exit() {
    reset_reindex_flag
    resume_solr_schedulers
}

########################################
# BUILD DOCKER IMAGES (DEV ONLY)
########################################
build_images() {

    log "Building local Solr images…"
    cd ../namex-solr
    make build

    log "Authenticating Docker to GCP Artifact Registry…"
    gcloud auth configure-docker "${REGION}-docker.pkg.dev"

    log "Tagging images…"

    docker tag name-request-solr-leader "${REPO_PATH}/name-request-solr-leader:${ENV}"
    docker tag name-request-solr-follower "${REPO_PATH}/name-request-solr-follower:${ENV}"

    log "Pushing images…"
    docker push "${REPO_PATH}/name-request-solr-leader:${ENV}"
    docker push "${REPO_PATH}/name-request-solr-follower:${ENV}"
}

########################################
# TAGGING IMAGES FOR TEST/PROD
########################################
tag_images() {
    log "Tagging ${SOURCE_TAG} → ${ENV}…"

    gcloud artifacts docker tags add \
        "${REPO_PATH}/name-request-solr-leader:${SOURCE_TAG}" \
        "${REPO_PATH}/name-request-solr-leader:${ENV}"

    # Keep follower tagging for TEST/PROD — required for full deploy
    gcloud artifacts docker tags add \
        "${REPO_PATH}/name-request-solr-follower:${SOURCE_TAG}" \
        "${REPO_PATH}/name-request-solr-follower:${ENV}"
}

########################################
# DEPLOY NEW INSTANCES
########################################
deploy_instances() {

    timestamp=$(date -u +"%Y-%m-%d--%H%M%S")

    NEW_LEADER_VM="namex-solr-leader-${ENV}-${timestamp}"
    NEW_FOLLOWER_VM="namex-solr-follower-${ENV}-${timestamp}"

    # Safe old VM detection
    log "Determining old leader & follower VMs…"
    OLD_LEADER_VM=$(gcloud compute instances list \
        --format="value(name)" \
        --filter="name~'^namex-solr-leader-${ENV}-'" \
        --sort-by="~creationTimestamp" \
        --limit=1 \
        --project="${PROJECT_ID}" || true)

    OLD_FOLLOWER_VM=$(gcloud compute instances list \
        --format="value(name)" \
        --filter="name~'^namex-solr-follower-${ENV}-'" \
        --sort-by="~creationTimestamp" \
        --limit=1 \
        --project="${PROJECT_ID}" || true)

    log "OLD_LEADER_VM=${OLD_LEADER_VM:-none}"
    log "OLD_FOLLOWER_VM=${OLD_FOLLOWER_VM:-none}"

    # Resolve old zones up front
    OLD_LEADER_ZONE=""
    if [[ -n "${OLD_LEADER_VM}" ]]; then
        OLD_LEADER_ZONE=$(get_instance_zone "${OLD_LEADER_VM}")
    fi
    OLD_FOLLOWER_ZONE=""
    if [[ -n "${OLD_FOLLOWER_VM}" ]]; then
        OLD_FOLLOWER_ZONE=$(get_instance_zone "${OLD_FOLLOWER_VM}")
    fi

    #####################################
    # CREATE NEW LEADER
    #####################################

    # Ensure connection draining is set to avoid cutting active requests during swap
    log "Ensuring connection draining on backend services…"
    gcloud compute backend-services update "${LEADER_BACKEND}" \
        --connection-draining-timeout=30 \
        --region="${REGION}" --project="${PROJECT_ID}" 2>/dev/null || true
    gcloud compute backend-services update "${FOLLOWER_BACKEND}" \
        --connection-draining-timeout=30 \
        --region="${REGION}" --project="${PROJECT_ID}" 2>/dev/null || true

    log "Creating NEW Leader VM: ${NEW_LEADER_VM}"
    LEADER_ZONE=$(create_vm_in_available_zone "${NEW_LEADER_VM}" "${LEADER_TEMPLATE}" "${LEADER_MACHINE_TYPE}")
    log "Leader created in zone: ${LEADER_ZONE}"

    NEW_LEADER_INTERNAL_IP=$(gcloud compute instances describe "${NEW_LEADER_VM}" \
        --zone "${LEADER_ZONE}" --project "${PROJECT_ID}" \
        --format='value(networkInterfaces[0].networkIP)')

    # Wait for Solr core to be ready before any operations
    wait_for_solr_ready "${NEW_LEADER_VM}" "${LEADER_ZONE}" "name_request"

    # Zone-specific instance group names to avoid cross-zone collisions
    LEADER_ZONE_SUFFIX=$(basename "${LEADER_ZONE}" | grep -o '[a-c]$')
    NEW_LEADER_GRP="namex-solr-leader-grp-${ENV}-${LEADER_ZONE_SUFFIX}"
    OLD_LEADER_GRP=""
    if [[ -n "${OLD_LEADER_ZONE}" ]]; then
        OLD_LEADER_ZONE_SUFFIX=$(basename "${OLD_LEADER_ZONE}" | grep -o '[a-c]$')
        OLD_LEADER_GRP="namex-solr-leader-grp-${ENV}-${OLD_LEADER_ZONE_SUFFIX}"
    fi

    log "Adding NEW leader to instance group ${NEW_LEADER_GRP}…"
    ensure_instance_group "${NEW_LEADER_GRP}" "${LEADER_ZONE}"
    gcloud compute instance-groups unmanaged add-instances \
        "${NEW_LEADER_GRP}" \
        --zone "${LEADER_ZONE}" \
        --instances "${NEW_LEADER_VM}" \
        --project "${PROJECT_ID}"

    # Add new to backend (old still serves traffic during transition)
    add_to_backend "${LEADER_BACKEND}" "${NEW_LEADER_GRP}" "${LEADER_ZONE}"

    # Wait for new leader to be healthy BEFORE removing old
    if ! wait_for_healthy_backend "${LEADER_BACKEND}" "${NEW_LEADER_VM}"; then
        rollback_backend "${LEADER_BACKEND}" "${NEW_LEADER_GRP}" "${LEADER_ZONE}"
        log "Cleaning up failed leader VM: ${NEW_LEADER_VM}"
        gcloud compute instances delete "${NEW_LEADER_VM}" --zone="${LEADER_ZONE}" --project="${PROJECT_ID}" --quiet 2>/dev/null || true
        exit 1
    fi

    # New is healthy → safe to remove old backend so the importer writes only to the new leader
    remove_old_backend "${LEADER_BACKEND}" \
        "${NEW_LEADER_GRP}" "${LEADER_ZONE}" "${OLD_LEADER_GRP}" "${OLD_LEADER_ZONE}"

    # Same-zone case: old VM still in shared IG → remove it so import doesn't split
    if [[ -n "${OLD_LEADER_VM}" && "${OLD_LEADER_GRP}" == "${NEW_LEADER_GRP}" ]]; then
        log "Removing old leader ${OLD_LEADER_VM} from shared instance group ${NEW_LEADER_GRP}…"
        gcloud compute instance-groups unmanaged remove-instances "${NEW_LEADER_GRP}" \
            --zone="${LEADER_ZONE}" --instances="${OLD_LEADER_VM}" \
            --project "${PROJECT_ID}" 2>/dev/null || true
    fi

    # Trap ensures REINDEX_CORE resets and schedulers resume even on failure (idempotent)
    trap cleanup_on_exit EXIT

    pause_solr_schedulers

    log "Enabling REINDEX_CORE in secret…"
    oc -n "${OC_NAMESPACE}" patch secret "${IMPORTER_SECRET}" \
        -p '{"stringData":{"REINDEX_CORE":"True"}}'

    # OC job idempotency guard
    JOB_NAME="namex-solr-importer-${ENV}-deploy-${timestamp}"
    oc -n "${OC_NAMESPACE}" delete job "${JOB_NAME}" --ignore-not-found=true

    log "Triggering importer CronJob…"
    oc -n "${OC_NAMESPACE}" create job \
        --from=cronjob/namex-solr-importer-"${ENV}" \
        "${JOB_NAME}"

    log "Waiting for importer job to complete (up to 90 min)…"
    JOB_DONE=""
    for _attempt in $(seq 1 540); do
        JOB_STATUS=$(oc -n "${OC_NAMESPACE}" get "job/${JOB_NAME}" \
            -o jsonpath='{.status.conditions[?(@.status=="True")].type}' 2>/dev/null || true)
        if echo "${JOB_STATUS}" | grep -q "Complete"; then
            JOB_DONE="complete"
            break
        fi
        if echo "${JOB_STATUS}" | grep -q "Failed"; then
            JOB_DONE="failed"
            break
        fi
        sleep 10
    done

    if [[ "${JOB_DONE}" != "complete" ]]; then
        echo "ERROR: Importer job ${JOB_DONE:-timed out}. Status: ${JOB_STATUS}"
        oc -n "${OC_NAMESPACE}" logs "job/${JOB_NAME}" --tail=30 2>/dev/null || true
        exit 1
    fi

    log "Importer job completed successfully."
    reset_reindex_flag

    # Verify the import actually landed on the new leader before deleting old / creating followers
    log "Verifying documents on new leader ${NEW_LEADER_VM}…"
    IMPORTED_RESP=$(gcloud compute ssh "${NEW_LEADER_VM}" \
        --zone="${LEADER_ZONE}" --project="${PROJECT_ID}" \
        --tunnel-through-iap \
        --command="curl -sf 'http://localhost:8983/solr/name_request/select?q=*:*&rows=0&wt=json'" \
        2>/dev/null || echo '{}')
    IMPORTED_COUNT=$(json_field "${IMPORTED_RESP}" numFound 0)
    if [[ -z "${IMPORTED_COUNT}" || "${IMPORTED_COUNT}" -le 0 ]]; then
        echo "ERROR: New leader ${NEW_LEADER_VM} has no documents after import (numFound=${IMPORTED_COUNT:-0}). Aborting to preserve old leader data."
        exit 1
    fi
    log "New leader has ${IMPORTED_COUNT} documents."
    resume_solr_schedulers

    ########################################
    # DEV ENV → LEADER ONLY
    ########################################
    if [[ "${ENV}" == "dev" ]]; then
        log "DEV environment: follower instance not required. Skipping follower creation."

        # Only delete old after everything succeeds
        if [[ -n "${OLD_LEADER_VM}" ]]; then
            log "Deleting OLD leader: ${OLD_LEADER_VM} (zone: ${OLD_LEADER_ZONE})"
            gcloud compute instances delete "${OLD_LEADER_VM}" --zone="${OLD_LEADER_ZONE}" --project="${PROJECT_ID}" --quiet
        fi

        log "Deployment complete (DEV: leader only)."
        return
    fi

    ########################################
    # TEST/PROD DEPLOY → CREATE FOLLOWER
    ########################################

    log "Creating NEW Follower VM: ${NEW_FOLLOWER_VM}"
    FOLLOWER_ZONE=$(create_vm_in_available_zone "${NEW_FOLLOWER_VM}" "${FOLLOWER_TEMPLATE}" "${FOLLOWER_MACHINE_TYPE}")
    log "Follower created in zone: ${FOLLOWER_ZONE}"

    # Wait for follower Solr core before configuring replication
    wait_for_solr_ready "${NEW_FOLLOWER_VM}" "${FOLLOWER_ZONE}" "name_request_follower"

    log "Setting follower replication properties…"
    retry 5 gcloud compute ssh "${NEW_FOLLOWER_VM}" \
      --zone="${FOLLOWER_ZONE}" --project="${PROJECT_ID}" \
      --tunnel-through-iap \
      --command="curl -sf -X POST -H 'Content-type: application/json' \
        -d '{\"set-user-property\":{\"solr.leaderUrl\": \"http://${NEW_LEADER_INTERNAL_IP}:8983/solr/name_request\"}}' \
        'http://localhost:8983/solr/name_request_follower/config/requestHandler?componentName=/replication'"

    # Wait for follower to fully replicate before adding to backend
    wait_for_replication "${NEW_FOLLOWER_VM}" "${FOLLOWER_ZONE}" "${NEW_LEADER_VM}" "${LEADER_ZONE}" "name_request_follower" "name_request"

    # Zone-specific follower instance group
    FOLLOWER_ZONE_SUFFIX=$(basename "${FOLLOWER_ZONE}" | grep -o '[a-c]$')
    NEW_FOLLOWER_GRP="namex-solr-follower-grp-${ENV}-${FOLLOWER_ZONE_SUFFIX}"
    OLD_FOLLOWER_GRP=""
    if [[ -n "${OLD_FOLLOWER_ZONE}" ]]; then
        OLD_FOLLOWER_ZONE_SUFFIX=$(basename "${OLD_FOLLOWER_ZONE}" | grep -o '[a-c]$')
        OLD_FOLLOWER_GRP="namex-solr-follower-grp-${ENV}-${OLD_FOLLOWER_ZONE_SUFFIX}"
    fi

    log "Adding follower to instance group ${NEW_FOLLOWER_GRP}…"
    ensure_instance_group "${NEW_FOLLOWER_GRP}" "${FOLLOWER_ZONE}"
    gcloud compute instance-groups unmanaged add-instances \
        "${NEW_FOLLOWER_GRP}" \
        --zone "${FOLLOWER_ZONE}" \
        --instances "${NEW_FOLLOWER_VM}" \
        --project "${PROJECT_ID}"

    # Add new to backend (old still serves traffic during transition)
    add_to_backend "${FOLLOWER_BACKEND}" "${NEW_FOLLOWER_GRP}" "${FOLLOWER_ZONE}"

    # Wait for new follower to be healthy BEFORE removing old
    if ! wait_for_healthy_backend "${FOLLOWER_BACKEND}" "${NEW_FOLLOWER_VM}"; then
        rollback_backend "${FOLLOWER_BACKEND}" "${NEW_FOLLOWER_GRP}" "${FOLLOWER_ZONE}"
        log "Cleaning up failed follower VM: ${NEW_FOLLOWER_VM}"
        gcloud compute instances delete "${NEW_FOLLOWER_VM}" --zone="${FOLLOWER_ZONE}" --project="${PROJECT_ID}" --quiet 2>/dev/null || true
        exit 1
    fi

    # New is healthy → safe to remove old backend
    remove_old_backend "${FOLLOWER_BACKEND}" \
        "${NEW_FOLLOWER_GRP}" "${FOLLOWER_ZONE}" "${OLD_FOLLOWER_GRP}" "${OLD_FOLLOWER_ZONE}"

    # Same-zone case: old VM still in shared IG → remove it
    if [[ -n "${OLD_FOLLOWER_VM}" && "${OLD_FOLLOWER_GRP}" == "${NEW_FOLLOWER_GRP}" ]]; then
        log "Removing old follower ${OLD_FOLLOWER_VM} from shared instance group ${NEW_FOLLOWER_GRP}…"
        gcloud compute instance-groups unmanaged remove-instances "${NEW_FOLLOWER_GRP}" \
            --zone="${FOLLOWER_ZONE}" --instances="${OLD_FOLLOWER_VM}" \
            --project="${PROJECT_ID}" 2>/dev/null || true
    fi

    ########################################
    # CLEANUP OLD INSTANCES
    ########################################

    if [[ -n "${OLD_LEADER_VM}" ]]; then
        log "Deleting OLD leader: ${OLD_LEADER_VM} (zone: ${OLD_LEADER_ZONE})"
        gcloud compute instances delete "${OLD_LEADER_VM}" --zone="${OLD_LEADER_ZONE}" --project="${PROJECT_ID}" --quiet
    fi

    if [[ -n "${OLD_FOLLOWER_VM}" ]]; then
        log "Deleting OLD follower: ${OLD_FOLLOWER_VM} (zone: ${OLD_FOLLOWER_ZONE})"
        gcloud compute instances delete "${OLD_FOLLOWER_VM}" --zone="${OLD_FOLLOWER_ZONE}" --project="${PROJECT_ID}" --quiet
    fi

    log "Deployment complete."
}

########################################
# DEPLOY FOLLOWER ONLY (TEST/PROD)
########################################

deploy_follower_instance() {

    timestamp=$(date -u +"%Y-%m-%d--%H%M%S")
    NEW_FOLLOWER_VM="namex-solr-follower-${ENV}-${timestamp}"

    #####################################
    # RESOLVE LEADER INTERNAL IP (read-only)
    #####################################

    log "Finding current leader VM…"
    CURRENT_LEADER_VM=$(gcloud compute instances list \
        --format="value(name)" \
        --filter="name~'^namex-solr-leader-${ENV}-'" \
        --sort-by="~creationTimestamp" \
        --limit=1 \
        --project="${PROJECT_ID}" || true)

    if [[ -z "${CURRENT_LEADER_VM}" ]]; then
        echo "ERROR: No leader VM found for ${ENV}. Cannot deploy follower."
        exit 1
    fi

    CURRENT_LEADER_ZONE=$(get_instance_zone "${CURRENT_LEADER_VM}")
    CURRENT_LEADER_IP=$(gcloud compute instances describe "${CURRENT_LEADER_VM}" \
        --zone "${CURRENT_LEADER_ZONE}" --project "${PROJECT_ID}" \
        --format='value(networkInterfaces[0].networkIP)')

    log "Leader: ${CURRENT_LEADER_VM} (${CURRENT_LEADER_ZONE}) — IP: ${CURRENT_LEADER_IP}"

    #####################################
    # FIND OLD FOLLOWER
    #####################################

    log "Finding current follower VM…"
    OLD_FOLLOWER_VM=$(gcloud compute instances list \
        --format="value(name)" \
        --filter="name~'^namex-solr-follower-${ENV}-'" \
        --sort-by="~creationTimestamp" \
        --limit=1 \
        --project="${PROJECT_ID}" || true)

    OLD_FOLLOWER_ZONE=""
    if [[ -n "${OLD_FOLLOWER_VM}" ]]; then
        OLD_FOLLOWER_ZONE=$(get_instance_zone "${OLD_FOLLOWER_VM}")
    fi

    log "OLD_FOLLOWER_VM=${OLD_FOLLOWER_VM:-none}"

    #####################################
    # CREATE NEW FOLLOWER
    #####################################

    log "Creating NEW Follower VM: ${NEW_FOLLOWER_VM}"
    FOLLOWER_ZONE=$(create_vm_in_available_zone "${NEW_FOLLOWER_VM}" "${FOLLOWER_TEMPLATE}" "${FOLLOWER_MACHINE_TYPE}")
    log "Follower created in zone: ${FOLLOWER_ZONE}"

    # Wait for follower Solr core before configuring replication
    wait_for_solr_ready "${NEW_FOLLOWER_VM}" "${FOLLOWER_ZONE}" "name_request_follower"

    log "Setting follower replication properties…"
    retry 5 gcloud compute ssh "${NEW_FOLLOWER_VM}" \
      --zone="${FOLLOWER_ZONE}" --project="${PROJECT_ID}" \
      --tunnel-through-iap \
      --command="curl -sf -X POST -H 'Content-type: application/json' \
        -d '{\"set-user-property\":{\"solr.leaderUrl\": \"http://${CURRENT_LEADER_IP}:8983/solr/name_request\"}}' \
        'http://localhost:8983/solr/name_request_follower/config/requestHandler?componentName=/replication'"

    # Wait for follower to fully replicate before adding to backend
    wait_for_replication "${NEW_FOLLOWER_VM}" "${FOLLOWER_ZONE}" "${CURRENT_LEADER_VM}" "${CURRENT_LEADER_ZONE}" "name_request_follower" "name_request"

    #####################################
    # SWAP INSTANCE GROUP + BACKEND
    #####################################

    FOLLOWER_ZONE_SUFFIX=$(basename "${FOLLOWER_ZONE}" | grep -o '[a-c]$')
    NEW_FOLLOWER_GRP="namex-solr-follower-grp-${ENV}-${FOLLOWER_ZONE_SUFFIX}"
    OLD_FOLLOWER_GRP=""
    if [[ -n "${OLD_FOLLOWER_ZONE}" ]]; then
        OLD_FOLLOWER_ZONE_SUFFIX=$(basename "${OLD_FOLLOWER_ZONE}" | grep -o '[a-c]$')
        OLD_FOLLOWER_GRP="namex-solr-follower-grp-${ENV}-${OLD_FOLLOWER_ZONE_SUFFIX}"
    fi

    log "Adding follower to instance group ${NEW_FOLLOWER_GRP}…"
    ensure_instance_group "${NEW_FOLLOWER_GRP}" "${FOLLOWER_ZONE}"
    gcloud compute instance-groups unmanaged add-instances \
        "${NEW_FOLLOWER_GRP}" \
        --zone "${FOLLOWER_ZONE}" \
        --instances "${NEW_FOLLOWER_VM}" \
        --project "${PROJECT_ID}"

    add_to_backend "${FOLLOWER_BACKEND}" "${NEW_FOLLOWER_GRP}" "${FOLLOWER_ZONE}"

    if ! wait_for_healthy_backend "${FOLLOWER_BACKEND}" "${NEW_FOLLOWER_VM}"; then
        rollback_backend "${FOLLOWER_BACKEND}" "${NEW_FOLLOWER_GRP}" "${FOLLOWER_ZONE}"
        log "Cleaning up failed follower VM: ${NEW_FOLLOWER_VM}"
        gcloud compute instances delete "${NEW_FOLLOWER_VM}" --zone="${FOLLOWER_ZONE}" --project="${PROJECT_ID}" --quiet 2>/dev/null || true
        exit 1
    fi

    remove_old_backend "${FOLLOWER_BACKEND}" \
        "${NEW_FOLLOWER_GRP}" "${FOLLOWER_ZONE}" "${OLD_FOLLOWER_GRP}" "${OLD_FOLLOWER_ZONE}"

    # Same-zone case: old VM still in shared IG → remove it
    if [[ -n "${OLD_FOLLOWER_VM}" && "${OLD_FOLLOWER_GRP}" == "${NEW_FOLLOWER_GRP}" ]]; then
        log "Removing old follower ${OLD_FOLLOWER_VM} from shared instance group ${NEW_FOLLOWER_GRP}…"
        gcloud compute instance-groups unmanaged remove-instances "${NEW_FOLLOWER_GRP}" \
            --zone="${FOLLOWER_ZONE}" --instances="${OLD_FOLLOWER_VM}" \
            --project="${PROJECT_ID}" 2>/dev/null || true
    fi

    #####################################
    # CLEANUP OLD FOLLOWER
    #####################################

    if [[ -n "${OLD_FOLLOWER_VM}" ]]; then
        log "Deleting OLD follower: ${OLD_FOLLOWER_VM} (zone: ${OLD_FOLLOWER_ZONE})"
        gcloud compute instances delete "${OLD_FOLLOWER_VM}" --zone="${OLD_FOLLOWER_ZONE}" --project="${PROJECT_ID}" --quiet
    fi

    log "Follower deployment complete."
}

########################################
# PARSE FLAGS
########################################
ACTION="${1:-}"
shift || true

LEADER_MACHINE_TYPE=""
FOLLOWER_MACHINE_TYPE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --leader-machine-type=*)
      LEADER_MACHINE_TYPE="${1#*=}"
      shift
      ;;
    --leader-machine-type)
      LEADER_MACHINE_TYPE="$2"
      shift 2
      ;;
    --follower-machine-type=*)
      FOLLOWER_MACHINE_TYPE="${1#*=}"
      shift
      ;;
    --follower-machine-type)
      FOLLOWER_MACHINE_TYPE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

########################################
# MAIN
########################################

case "${ACTION}" in
    build)
        check_build_prereqs
        build_images
        ;;
    tag)
        check_prereqs
        tag_images
        ;;
    deploy)
        check_deploy_prereqs
        deploy_instances
        ;;
    deploy-follower)
        check_prereqs
        deploy_follower_instance
        ;;
    *)
        echo "Usage:"
        echo "  $0 build             # DEV: Build & push leader image only"
        echo "  $0 tag               # Tag images for TEST/PROD"
        echo "  $0 deploy            # Deploy leader only (DEV) or leader+follower (TEST/PROD)"
        echo "  $0 deploy-follower   # Deploy follower only (TEST/PROD)"
        echo ""
        echo "  Options (deploy / deploy-follower):"
        echo "    --leader-machine-type <type>    Override leader machine type (e.g., e2-standard-4)"
        echo "    --follower-machine-type <type>  Override follower machine type (e.g., e2-standard-4)"
        exit 1
        ;;
esac
