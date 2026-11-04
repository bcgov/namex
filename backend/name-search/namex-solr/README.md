# Application Name

BC Registries NameX Solr

## Technology Stack Used

- Apache Solr
- Docker

### Development Setup

1. Pull the base solr docker image

- `docker pull solr:9.10.1`

2. Run your solr containers

- if first time or need to pickup new solr changes outside of /solr/name_request directory:
  - Build leader image: `make build-local`
  - Run leader image: `docker run -d -p 8863:8983 --name name-request-solr-leader-local name-request-solr-local` (it will be available on port 8863)
    _NOTE: if you want the data to persist then add `-v $PWD/solr/name-request:/var/solr/data` (do NOT do this for the solr instance used for api unit tests)_
  - Optional: setup follower node
    - Get leader IP: `docker inspect name-request-solr-leader-local | grep IPAddress`
    - Use the docker IP to set the leader url: `export LEADER_URL=http://leader_IP:8863/solr/name_request`
    - Build the follower image: `make build-follower`
    - Run follower image: `docker run -d -p 8864:8983 --name name-request-solr-follower-local name-request-solr-follower` (it will be available on port 8864)
    - Add docker network so that follower can poll from leader:
      - `docker network create solr`
      - `docker network connect solr name-request-solr-leader-local`
      - `docker network connect solr name-request-solr-follower-local`
- else
  - `docker start name-request-solr-leader-local`

3. Check logs for errors

- `docker logs name-request-solr-leader-local`

4. Go to admin UI in browser and check the solr core is there (it will be empty)

- http://localhost:8863/solr
