# Containerized SOLR On OpenShift
Apache SOLR makes it easy to add search capability into your apps.  SOLR is a search server (backed by the Lucene search library).  This repository provides a way for you to take advantage of that in OpenShift.

The BC Registries Names Examination project created the NAMEX version of this image with:
* some minor modifications to the startup scripts to accommodate starting with multiple cores. Cores can be passed in as a comma delimited list.
* addition of the Solr-JDBC library (v2.3.8) to allow reading of the synonyms from a database table.

## There are 2 distinct parts to this repo:
   
### (1) A Dockerfile

Which overrides the [official SOLR image][2] to tweak a few things in order to run SOLR efficiently on OpenShift.  

### (2) S2I scripts

Which allow you to easily push your project specific configuration files into the SOLR container.

## How to use all of this with your apps
Sounds cool right?  It is.  And here's how you can use it.

### Quick Start
* Bring up a local OpenShift cluster.
  * There are some [Chocolatey Scripts](https://github.com/WadeBarnes/dev-tools/tree/master/chocolatey) that make it very easy to do this on Windows.
* Run the `buildLocalProject.sh` script in the `openshift` directory.

This will create a **Solr** project and generate all of the build and deployment configurations needed for a working Solr instance complete with a core configured from source.

### If you just want to try running SOLR in OpenShift...

Create the SOLR app from a Docker image
`> oc new-app dudash/openshift-solr --name=solr-imageonly-demo`

Now you can access it via the route that was automatically exposed on port 8983 and whereever your OpenShift apps route (e.g. openshift-solr-myproject.127.0.0.1.nip.io).  Note: this won't autogenerate a SOLR core.

### If you want to provide configuration in an automated way...
* Create a repo
* Create a folder called `solr/autocore/conf` and add SOLR config files for your desired SOLR configuration
  (Refer to the sample in the project).
* Wire up your build configuration to point to the repo a configuration.  Refer to the script and template samples in the `openshift` directory.

### The S2I process
This repo doesn't require [the s2i tool](https://github.com/openshift/source-to-image) to build the image.  However, if you look into the Dockerfile, it does set some s2i LABELS in order for OpenShift to be able to use it as an s2i builder image.

#### assemble script
Refer to the documentation in the script for details.

#### run script
Refer to the documentation in the script for details.

## Want to help?
If you find and issues, go ahead and write them up.  If you want to submit some code changes, please see the [CONTRIBUTING][3] docs.


[1]: https://github.com/docker-solr/docker-solr
[2]: https://store.docker.com/images/f4e3929d-d8bc-491e-860c-310d3f40fff2?tab=description
[3]: ./CONTRIBUTING.md
