# Solr Deployment Notes

Apache Solr is the search index database used by the name examination system.

This documentation describes the process used when recreating the `solr` build and image in the `servicebc-ne-tools`
OpenShift project. Before creating these Solr artifacts, the `namex-solr-base` image must exist in the OpenShift
project `servicebc-ne-tools`. See the `bcgov/namex-solr` on GitHub for details if this image does not exist.

This documentation assumes that `oc.exe` from OpenShift Origin Client Tools has been installed and that the user is
either running Minishift locally or has an account on the Pathfinder OpenShift cluster.

## Log in to OpenShift

Log into the `OpenShift Web Console`. Click the drop-down for your username in the upper-right corner, and select
`Copy Login Command`. Paste the command into your shell:

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


## TODO: configmap

## Creating and Replacing the `solr` Build

Creating the `solr` build should only need to be once. Replacing the build should only need to be done when changing
the Github repository location.

### Creating the Build

Ensure that your current project is `servicebc-ne-tools`:

```
C:\> oc project servicebc-ne-tools
```

Change directory to the OpenShift files for Solr in your local copy of the `bcgov/namex` repository:

```
C:\> cd \<path>\namex\solr\openshift
C:\<path>\namex\solr\openshift>
```

See below for building from a fork of the `bcgov/namex` repository. If you want to use `bcgov/namex` itself then
generate the configuration file from the template, and pipe the output back into `oc` to replace the build:

```
C:\<path>\namex\solr\openshift> oc process -f templates\solr-build.json --param-file=solr-build.param | oc create -f -
imagestream "solr" created
buildconfig "solr" created
```

If you want to create from a fork of the `bcgov/namex-solr` repository, generate the configuration file from the
template and pipe the output back into `oc` to replace the build:

```
C:\<path>\namex-solr\openshift> oc process -f templates\solr-build.json -p GIT_REPO_URL=https://github.com/<USERNAME>/namex-solr.git | oc create -f -
warning: Template parameter "GIT_REPO_URL" already defined, ignoring value from file "solr-build.param"
imagestream "solr" created
buildconfig "solr" created
```

In the OpenShift Web Console go to the `names examination (tools)` project, and then `Builds` > `Builds`. Wait for the
`solr` build to change Status to `Running` and then to `Complete`. You can also check the Created value to ensure that
it is recent. 

In the OpenShift Web Console go to the `names examination (tools)` project, and then `Builds` > `Images`. Click the
`solr` image and the tag `Latest` should now have been updated. The image needs to be tagged in order to get it into a
specific environment.

### Replacing the `solr` Build

*This step is only needed when you want to change the Github repository used for the build. If want to alter the build
process, do so and commit your changes to the repository. Then click the `Start Build` button in the `OpenShift Web
Console` to start a new build.*

The replacement process is nearly identical to the creation process, just follow the creation instructions above except
using `replace` rather than `create` for the final `oc` call.

## Deploy

When deploying to `<ENV>` (dev / test / prod) ensure that your current project is `servicebc-ne-<ENV>`. For example, to
deploy to dev:

```
C:\> oc project servicebc-ne-dev
```

Change directory to the OpenShift files for Solr in your local copy of the `bcgov/namex` repository:

```
C:\> cd \<path>\namex\solr\openshift
C:\<path>\namex\solr\openshift>
```

See instructions for Minishift below, but when deploying to the Pathfinder Openshift cluster: generate the
configuration file from the template and the parameters for your specific environment (dev / test / prod), and pipe the
output back into `oc` to replace the build. For example, to deploy to dev:

```
C:\<path>\namex\solr\openshift> oc process -f templates/solr-deploy.json --param-file=solr-deploy.dev.param | oc create -f -
service "solr" created
route "solr" created
persistentvolumeclaim "solr" created
deploymentconfig "solr" created
```

For Minishift we don't have Gluster for a filesystem, so we need a different deployment file:

```
C:\<path>\namex\solr\openshift> oc process -f templates/solr-deploy-local.json --param-file=solr-deploy.dev.param -p APPLICATION_DOMAIN=192.168.99.100.nip.io | oc create -f -
warning: Template parameter "APPLICATION_DOMAIN" already defined, ignoring value from file "solr-deploy.dev.param"
service "solr" created
route "solr" created
persistentvolumeclaim "solr-cores" created
persistentvolumeclaim "solr-trademarks" created
deploymentconfig "solr" created
```

## Tagging an Image

When a new Solr image is tagged for `dev` or `test`, it will be automatically deployed:

```
C:\> oc tag servicebc-ne-tools/solr:latest servicebc-ne-tools/solr:dev
Tag solr:ENV set to servicebc-ne-tools/solr@sha256:1d39a55e77076835a67e38ff01cc188cdc713839c96a19c4a14d92e124c269d2.
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

TODO: create a new route name solr2, hostname 192.168.99.100.nip.io, Secure route, Insecure: redirect. Visit
https://192.168.99.100.nip.io

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
