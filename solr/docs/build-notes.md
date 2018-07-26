# Solr Deployment Notes

Apache Solr is the search index database used by the name examination system.

This documentation describes the process used when recreating the `solr` build and image in the `servicebc-ne-tools`
OpenShift project. Before creating these Solr artifacts, the `namex-solr-base` image must exist in the OpenShift
project `servicebc-ne-tools`. See the `bcgov/namex-solr` on GitHub for details if this image does not exist.

This documentation assumes that `oc.exe` from OpenShift Origin Client Tools has been installed and that the user has
an account on the Pathfinder OpenShift cluster.

## Log in to OpenShift

Log into the [OpenShift Web Console](https://console.pathfinder.gov.bc.ca:8443/console). Click the drop-down for your
username in the upper-right corner, and select `Copy Login Command`. Paste the command into your shell:

```
C:\> oc login https://console.pathfinder.gov.bc.ca:8443 --token=<blahblahblah>
Logged into "https://console.pathfinder.gov.bc.ca:8443" as "<username>" using the token provided.

You have access to the following projects and can switch between them with 'oc project <projectname>':

    servicebc-ne-dev
    servicebc-ne-test
  * servicebc-ne-tools

Using project "servicebc-ne-tools".
```

(Note that you could also run `oc login` and enter the same credentials).

## Creating Solr

Creating Solr in a new environment is a fairly rare occurrence. It only needs to happen once, and subsequent changes
are picked up by *replacing*, below. As the creation process is nearly identical to the replacement process, just
follow the replacement instructions except using `create` rather than `replace` for the final `oc` call.

## Replacing Solr

*This step is used when the `solr` build already exists in the OpenShift project `servicebc-ne-tools`, but it needs
to be updated.*

### Replacing the Build

Ensure that your current project is `servicebc-ne-tools`:

```
C:\> oc project servicebc-ne-tools
```

Change directory to the OpenShift files for Solr in your local copy of the `bcgov/namex` repository:

```
C:\> cd \<path>\namex\solr\openshift
C:\<path>\namex\solr\openshift>
```

Generate the configuration file from the template and the parameters, and pipe the output back into `oc` to replace
the build:

```
C:\<path>\namex\solr\openshift> oc process -f templates\solr-build.json --param-file=solr-build.param | oc replace -f -
imagestream "solr" replaced
buildconfig "solr" replaced
```

In the OpenShift Web Console go to the `names examination (tools)` project, and then `Builds` > `Builds`. Wait for the
`solr` build to change Status to `Running` and then to `Complete`. You can also check the Created value to ensure that
it is recent. 

In the OpenShift Web Console go to the `names examination (tools)` project, and then `Builds` > `Images`. Click the
`solr` image and the tag `Latest` should now have been updated. The image needs to be pushed in order to get it into a
specific environment.

## Tagging an Image

A new Solr image must be tagged before it is deployed for a given *ENV* (`dev`, `test`, or `prod`):

```
C:\> oc tag servicebc-ne-tools/solr:latest servicebc-ne-tools/solr:ENV
Tag solr:ENV set to servicebc-ne-tools/solr@sha256:1d39a55e77076835a67e38ff01cc188cdc713839c96a19c4a14d92e124c269d2.
```

## Deploy

When deploying to *<ENV>* (dev / test / prod) ensure that your current project is `servicebc-ne-<ENV>`. For example, to
deploy to dev:

```
C:\> oc project servicebc-ne-dev
```

Change directory to the OpenShift files for Solr in your local copy of the `bcgov/namex` repository:

```
C:\> cd \<path>\namex\solr\openshift
C:\<path>\namex\solr\openshift>
```

Generate the configuration file from the template and the parameters for your specific environment (dev / test / prod),
and pipe the output back into `oc` to replace the build. For example, to deploy to dev:

```
C:\<path>\namex\solr\openshift> oc process -f templates/solr-deploy.json --param-file=solr-deploy.dev.param | oc create -f -
service "solr" created
route "solr" created
persistentvolumeclaim "solr" created
deploymentconfig "solr" created
```



.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.








#### TODO: Clean up below and move to the above.
 

* Need  image.  See TheOrgBook/docker/manage for original "solr-base" build files.

created templates/solr-build.json

* BUILDNOTES for namex-solr
As per the project documentation but build will only work for local OpenShift

* Pipeline
* Adapted from https://github.com/BCDevOps/openshift-tools/blob/master/provisioning/pipeline/create-pipeline.sh
oc process -f solr-pipeline-build.json --param-file=solr-pipeline.param | oc create -f -

* Extracting a template from OpenShift
EXAMPLE: extracting a deployment config

oc export --as-template=solr-deploy dc solr-names -o json
--as-template=solr-deploy   is the name of the root object
dc                          is deployment config
solr-names                  is the name of the deployment config
-o json                     specifies json as the output format
