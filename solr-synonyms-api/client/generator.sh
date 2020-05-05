#!/bin/bash
echo "Namex Synonyms API client generator"
echo "-----------------------------------"

echo "Please enter the URL for the OpenApi spec to use:"
read OAPI_SPEC_URL

if [[ -z $OAPI_SPEC_URL ]]
then
    OAPI_SPEC_URL="SOLR_SYNONYMS_API_URL"
fi

echo "Generating python client for OpenApi spec at:" $OAPI_SPEC_URL

# Download to the OpenApi spec JSON
# TODO: Support other formats
curl -o swagger.json $OAPI_SPEC_URL
# Run swagger-codegen-cli against our client template for Python
docker run -P --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -i /local/swagger.json  -l python -t /local/template -o /local/dist
# Remove the downloaded swagger.json
rm -f swagger.json