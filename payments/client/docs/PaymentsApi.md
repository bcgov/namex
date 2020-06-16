# openapi_client.PaymentsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_payment**](PaymentsApi.md#create_payment) | **POST** /api/v1/payment-requests | Create payment records
[**get_payment**](PaymentsApi.md#get_payment) | **GET** /api/v1/payment-requests/{payment_identifier} | Get Payment
[**update_payment**](PaymentsApi.md#update_payment) | **PUT** /api/v1/payment-requests/{payment_identifier} | Update payment records


# **create_payment**
> Payment create_payment(payment_request)

Create payment records

Creates payment records.

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
    api_instance = openapi_client.PaymentsApi(api_client)
    payment_request = {"paymentInfo":{"methodOfPayment":"CC"},"businessInfo":{"businessIdentifier":"CP1234567","corpType":"CP","businessName":"ABC Corp","contactInfo":{"city":"Victoria","postal_code":"V8P2P2","province":"BC","addressLine1":"100 Douglas Street","country":"CA"}},"filingInfo":{"filingTypes":[{"filingTypeCode":"OTADD","filingDescription":"TEST"},{"filingTypeCode":"OTANN"}]}} # PaymentRequest | 

    try:
        # Create payment records
        api_response = api_instance.create_payment(payment_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PaymentsApi->create_payment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_request** | [**PaymentRequest**](PaymentRequest.md)|  | 

### Return type

[**Payment**](Payment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |
**400** | BadRequest |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_payment**
> Payment get_payment(payment_identifier)

Get Payment

Get Payment by filing identifier

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
    api_instance = openapi_client.PaymentsApi(api_client)
    payment_identifier = 'payment_identifier_example' # str | Unique Identifier for the payment

    try:
        # Get Payment
        api_response = api_instance.get_payment(payment_identifier)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PaymentsApi->get_payment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_identifier** | **str**| Unique Identifier for the payment | 

### Return type

[**Payment**](Payment.md)

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

# **update_payment**
> Payment update_payment(payment_identifier, payment_request)

Update payment records

Updates payment records.

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
    api_instance = openapi_client.PaymentsApi(api_client)
    payment_identifier = 'payment_identifier_example' # str | 
payment_request = {"paymentInfo":{"methodOfPayment":"CC"},"businessInfo":{"businessIdentifier":"CP1234567","corpType":"CP","businessName":"ABC Corp","contactInfo":{"city":"Victoria","postalCode":"V8P2P2","province":"BC","addressLine1":"100 Douglas Street","country":"CA"}},"filingInfo":{"filingTypes":[{"filingTypeCode":"OTADD","filingDescription":"TEST"},{"filingTypeCode":"OTANN"}]}} # PaymentRequest | 

    try:
        # Update payment records
        api_response = api_instance.update_payment(payment_identifier, payment_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PaymentsApi->update_payment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_identifier** | **str**|  | 
 **payment_request** | [**PaymentRequest**](PaymentRequest.md)|  | 

### Return type

[**Payment**](Payment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |
**400** | BadRequest |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

