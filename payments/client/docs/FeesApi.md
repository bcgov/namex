# openapi_client.FeesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**calculate_fees**](FeesApi.md#calculate_fees) | **GET** /api/v1/fees/{corp_type}/{filing_type_code} | Calculate Fees


# **calculate_fees**
> Fee calculate_fees(corp_type, filing_type_code, jurisdiction=jurisdiction, date=date, priority=priority)

Calculate Fees

Calculate Fees on the filing type for corp type

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
    api_instance = openapi_client.FeesApi(api_client)
    corp_type = 'corp_type_example' # str | Corp Type
filing_type_code = 'filing_type_code_example' # str | Filing type code
jurisdiction = 'jurisdiction_example' # str | Jurisdiction or Province code (optional)
date = 'date_example' # str | Date on which the filing rates are applicable (optional)
priority = 'priority_example' # str | Indicator if priority fees are applicable (optional)

    try:
        # Calculate Fees
        api_response = api_instance.calculate_fees(corp_type, filing_type_code, jurisdiction=jurisdiction, date=date, priority=priority)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FeesApi->calculate_fees: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **corp_type** | **str**| Corp Type | 
 **filing_type_code** | **str**| Filing type code | 
 **jurisdiction** | **str**| Jurisdiction or Province code | [optional] 
 **date** | **str**| Date on which the filing rates are applicable | [optional] 
 **priority** | **str**| Indicator if priority fees are applicable | [optional] 

### Return type

[**Fee**](Fee.md)

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

