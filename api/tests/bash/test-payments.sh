#!/bin/bash
# Note this requires JQ for handling JSON
PAYMENT_SVC_AUTH_URL="fill this in!"
PAYMENT_SVC_AUTH_CLIENT_ID="fill this in!"
PAYMENT_SVC_URL="fill this in!"
PAYMENT_SVC_CLIENT_SECRET="fill this in!"

invoice_id=6074
token=""

function get_client_credentials {
    result=$(curl --request POST \
      --url $PAYMENT_SVC_AUTH_URL \
      --header "Content-Type: application/x-www-form-urlencoded" \
      --data grant_type=client_credentials \
      --data client_id=$PAYMENT_SVC_AUTH_CLIENT_ID \
      --data client_secret=$PAYMENT_SVC_CLIENT_SECRET)
    echo $result | jq --raw-output '.access_token'
}

function test_refunds {
    echo "test refunds"
    echo $token
    curl -v -i -X POST -H "Authorization: Bearer $token" -H "Content-Type: application/json" https://pay-api-dev.pathfinder.gov.bc.ca/api/v1/payment-requests/$invoice_id/refunds
}

token=$(get_client_credentials) && test_refunds
