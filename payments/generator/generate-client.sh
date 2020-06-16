#!/bin/bash
echo "Service BC Pay API client generator"
echo "---------------------------------------"

SCRIPT_DIR=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT_DIR=$SCRIPT_DIR/../

# Grab our environment variables
source $ROOT_DIR/.env

echo "Please enter the URL for the OpenApi spec to use or press enter to use the defaults:"
echo "["API_SPEC_URL"]"

read OAPI_SPEC_URL

if [[ -z $OAPI_SPEC_URL ]]
then
    echo "No URL provided, using defaults from .env"
    # OAPI_SPEC_URL="localhost:"$FLASK_RUN_PORT"/api/v1/swagger.yml"
    OAPI_SPEC_URL=$API_SPEC_URL
fi

echo "Generating python client for spec at:"
echo $OAPI_SPEC_URL

# Clean the dist folder

echo "Clearing the dist folder"
rm -rf $SCRIPT_DIR/dist/.
echo "---------------------------------------"

echo "Generating new API client"
echo "---------------------------------------"

# Download to the OpenApi spec JSON
# TODO: Support other formats
echo "Downloading API spec..."
curl -o $SCRIPT_DIR/swagger.yml $OAPI_SPEC_URL
# Run swagger-codegen-cli against our client template for Python
echo "Downloading API spec..."
docker run -P --rm -v $SCRIPT_DIR:/local openapitools/openapi-generator-cli generate -i /local/swagger.yml -g python -t /local/template -o /local/dist
# Remove the downloaded swagger.yml

echo "Cleaning up distribution files"
rm -f $SCRIPT_DIR/swagger.yml

# Clean out unnecessary files from the distribution
rm -rfv $SCRIPT_DIR/dist/.git
rm -fv $SCRIPT_DIR/dist/.gitignore

echo "Clearing the client folder"
rm -rf $ROOT_DIR/client/.

echo "Copy files to client dir"
cp -R $SCRIPT_DIR/dist/. $ROOT_DIR/client

echo "Clearing the dist folder: "$SCRIPT_DIR/dist

rm -rfv $SCRIPT_DIR/dist

echo "---------------------------------------"
echo "API client generation complete"
echo "---------------------------------------"

echo "Would you like to push the client to a remote repository? [yes / no]"
read PUSH_UPDATE

if [[ $PUSH_UPDATE == 'yes' ]]
then
    echo "Please enter a git repository URL or press enter to use the defaults:"
    read GIT_REMOTE

    if [[ -z "$GIT_REMOTE" ]]
    then
        echo "No git repository URL provided, using defaults from .env"
        GIT_REMOTE=$API_CLIENT_REPO_URL
        if [[ -z $GIT_REMOTE ]]
        then
            echo "No git repository URL configured, please set API_CLIENT_REPO_URL in your .env"
            exit
        fi
    fi

    cd $SCRIPT_DIR/dist

    git init

    GIT_REMOTE=$GIT_REMOTE".git"
    echo "Adding git remote:"$GIT_REMOTE

    git remote add origin $GIT_REMOTE

    echo "Please enter the name of the branch you would like to commit to [(default) test-codegen]:"
    read GIT_REMOTE_BRANCH

    if [[ -z $GIT_REMOTE_BRANCH ]]
    then
        GIT_REMOTE_BRANCH="test-codegen"
    fi

    git checkout -b $GIT_REMOTE_BRANCH
    git add .

    git commit -m "Automatic update."

    # TODO: Tag versions if necessary
    # git tag -a v2.0 -m 'version 2.0'

    git push --set-upstream -f origin $GIT_REMOTE_BRANCH
fi