#!/bin/bash
SCRIPT_DIR=$(dirname $0)
export MSYS_NO_PATHCONV=1

# ===================================================================================================
# Funtions
# ---------------------------------------------------------------------------------------------------
usage (){
  echo "========================================================================================"
  echo "Creates a Solr test project in OpenShift"
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0} <project_name> <git_ref> <git_uri>"
  echo
  echo "Where:"
  echo " - <project_name> is the name of the openshift project."
  echo " - <git_ref> is GitHub ref to use."
  echo " - <git_uri> is the GitHub repo to use."
  echo
  echo "Examples:"
  echo "${0} solr master https://github.com/bcgov/openshift-solr.git"
  echo "========================================================================================"
  exit 1
}

exitOnError (){
  rtnCd=$?
  if [ ${rtnCd} -ne 0 ]; then
	echo "An error has occurred.!  Please check the previous output message(s) for details."
    exit ${rtnCd}
  fi
}

isLocalCluster (){
  rtnVal=$(oc project | grep //10.0)
  if [ -z "$rtnVal" ]; then
    # Not a local cluster ..."
	return 1
  else
    # Is a local cluster ..."
	return 0
  fi
}
# ===================================================================================================

# ===================================================================================================
# Setup
# ---------------------------------------------------------------------------------------------------
if [ -z "${1}" ]; then
  usage
elif [ -z "${2}" ]; then
  usage  
elif [ -z "${3}" ]; then
  usage
elif [ ! -z "${4}" ]; then
  usage
else
  PROJECT_NAMESPACE=$1
  GIT_REF=$2
  GIT_URI=$3
fi
# ===================================================================================================

if ! isLocalCluster; then
  echo "This script can only be run on a local cluster!"
  exit 1
fi

./createLocalProject.sh ${PROJECT_NAMESPACE} "Solr" "Solr Test Project"
exitOnError

./generateBuilds.sh ${PROJECT_NAMESPACE} ${GIT_REF} ${GIT_URI}
exitOnError

./generateDeployments.sh ${PROJECT_NAMESPACE} latest ${PROJECT_NAMESPACE}
exitOnError