#!/bin/bash
echo "Swagger / OpenApi3 API client generator"
echo "---------------------------------------"

SCRIPT_DIR=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT_DIR=${SCRIPT_DIR}/../

echo ${ROOT_DIR}

# Grab our environment variables
source ${SCRIPT_DIR}/.env

function is_url () {
    if [[ `curl -s --head "$1" | head -n 1 | grep "HTTP/[1-3].[0-9] [23].."` ]]
    then echo "true"; fi
}

# Set the source for the OpenApi spec
echo "Please enter the URL / file name for the OpenApi spec to use or press enter to use the defaults:"
if [[ -z ${API_SPEC_SRC} ]]
then
    echo "[default: none]"
else
    echo "[default: "${API_SPEC_SRC}"]"
fi

read OAPI_SPEC_SRC

if [[ -z ${OAPI_SPEC_SRC} ]]
then
    echo "No URL / file name provided, using defaults from .env"
    OAPI_SPEC_SRC=${API_SPEC_SRC}
fi

# Set the VERSION of the OpenApi spec
echo "Please choose a version of OpenApi to use: [2 / 3]"
if [[ -z ${DEFAULT_OPEN_API_VERSION} ]]
then
    echo "[default: none]"
else
    echo "[default: "${DEFAULT_OPEN_API_VERSION}"]"
fi

read OPEN_API_VERSION
if [[ -z ${OPEN_API_VERSION} ]]
then
    OPEN_API_VERSION=${DEFAULT_OPEN_API_VERSION}
fi

# Set the FORMAT of the OpenApi spec file
echo "What format is the spec in?: [yml / json]"
if [[ -z ${DEFAULT_SPEC_FORMAT} ]]
then
    echo "[default: none]"
else
    echo "[default: "${DEFAULT_SPEC_FORMAT}"]"
fi

read SPEC_FORMAT
if [[ -z ${SPEC_FORMAT} ]]
then
    SPEC_FORMAT=${DEFAULT_SPEC_FORMAT}
fi

# Set the TEMPLATE
echo "Choose a template to use: [oapi2 /  oapi3 / <custom>]"
if [[ -z ${DEFAULT_TEMPLATE_DIR} ]]
then
    echo "[default: none]"
else
    echo "[default: ${DEFAULT_TEMPLATE_DIR}]"
fi

read TEMPLATE_DIR
if [[ -z ${TEMPLATE_DIR} ]]
then
    if [[ ${OPEN_API_VERSION} == '3'  ]]
        then
            TEMPLATE_DIR=${OAPI3_TEMPLATE_DIR}
    elif [[ ${OPEN_API_VERSION} == '2'  ]]
        then
            TEMPLATE_DIR=${OAPI2_TEMPLATE_DIR}
    fi

fi

echo "Generating python client for spec at [${OAPI_SPEC_SRC}] using the ${TEMPLATE_DIR} template"

# Clean the dist folder
echo "Clearing the dist folder"
rm -rf ${SCRIPT_DIR}/dist/.
echo "-----------------------------------"

echo "Generating new API client"
echo "-----------------------------------"

SPEC_FILE_NAME="downloaded-api-spec"
IS_VALID_URL=$(is_url ${OAPI_SPEC_SRC})
if [[ ${IS_VALID_URL} == true ]]
then
    # Download the OpenApi spec JSON
    echo "Downloading API spec..."
    curl -vo ${SCRIPT_DIR}/specs/${SPEC_FILE_NAME}.${SPEC_FORMAT} ${OAPI_SPEC_SRC}
else
    SPEC_FILE_NAME=${OAPI_SPEC_SRC}
    echo "Using API spec [${SCRIPT_DIR}/specs/${SPEC_FILE_NAME}.${SPEC_FORMAT}]"
fi

# Run swagger-codegen-cli against our client template for Python
if [[ ${OPEN_API_VERSION} == '2' ]]
    then
        echo "docker run -P --rm -v ${SCRIPT_DIR}:/local swaggerapi/swagger-codegen-cli generate -i /local/specs/${SPEC_FILE_NAME}.${SPEC_FORMAT}  -l python -t /local/template/${TEMPLATE_DIR} -o /local/dist"
        docker run -P --rm -v ${SCRIPT_DIR}:/local swaggerapi/swagger-codegen-cli generate -i "/local/specs/${SPEC_FILE_NAME}.${SPEC_FORMAT}"  -l python -t "/local/template/${TEMPLATE_DIR}" -o "/local/dist"
elif [[ ${OPEN_API_VERSION} == '3' ]]
    then
        echo "run -P --rm -v ${SCRIPT_DIR}:/local openapitools/openapi-generator-cli generate -i /local/specs/${SPEC_FILE_NAME}.${SPEC_FORMAT} -g python -t /local/template/${TEMPLATE_DIR} -o /local/dist"
        docker run -P --rm -v ${SCRIPT_DIR}:/local openapitools/openapi-generator-cli generate -i "/local/specs/${SPEC_FILE_NAME}.${SPEC_FORMAT}" -g python -t "/local/template/${TEMPLATE_DIR}" -o "/local/dist"
fi

if [[ ${IS_VALID_URL} == true ]]
then
    # Remove the downloaded swagger.json
    echo "Cleaning up distribution files"
    rm -f ${SCRIPT_DIR}/specs/${SPEC_FILE_NAME}.${SPEC_FORMAT}
fi

# Clean out unnecessary files from the distribution
rm -rfv ${SCRIPT_DIR}/dist/.git
rm -fv ${SCRIPT_DIR}/dist/.gitignore

echo "-----------------------------------"
echo "API client generation complete"
echo "-----------------------------------"

echo "Would you like to push the client to a remote repository? [yes / no]"
read PUSH_UPDATE

if [[ ${PUSH_UPDATE} == 'yes' ]]
then
    echo "Please enter a git repository URL or press enter to use the defaults:"
    if [[ -z ${API_CLIENT_REPO_URL} ]]
    then
        echo "[default: none]"
    else
        echo "[default: ${API_CLIENT_REPO_URL}]"
    fi

    read GIT_REMOTE

    if [[ -z "${GIT_REMOTE}" ]]
    then
        if [[ -z ${API_CLIENT_REPO_URL} ]]
        then
            echo "No git repository URL configured, please set API_CLIENT_REPO_URL in your .env"
            exit
        else
            echo "No git repository URL provided, using default from .env"
            GIT_REMOTE=${API_CLIENT_REPO_URL}
        fi
    fi

    echo "Please enter the name of the branch you would like to commit to:"
    echo "[(default) test-codegen]"

    read GIT_REMOTE_BRANCH

    if [[ -z ${GIT_REMOTE_BRANCH} ]]
    then
        GIT_REMOTE_BRANCH="test-codegen"
    fi

    mkdir -p ${SCRIPT_DIR}/dist
    cd ${SCRIPT_DIR}/dist

    git init

    GIT_REMOTE="${GIT_REMOTE}.git"
    echo "Adding git remote:${GIT_REMOTE}"

    git remote add origin ${GIT_REMOTE}

    git checkout -b ${GIT_REMOTE_BRANCH}
    git add . --verbose

    CUR_TIMESTAMP=$(date)
    git commit -m "[OpenApi Client Generator] Automatic update - ${CUR_TIMESTAMP}."
    echo awk 'FNR <= 1' | git log
    # TODO: Tag versions if necessary
    # git tag -a v2.0 -m 'version 2.0'

    git push --set-upstream -f origin ${GIT_REMOTE_BRANCH}
fi