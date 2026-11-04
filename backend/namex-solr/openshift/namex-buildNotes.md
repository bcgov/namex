# Solr Deployment Notes

Apache Solr is the search index database used by the name examination system.

This documentation describes the process used when recreating the `namex-solr-base` build and image in the
`servicebc-ne-tools` OpenShift project. These steps must be performed before the `solr` build and image can be created.

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

## Creating and Replacing the `namex-solr-base` Build

Creating the `namex-solr-base` build should only need to be once. Replacing the build should only need to be done when
changing the Github repository location.

### Creating the Build

Ensure that your current project is `servicebc-ne-tools`:

```
C:\> oc project servicebc-ne-tools
```

Change directory to the OpenShift template files in your local copy of the `bcgov/namex-solr` repository:

```
C:\> cd \<path>\namex-solr\openshift
C:\<path>\namex-solr\openshift>
```

See below for building from a fork of the `bcgov/namex-solr` repository. If you want to use `bcgov/namex-solr` itself
then generate the configuration file from the template, and pipe the output back into `oc` to replace the build:

```
C:\<path>\namex-solr\openshift> oc process -f templates\namex-solr-base-build.json | oc create -f -
imagestream "namex-solr-base" created
buildconfig "namex-solr-base" created
```

If you want to create from a fork of the `bcgov/namex-solr` repository, generate the configuration file from the
template and pipe the output back into `oc` to replace the build:

```
C:\<path>\namex-solr\openshift> oc process -f templates\namex-solr-base-build.json -p GIT_REPO_URL=https://github.com/<USERNAME>/namex-solr.git | oc create -f -
imagestream "namex-solr-base" created
buildconfig "namex-solr-base" created
```

In the OpenShift Web Console go to the `names examination (tools)` project, and then `Builds` > `Builds`. Wait for the
`namex-solr-base` build to change Status to `Running` and then to `Complete`. You can also check the Created value to
ensure that it is recent. 

In the OpenShift Web Console go to the `names examination (tools)` project, and then `Builds` > `Images`. Click the
`namex-solr-base` image and the tag `Latest` should exist.

## Replacing the `namex-solr-base` Build

*This step is only needed when you want to change the Github repository used for the build. If want to alter the build
process, do so and commit your changes to the repository. Then click the `Start Build` button in the `OpenShift Web
Console` to start a new build.*

The replacement process is nearly identical to the creation process, just follow the creation instructions above except
using `replace` rather than `create` for the final `oc` call.
