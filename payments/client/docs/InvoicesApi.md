# openapi_client.InvoicesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_invoice**](InvoicesApi.md#get_invoice) | **GET** /api/v1/payment-requests/{payment_identifier}/invoices/{invoice_id} | Get Invoice
[**get_invoices**](InvoicesApi.md#get_invoices) | **GET** /api/v1/payment-requests/{payment_identifier}/invoices | Get Invoices


# **get_invoice**
> Invoice get_invoice(payment_identifier, invoice_id)

Get Invoice

Get an invoice for the payment

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
    api_instance = openapi_client.InvoicesApi(api_client)
    payment_identifier = 'payment_identifier_example' # str | Unique Identifier for the payment
invoice_id = 'invoice_id_example' # str | Unique Identifier for the invoice

    try:
        # Get Invoice
        api_response = api_instance.get_invoice(payment_identifier, invoice_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling InvoicesApi->get_invoice: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_identifier** | **str**| Unique Identifier for the payment | 
 **invoice_id** | **str**| Unique Identifier for the invoice | 

### Return type

[**Invoice**](Invoice.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  * X-Application-Context - X-Application-Context <br>  * Access-Control-Allow-Origin - Access-Control-Allow-Origin <br>  * Access-Control-Allow-Methods - Access-Control-Allow-Methods <br>  * Access-Control-Allow-Headers - Access-Control-Allow-Headers <br>  |
**400** | BadRequest |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_invoices**
> Invoices get_invoices(payment_identifier)

Get Invoices

Get Invoices for the payment

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
    api_instance = openapi_client.InvoicesApi(api_client)
    payment_identifier = 'payment_identifier_example' # str | Unique Identifier for the payment

    try:
        # Get Invoices
        api_response = api_instance.get_invoices(payment_identifier)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling InvoicesApi->get_invoices: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_identifier** | **str**| Unique Identifier for the payment | 

### Return type

[**Invoices**](Invoices.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  * X-Application-Context - X-Application-Context <br>  * Access-Control-Allow-Origin - Access-Control-Allow-Origin <br>  * Access-Control-Allow-Methods - Access-Control-Allow-Methods <br>  * Access-Control-Allow-Headers - Access-Control-Allow-Headers <br>  |
**400** | BadRequest |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

