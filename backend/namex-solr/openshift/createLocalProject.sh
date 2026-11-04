#!/bin/bash
SCRIPT_DIR=$(dirname $0)

# ===================================================================================================
# Funtions
# ---------------------------------------------------------------------------------------------------
usage (){
  echo "========================================================================================"
  echo "Creates a local OpenShift project."
  echo
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0} <project_namespace> <displayname> <description>"
  echo
  echo "Where:"
  echo " - <project_namespace> the root namespace for the project set."
  echo " - <displayname> The display name for the project set."
  echo " - <description> The description of the project set."
  echo
  echo "Examples:"
  echo "${0} solr \"Solr\" \"Solr Test Project\""
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

createProject (){
  namespace=$1
  display_name=$2
  description=$3
  
  oc new-project ${namespace} --display-name="${display_name}" --description="${description}"
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

projectExists (){
  project=$1
  rtnVal=$(oc projects | grep ${project})
  if [ -z "$rtnVal" ]; then
    # Project does not exist ..."
	return 1
  else
    # Project exists ..."
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
  DISPLAY_NAME=$2
  DESCRIPTION=$3
fi
# ===================================================================================================

if ! isLocalCluster; then
  echo "This script can only be run on a local cluster!"
  exit 1
fi

if ! projectExists ${PROJECT_NAMESPACE}; then
  createProject ${PROJECT_NAMESPACE} "${DISPLAY_NAME}" "${DESCRIPTION}"
  exitOnError
else
  echo "${PROJECT_NAMESPACE} exists ..."
fi