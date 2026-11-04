gcloud logging metrics create solr_backend_unhealthy \
  --project=google-mpf-547144339658 \
  --description="Solr backend unhealthy (leader or follower)" \
  --log-filter='logName="projects/a083gt-prod/logs/compute.googleapis.com%2Fhealthchecks"
AND resource.type="gce_instance_group"
AND (resource.labels.instance_group_name="namex-solr-leader-grp-prod"
     OR resource.labels.instance_group_name="namex-solr-follower-grp-prod")
AND jsonPayload.healthCheckProbeResult.healthState="UNHEALTHY"'

gcloud logging metrics create solr_health_unhealthy \
  --project=google-mpf-547144339658 \
  --description="Any health check failure (Solr, Docker, Disk)" \
  --log-filter='logName="projects/a083gt-prod/logs/gcplogs-docker-driver"
AND resource.type="gce_instance"
AND jsonPayload.message:"HEALTH CHECK FAILED"'