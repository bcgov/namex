# openapi_client.ReceiptsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_receipt**](ReceiptsApi.md#get_receipt) | **GET** /api/v1/payment-requests/{payment_identifier}/receipts | Get receipt for the payment


# **get_receipt**
> file get_receipt(payment_identifier)

Get receipt for the payment

Returns payment receipt details

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
    api_instance = openapi_client.ReceiptsApi(api_client)
    payment_identifier = 'payment_identifier_example' # str | Unique Identifier for the payment

    try:
        # Get receipt for the payment
        api_response = api_instance.get_receipt(payment_identifier)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ReceiptsApi->get_receipt: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_identifier** | **str**| Unique Identifier for the payment | 

### Return type

**file**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/pdf, application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Receipt PDF file |  -  |
**400** | BadRequest |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

