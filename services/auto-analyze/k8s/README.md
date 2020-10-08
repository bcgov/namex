# create the deployment config

```bash
oc process -f templates/deploy.json -p deploy.dev.template.param  | oc create -f -
```
