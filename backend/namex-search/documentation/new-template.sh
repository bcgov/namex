#!/usr/bin/env bash
set -euo pipefail

# ============================================================
#  FLAGS
# ============================================================
TEMPLATES_ONLY="false"
UPDATE_VM="false"
if [[ "${1:-}" == "--templates-only" ]]; then
  TEMPLATES_ONLY="true"
elif [[ "${1:-}" == "--update-vm" ]]; then
  UPDATE_VM="true"
fi

# ============================================================
#  CONFIG — change ENV as needed
# ============================================================
ENV="test"   # dev / test / prod
LABEL="Test"
PROJECT="a083gt"
PROJECT_ID="${PROJECT}-${ENV}"
APP="namex"

VPC_NETWORK="bcr-vpc-${ENV}"
VPC_HOST_PROJECT="c4hnrd"
VPC_HOST_PROJECT_ID="${VPC_HOST_PROJECT}-${ENV}"
VPC_SUBNET="bcr-common-${ENV}-montreal"
REGION="northamerica-northeast1"
ZONE="northamerica-northeast1-a"
TAGS="${APP}-solr"
BOOT_DISK_IMAGE="cos-121-18867-199-38"
ARTIFACT_REGISTRY_PROJECT="c4hnrd-tools"
IMAGE_PROJECT="${VPC_HOST_PROJECT}-tools"
IMAGE_REPO="vm-repo"

FOLLOWER_ROLE="follower"
LEADER_ROLE="leader"

FOLLOWER_GRP_NAME="${APP}-solr-${FOLLOWER_ROLE}-grp-${ENV}"
LEADER_GRP_NAME="${APP}-solr-${LEADER_ROLE}-grp-${ENV}"
INSTANCE_TEMPLATE_FOLLOWER="${APP}-solr-${FOLLOWER_ROLE}-vm-tmpl-${ENV}"
INSTANCE_TEMPLATE_LEADER="${APP}-solr-${LEADER_ROLE}-vm-tmpl-${ENV}"

FOLLOWER_IMAGE="name-request-solr-${FOLLOWER_ROLE}"
LEADER_IMAGE="name-request-solr-${LEADER_ROLE}"

DEVICE_NAME="${APP}-solr-disk-$ENV"
PATH_TO_STARTUP_SCRIPT="../${APP}-solr/startupscript.txt"

SERVICE_ACCOUNT="sa-solr-vm@${PROJECT_ID}.iam.gserviceaccount.com"

# ============================================================
#  ENVIRONMENT-SPECIFIC MACHINE TYPES
# ============================================================
if [[ "$ENV" == "dev" ]]; then
  MACHINE_TYPE_FOLLOWER="custom-1-5120"
  BOOT_DISK_SIZE_FOLLOWER="10GiB"
  FOLLOWER_FILTERCACHE_MAXRAM="50"
  FOLLOWER_QRCACHE_MAXRAM="25"
  FOLLOWER_DOCCACHE_MAXRAM="20"
  FOLLOWER_PERSEGCACHE_MAXRAM="30"
  MACHINE_TYPE_LEADER="custom-1-5120"
  BOOT_DISK_SIZE_LEADER="10GiB"
elif [[ "$ENV" == "test" ]]; then
  MACHINE_TYPE_FOLLOWER="custom-1-6656"
  BOOT_DISK_SIZE_FOLLOWER="10GiB"
  FOLLOWER_FILTERCACHE_MAXRAM="50"
  FOLLOWER_QRCACHE_MAXRAM="25"
  FOLLOWER_DOCCACHE_MAXRAM="20"
  FOLLOWER_PERSEGCACHE_MAXRAM="30"
  MACHINE_TYPE_LEADER="custom-1-5120"
  BOOT_DISK_SIZE_LEADER="10GiB"
elif [[ "$ENV" == "sandbox" ]]; then
  MACHINE_TYPE_FOLLOWER="custom-1-6656"
  BOOT_DISK_SIZE_FOLLOWER="24GiB"
  FOLLOWER_FILTERCACHE_MAXRAM="100"
  FOLLOWER_QRCACHE_MAXRAM="50"
  FOLLOWER_DOCCACHE_MAXRAM="30"
  FOLLOWER_PERSEGCACHE_MAXRAM="60"
  MACHINE_TYPE_LEADER="custom-1-6656"
  BOOT_DISK_SIZE_LEADER="24GiB"
elif [[ "$ENV" == "prod" ]]; then
  MACHINE_TYPE_FOLLOWER="e2-standard-8"
  BOOT_DISK_SIZE_FOLLOWER="24GiB"
  FOLLOWER_FILTERCACHE_MAXRAM="2000"
  FOLLOWER_QRCACHE_MAXRAM="500"
  FOLLOWER_DOCCACHE_MAXRAM="200"
  FOLLOWER_PERSEGCACHE_MAXRAM="500"
  MACHINE_TYPE_LEADER="e2-standard-4"
  BOOT_DISK_SIZE_LEADER="40GiB"
fi

# ============================================================
#  COMPUTE JVM MEMORY (50% of machine RAM)
# ============================================================
# Handles standard families (e2-standard-N => N*4GiB) and custom
# types (custom-*-MMMM => MMMM MB total).
compute_jvm_mem() {
  local mt="$1"
  if [[ "$mt" =~ ^e2-standard-([0-9]+)$ ]]; then
    g=$(( ${BASH_REMATCH[1]} * 4 ))
  elif [[ "$mt" =~ ^custom-[0-9]+-([0-9]+)$ ]]; then
    g=$(( (${BASH_REMATCH[1]} / 1024) ))
  else
    echo "ERROR: Unsupported machine type for JVM compute: $mt" >&2
    exit 1
  fi
  g=$(( g / 3 ))
  echo "${g}g"
}

FOLLOWER_JVM_MEM="$(compute_jvm_mem "$MACHINE_TYPE_FOLLOWER")"
LEADER_JVM_MEM="$(compute_jvm_mem "$MACHINE_TYPE_LEADER")"

# ============================================================
#  FIND CURRENT VMs
# ============================================================
echo "➤ Finding current VMs..."
CURRENT_VMS=$(gcloud compute instances list \
  --project="$PROJECT_ID" \
  --filter="name~namex-solr.*${ENV}" \
  --format="value(name)" 2>/dev/null || true)

if [[ -n "$CURRENT_VMS" ]]; then
  echo "  Current VMs: $CURRENT_VMS"
else
  echo "  No existing VMs found."
fi

# ============================================================
#  DELETE OLD VMs (skipped with --templates-only or --update-vm)
# ============================================================
if [[ "$TEMPLATES_ONLY" == "true" || "$UPDATE_VM" == "true" ]]; then
  echo "➤ Skipping VM deletion (--templates-only or --update-vm)."
else
  echo "➤ Deleting old VMs..."
  for VM_NAME in $CURRENT_VMS; do
    # Remove from instance group first
    ROLE=$(echo "$VM_NAME" | grep -o "leader\|follower")
    GRP_NAME="${APP}-solr-${ROLE}-grp-${ENV}"

    gcloud compute instance-groups unmanaged remove-instances "$GRP_NAME" \
      --zone="$ZONE" \
      --instances="$VM_NAME" \
      --project="$PROJECT_ID" 2>/dev/null || true

    gcloud compute instances delete "$VM_NAME" \
      --zone="$ZONE" \
      --project="$PROJECT_ID" \
      --quiet 2>/dev/null || true
    echo "  Deleted: $VM_NAME"
  done
fi

# ============================================================
#  DELETE OLD TEMPLATES
# ============================================================
echo "➤ Deleting old instance templates..."
for TMPL in "$INSTANCE_TEMPLATE_LEADER" "$INSTANCE_TEMPLATE_FOLLOWER"; do
  gcloud compute instance-templates delete "$TMPL" \
    --project="$PROJECT_ID" \
    --quiet 2>/dev/null || true
  echo "  Deleted template: $TMPL"
done

# ============================================================
#  CREATE NEW TEMPLATES
# ============================================================
echo "➤ Creating new leader template..."
gcloud compute instance-templates create "$INSTANCE_TEMPLATE_LEADER" \
  --project="$PROJECT_ID" \
  --machine-type="$MACHINE_TYPE_LEADER" \
  --network-interface=network=projects/$VPC_HOST_PROJECT_ID/global/networks/$VPC_NETWORK,subnet=projects/$VPC_HOST_PROJECT_ID/regions/$REGION/subnetworks/$VPC_SUBNET,stack-type=IPV4_ONLY,no-address \
  --metadata-from-file=startup-script="$PATH_TO_STARTUP_SCRIPT" \
  --metadata=google-logging-enabled=true,role=$LEADER_ROLE,env=$ENV,label=$LABEL,jvm_mem=$LEADER_JVM_MEM,image=$LEADER_IMAGE,image_project=$IMAGE_PROJECT,image_repo=$IMAGE_REPO,zone=$ZONE,block-project-ssh-keys=TRUE \
  --maintenance-policy=MIGRATE \
  --provisioning-model=STANDARD \
  --service-account="$SERVICE_ACCOUNT" \
  --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
  --tags="$TAGS" \
  --create-disk=auto-delete=yes,boot=yes,device-name="$DEVICE_NAME",image=projects/cos-cloud/global/images/$BOOT_DISK_IMAGE,mode=rw,size="$BOOT_DISK_SIZE_LEADER",type=pd-ssd \
  --shielded-secure-boot \
  --shielded-vtpm \
  --shielded-integrity-monitoring

if [[ "$ENV" != "dev" ]]; then
  echo "➤ Creating new follower template..."
  gcloud compute instance-templates create "$INSTANCE_TEMPLATE_FOLLOWER" \
    --project="$PROJECT_ID" \
    --machine-type="$MACHINE_TYPE_FOLLOWER" \
    --network-interface=network=projects/$VPC_HOST_PROJECT_ID/global/networks/$VPC_NETWORK,subnet=projects/$VPC_HOST_PROJECT_ID/regions/$REGION/subnetworks/$VPC_SUBNET,stack-type=IPV4_ONLY,no-address \
    --metadata-from-file=startup-script="$PATH_TO_STARTUP_SCRIPT" \
    --metadata=google-logging-enabled=true,role=$FOLLOWER_ROLE,env=$ENV,label=$LABEL,jvm_mem=$FOLLOWER_JVM_MEM,filtercache_maxram=$FOLLOWER_FILTERCACHE_MAXRAM,qrcache_maxram=$FOLLOWER_QRCACHE_MAXRAM,doccache_maxram=$FOLLOWER_DOCCACHE_MAXRAM,persegcache_maxram=$FOLLOWER_PERSEGCACHE_MAXRAM,image=$FOLLOWER_IMAGE,image_project=$IMAGE_PROJECT,image_repo=$IMAGE_REPO,zone=$ZONE,block-project-ssh-keys=TRUE \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account="$SERVICE_ACCOUNT" \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
    --tags="$TAGS" \
    --create-disk=auto-delete=yes,boot=yes,device-name="$DEVICE_NAME",image=projects/cos-cloud/global/images/$BOOT_DISK_IMAGE,mode=rw,size="$BOOT_DISK_SIZE_FOLLOWER",type=pd-ssd \
    --shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring
fi

# ============================================================
#  UPDATE SHIELDED SETTINGS ON RUNNING VMs (--update-vm only)
# ============================================================
if [[ "$UPDATE_VM" == "true" && -n "$CURRENT_VMS" ]]; then
  echo "➤ Updating shielded settings on running VMs (--update-vm)..."
  for VM_NAME in $CURRENT_VMS; do
    echo "  Stopping $VM_NAME..."
    gcloud compute instances stop "$VM_NAME" \
      --zone="$ZONE" \
      --project="$PROJECT_ID"

    echo "  Enabling Secure Boot on $VM_NAME..."
    gcloud compute instances update "$VM_NAME" \
      --shielded-secure-boot \
      --zone="$ZONE" \
      --project="$PROJECT_ID"

    echo "  Starting $VM_NAME..."
    gcloud compute instances start "$VM_NAME" \
      --zone="$ZONE" \
      --project="$PROJECT_ID"

    echo "  ✔ $VM_NAME updated."
  done
fi

# ============================================================
#  CREATE NEW VMs (skipped with --templates-only or --update-vm)
# ============================================================
if [[ "$TEMPLATES_ONLY" == "true" || "$UPDATE_VM" == "true" ]]; then
  echo "➤ Skipping VM creation (--templates-only or --update-vm)."
else
  NEW_LEADER_VM="${APP}-solr-${LEADER_ROLE}-$(date -u +"%Y-%m-%d--%H%M%S")"

  echo "➤ Creating leader VM: $NEW_LEADER_VM"
  gcloud compute instances create "$NEW_LEADER_VM" \
    --source-instance-template "$INSTANCE_TEMPLATE_LEADER" \
    --zone "$ZONE" \
    --project "$PROJECT_ID"

  gcloud compute instance-groups unmanaged add-instances "$LEADER_GRP_NAME" \
    --zone="$ZONE" \
    --instances="$NEW_LEADER_VM" \
    --project "$PROJECT_ID"

  if [[ "$ENV" != "dev" ]]; then
    NEW_FOLLOWER_VM="${APP}-solr-${FOLLOWER_ROLE}-$(date -u +"%Y-%m-%d--%H%M%S")"

    echo "➤ Creating follower VM: $NEW_FOLLOWER_VM"
    gcloud compute instances create "$NEW_FOLLOWER_VM" \
      --source-instance-template "$INSTANCE_TEMPLATE_FOLLOWER" \
      --zone "$ZONE" \
      --project "$PROJECT_ID"

    gcloud compute instance-groups unmanaged add-instances "$FOLLOWER_GRP_NAME" \
      --zone="$ZONE" \
      --instances="$NEW_FOLLOWER_VM" \
      --project "$PROJECT_ID"
  fi
fi

echo "✔ Done. Templates created with service account: $SERVICE_ACCOUNT"