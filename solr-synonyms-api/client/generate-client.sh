#!/bin/bash
echo "Namex Synonyms API client generator"
echo "-----------------------------------"

DIR=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)

# Grab our environment variables
source $DIR/../.env

echo "Please enter the URL for the OpenApi spec to use or press enter to use the defaults:"
read OAPI_SPEC_URL

if [[ -z $OAPI_SPEC_URL ]]
then
    echo "No URL provided, using defaults from .env"
    OAPI_SPEC_URL="localhost:"$FLASK_RUN_PORT"/api/v1/swagger.json"
fi

echo "Generating python client for spec at:"
echo $OAPI_SPEC_URL

# Clean the dist folder

echo "Clearing the dist folder"
rm -rf $DIR/dist/.
echo "-----------------------------------"

echo "Generating new API client"
echo "-----------------------------------"

# Download to the OpenApi spec JSON
# TODO: Support other formats
echo "Downloading API spec..."
curl -o $DIR/swagger.json $OAPI_SPEC_URL
# Run swagger-codegen-cli against our client template for Python
echo "Downloading API spec..."
docker run -P --rm -v $DIR:/local swaggerapi/swagger-codegen-cli generate -i /local/swagger.json  -l python -t /local/template/namex -o /local/dist
# Remove the downloaded swagger.json

echo "Cleaning up distribution files"
rm -f $DIR/swagger.json

# Clean out unnecessary files from the distribution
rm -rfv $DIR/dist/.git
rm -fv $DIR/dist/.gitignore

echo "-----------------------------------"
echo "API client generation complete"
echo "-----------------------------------"

echo "Would you like to push the client to a remote repository? [yes / no]"
read PUSH_UPDATE

if [[ $PUSH_UPDATE == 'yes' ]]
then
    echo "Please enter a git repository URL or press enter to use the defaults:"
    read GIT_REMOTE

    if [[ -z "$GIT_REMOTE" ]]
    then
        echo "No git repository URL provided, using defaults from .env"
        GIT_REMOTE=$SYNONYMS_API_CLIENT_REPO_URL
        if [[ -z $GIT_REMOTE ]]
        then
            echo "No git repository URL configured, please set SYNONYMS_API_CLIENT_REPO_URL in your .env"
            exit
        fi
    fi

    cd $DIR/dist

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