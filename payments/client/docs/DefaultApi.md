# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_api_v1_payment_requests_payment_identifier**](DefaultApi.md#delete_api_v1_payment_requests_payment_identifier) | **DELETE** /api/v1/payment-requests/{payment_identifier} | 


# **delete_api_v1_payment_requests_payment_identifier**
> delete_api_v1_payment_requests_payment_identifier(payment_identifier)



DELETE payment request

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    payment_identifier = 'payment_identifier_example' # str | 

    try:
        api_instance.delete_api_v1_payment_requests_payment_identifier(payment_identifier)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_api_v1_payment_requests_payment_identifier: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_identifier** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

