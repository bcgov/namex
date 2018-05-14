
##Provision a PostgreSQL database


```bash
oc process -n openshift postgresql-persistent -p POSTGRESQL_USER=namex -p POSTGRESQL_DATABASE=namex -p POSTGRESQL_PASSWORD=<postgres_pwd> -p VOLUME_CAPACITY=250Mi | oc apply  -n <deployment namespace> -f -
```

## connect remotely to DB
```bash
oc get pods --selector name=postgresql
NAME                 READY     STATUS    RESTARTS   AGE
postgresql-2-d7blw   1/1       Running   0          3h

## oc port-forward <pod-name> <local-port>:<remote:port>
oc port-forward postgresql-2-d7blw 15432:5432

## psql <dbname> <username> --host=<hotname> --port=<port>
psql namex <username> --host=127.0.0.1 --port=15432
```
