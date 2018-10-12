# Cron Jobs

Cron Jobs are scheduled jobs that we have running in Openshift.

### Basic Info

We have *two* cron jobs running in our project right now:
>1. `inprogress-update`
>2. `nro-update`

They have an image and a build visible in servicebc-ne-*tools*. 
To check if they are running with Openshift go into **dev**, **test** or **prod** and 
look in Applications >> *Pods* or (with the oc client) use the `oc get cronjobs` command. 
>Each time a cron job runs it will 
create a pod, try accomplishing its task, and then tear down the pod.

**Note**: when a new image is pushed the cron job will pick up the code changes (i.e. changes to any *.py files it uses) 
without being re-created, but it will *not* pick up changes made to its .yml file.

The .yml file for the cron job should reside in: 
>`<context-directory>/openshift/templates`

To change the schedule, name, commands it runs, or the container information (i.e. environment variables, image, etc.):
>1. `edit the .yml file`
>2. `delete the old cron job`
>3. `re-create the cron job using the editted .yml file`

**Note**: you can edit the cron job directly in the oc client, which allows you to skip deleting/re-creating the old
job, however you should still change the .yml file in the repo to keep it consistent/up to date.

### Basic Commands

open *NS* 
>```oc project servicebc-ne-<NS> (tools, dev, test, prod)>```

*view* 
>```oc get cronjobs```

*edit*
>```oc edit cronjobs/<cronjob name>```

*delete*
>```oc delete cronjobs/<cronjob name>```

*create*
>```oc process -f <.yml file> -p ENV_TAG=<(dev, test, or prod)> | oc create -f - ```

>**Note**: if you *don't* specify the ENV_TAG it will default to dev (and therefore run off the image tagged with dev)
