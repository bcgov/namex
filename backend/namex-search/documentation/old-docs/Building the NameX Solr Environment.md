*NOTE: this expects you to already have your gcloud setup / permissions to the gcp environment*

SETUP
```
PROJECT=a083gt
```

```
ENV=prod
```

```
PROJECT_ID=$PROJECT-$ENV
```

```
VPC_NETWORK=bcr-vpc-prod
```

```
VPC_HOST_PROJECT=c4hnrd
```

```
VPC_HOST_PROJECT_ID=$VPC_HOST_PROJECT-$ENV
```

```
VPC_SUBNET=bcr-common-prod-montreal
```

```
REGION=northamerica-northeast1
ZONE=northamerica-northeast1-a
```

### API Networking Stuff

Assign internal static IP
```
LB_LEADER_IP=$(gcloud compute addresses create namex-solr-ilb-ip \
  --region="$REGION" \
  --subnet="projects/$VPC_HOST_PROJECT_ID/regions/$REGION/subnetworks/$VPC_SUBNET" \
  --project="$PROJECT_ID" \
  --format="value(address)")

LB_FOLLOWER_IP=$(gcloud compute addresses create namex-solr-follower-ilb-ip \
  --region="$REGION" \
  --subnet="projects/$VPC_HOST_PROJECT_ID/regions/$REGION/subnetworks/$VPC_SUBNET" \
  --project="$PROJECT_ID" \
  --format="value(address)")
```

### Solr Networking stuff
1. Create instance follower/leader instance groups

   ```
   FOLLOWER_GRP_NAME=namex-solr-follower-grp-$ENV
   ```

   ```
   gcloud compute instance-groups unmanaged create $FOLLOWER_GRP_NAME --project=$PROJECT_ID --zone=northamerica-northeast1-a
   ```

   ```
   gcloud compute instance-groups unmanaged set-named-ports $FOLLOWER_GRP_NAME --project=$PROJECT_ID --zone=northamerica-northeast1-a --named-ports=http:8983
   ```

   ```
   LEADER_GRP_NAME=namex-solr-leader-grp-$ENV
   ```

   ```
   gcloud compute instance-groups unmanaged create $LEADER_GRP_NAME --project=$PROJECT_ID --zone=northamerica-northeast1-a
   ```

   ```
   gcloud compute instance-groups unmanaged set-named-ports $LEADER_GRP_NAME --project=$PROJECT_ID --zone=northamerica-northeast1-a --named-ports=http:8983
   ```
2. Create the health check
    ```
    TAGS=namex-solr
    ```

   ```
   HEALTH_CHECK_NAME=namex-solr-health-check-$ENV

   ```

   ```

    gcloud compute health-checks create tcp $HEALTH_CHECK_NAME \
       --region=$REGION \
       --project=$PROJECT_ID \
       --port=8983 \
       --check-interval=5s \
       --timeout=5s \
       --unhealthy-threshold=2 \
       --healthy-threshold=2


   ```
3. Add the firewall rule to allow the health check connection
   ```

   gcloud compute firewall-rules create allow-namex-solr-ilb-hc \
       --priority=1000 \
       --direction=INGRESS \
       --action=ALLOW \
       --rules=tcp:8983 \
       --source-ranges=35.191.0.0/16,130.211.0.0/22 \
       --network=$VPC_NETWORK \
       --target-tags=$TAGS \
       --project=$VPC_HOST_PROJECT_ID

       LB_SUBNET_CIDR=$(gcloud compute networks subnets describe $VPC_SUBNET \
         --region=$REGION \
         --project=$VPC_HOST_PROJECT_ID \
         --format="value(ipCidrRange)")

     gcloud compute firewall-rules create allow-namex-solr-ilb \
         --priority=1000 \
         --direction=INGRESS \
         --action=ALLOW \
         --rules=tcp:8983 \
         --source-ranges=$LB_SUBNET_CIDR \
         --network=$VPC_NETWORK \
         --target-tags=$TAGS \
         --project=$VPC_HOST_PROJECT_ID


   ```
1. Create the follower/leader load balancers via TCP

```
gcloud compute backend-services create namex-solr-leader-backend \
    --protocol=TCP \
    --health-checks=$HEALTH_CHECK_NAME \
    --health-checks-region=$REGION \
    --region=$REGION \
    --load-balancing-scheme=INTERNAL \
    --project=$PROJECT_ID

gcloud compute backend-services add-backend namex-solr-leader-backend \
  --instance-group=$LEADER_GRP_NAME \
  --instance-group-zone=$ZONE \
  --region=$REGION \
  --project=$PROJECT_ID


gcloud compute backend-services create namex-solr-follower-backend \
  --protocol=TCP \
  --health-checks=$HEALTH_CHECK_NAME \
  --health-checks-region=$REGION \
  --region=$REGION \
  --load-balancing-scheme=INTERNAL \
  --project=$PROJECT_ID

gcloud compute backend-services add-backend namex-solr-follower-backend \
  --instance-group=$FOLLOWER_GRP_NAME \
  --instance-group-zone=$ZONE \
  --region=$REGION \
  --project=$PROJECT_ID

gcloud compute forwarding-rules create namex-solr-tcp-ilb-rule \
  --load-balancing-scheme=INTERNAL \
  --network="projects/$VPC_HOST_PROJECT_ID/global/networks/$VPC_NETWORK" \
  --subnet="projects/$VPC_HOST_PROJECT_ID/regions/$REGION/subnetworks/$VPC_SUBNET" \
  --address="$LB_LEADER_IP" \
  --ports=8983 \
  --backend-service=namex-solr-leader-backend \
  --backend-service-region=$REGION \
  --region=$REGION \
  --project=$PROJECT_ID


gcloud compute forwarding-rules create namex-solr-follower-ilb-rule \
  --load-balancing-scheme=INTERNAL \
  --network="projects/$VPC_HOST_PROJECT_ID/global/networks/$VPC_NETWORK" \
  --subnet="projects/$VPC_HOST_PROJECT_ID/regions/$REGION/subnetworks/$VPC_SUBNET" \
  --address="$LB_FOLLOWER_IP" \
  --ports=8983 \
  --backend-service=namex-solr-follower-backend \
  --backend-service-region=$REGION \
  --region=$REGION \
  --project=$PROJECT_ID

```


### SOLR
1. Create the instance templates
   - set variables

     ```
     INSTANCE_TEMPLATE_FOLLOWER=namex-solr-follower-vm-tmpl-$ENV
     ```

     ```
     INSTANCE_TEMPLATE_LEADER=namex-solr-leader-vm-tmpl-$ENV
     ```
     *Set to the default compute service account EMAIL*
     ```
     SERVICE_ACCOUNT=$(gcloud iam service-accounts list --format="value(email)" --filter displayName:"Default compute service account" --project=$PROJECT_ID)
     ```

     ```
     DEVICE_NAME=namex-solr-disk-$ENV
     ```

     ```
     ARTIFACT_REGISTRY_PROJECT=c4hnrd-tools
     ```

     ```
     BOOT_DISK_IMAGE=cos-121-18867-199-38
     ```
     ```
     PATH_TO_STARTUP_SCRIPT=namex-solr/startupscript.txt
     ```

     <!-- For DEV (only has Leader instance)
     ```
     MACHINE_TYPE_LEADER=custom-1-5120
     ```
      ```
     BOOT_DISK_SIZE_LEADER=10GiB
     ``` -->
     <!-- For TEST
     ```
     MACHINE_TYPE_FOLLOWER=custom-1-5120
     ```
     ```
     BOOT_DISK_SIZE_FOLLOWER=10GiB
     ```
      ```
     MACHINE_TYPE_LEADER=custom-1-5120
     ```
      ```
     BOOT_DISK_SIZE_LEADER=10GiB
     ``` -->
     <!-- For SANDBOX
     ```
     MACHINE_TYPE_FOLLOWER=custom-1-6656
     ```
     ```
     BOOT_DISK_SIZE_FOLLOWER=16GiB
     ```
      ```
     MACHINE_TYPE_LEADER=custom-1-6656
     ```
      ```
     BOOT_DISK_SIZE_LEADER=24GiB
     ``` -->
     For PROD
     ```
     MACHINE_TYPE_FOLLOWER=custom-1-8192-ext
     ```
     ```
     BOOT_DISK_SIZE_FOLLOWER=16GiB
     ```
      ```
     MACHINE_TYPE_LEADER=custom-2-10240
     ```
      ```
     BOOT_DISK_SIZE_LEADER=24GiB
     ```

   -  create the templates. UPDATE THE STARTUP SCRIPT BEFORE RUNNING in namex-solr/startupscript.txt
    ```
    gcloud compute instance-templates create $INSTANCE_TEMPLATE_FOLLOWER --project=$PROJECT_ID --machine-type=$MACHINE_TYPE_FOLLOWER --network-interface=network=projects/$VPC_HOST_PROJECT_ID/global/networks/$VPC_NETWORK,subnet=projects/$VPC_HOST_PROJECT_ID/regions/northamerica-northeast1/subnetworks/$VPC_SUBNET,stack-type=IPV4_ONLY,no-address --metadata=google-logging-enabled=true --metadata-from-file=startup-script=$PATH_TO_STARTUP_SCRIPT --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=$SERVICE_ACCOUNT --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append --tags=$TAGS --create-disk=auto-delete=yes,boot=yes,device-name=$DEVICE_NAME,image=projects/cos-cloud/global/images/$BOOT_DISK_IMAGE,mode=rw,size=$BOOT_DISK_SIZE_FOLLOWER,type=pd-ssd --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any

    gcloud compute instance-groups set-named-ports $FOLLOWER_GRP_NAME \
    --named-ports http:8983 \
    --zone=$ZONE \
    --project=$PROJECT_ID


    ```
    UPDATE THE STARTUP SCRIPT AGAIN BEFORE RUNNING in namex-solr/startupscript.txt

    ```
    gcloud compute instance-templates create $INSTANCE_TEMPLATE_LEADER --project=$PROJECT_ID --machine-type=$MACHINE_TYPE_LEADER --network-interface=network=projects/$VPC_HOST_PROJECT_ID/global/networks/$VPC_NETWORK,subnet=projects/$VPC_HOST_PROJECT_ID/regions/northamerica-northeast1/subnetworks/$VPC_SUBNET,stack-type=IPV4_ONLY,no-address --metadata=google-logging-enabled=true --metadata-from-file=startup-script=$PATH_TO_STARTUP_SCRIPT --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=$SERVICE_ACCOUNT --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append --tags=$TAGS --create-disk=auto-delete=yes,boot=yes,device-name=$DEVICE_NAME,image=projects/cos-cloud/global/images/$BOOT_DISK_IMAGE,mode=rw,size=$BOOT_DISK_SIZE_LEADER,type=pd-ssd --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any

    gcloud compute instance-groups set-named-ports $LEADER_GRP_NAME \
    --named-ports http:8983 \
    --zone=$ZONE \
    --project=$PROJECT_ID


    ```
1. Update permissions to allow this environment to pull the image from tools <-- not sure why we need this? maybe to use for pulling image from common-tools
   ```
   gcloud projects add-iam-policy-binding $ARTIFACT_REGISTRY_PROJECT --member serviceAccount:$SERVICE_ACCOUNT --role=roles/artifactregistry.serviceAgent
   ```
2. *Deploy, create, and load the solr VMs
