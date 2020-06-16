# openapi_client.TransactionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_transaction**](TransactionsApi.md#create_transaction) | **POST** /api/v1/payment-requests/{payment_identifier}/transactions | Create a transaction
[**get_transaction**](TransactionsApi.md#get_transaction) | **GET** /api/v1/payment-requests/{payment_identifier}/transactions/{transaction_identifier} | Get Transaction
[**get_transactions**](TransactionsApi.md#get_transactions) | **GET** /api/v1/payment-requests/{payment_identifier}/transactions | Get Transactions
[**update_transaction**](TransactionsApi.md#update_transaction) | **PUT** /api/v1/payment-requests/{payment_identifier}/transactions/{transaction_identifier} | Update a transaction


# **create_transaction**
> Transaction create_transaction(payment_identifier, redirect_uri)

Create a transaction

Creates a transaction for the payment.

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
    api_instance = openapi_client.TransactionsApi(api_client)
    payment_identifier = 'payment_identifier_example' # str | 
redirect_uri = 'redirect_uri_example' # str | Redirect URI

    try:
        # Create a transaction
        api_response = api_instance.create_transaction(payment_identifier, redirect_uri)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TransactionsApi->create_transaction: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_identifier** | **str**|  | 
 **redirect_uri** | **str**| Redirect URI | 

### Return type

[**Transaction**](Transaction.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |
**400** | BadRequest |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_transaction**
> Transactions get_transaction(receipt_number, payment_identifier, transaction_identifier)

Get Transaction

Get a Transaction for the payment

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
    api_instance = openapi_client.TransactionsApi(api_client)
    receipt_number = 'http%3A//localhost%3A8080/coops-web/transactions%3Ftransaction_id%3Dabcd' # str | Receipt Number for the payment
payment_identifier = 'payment_identifier_example' # str | Unique Identifier for the payment
transaction_identifier = 'transaction_identifier_example' # str | Unique Identifier for the transaction

    try:
        # Get Transaction
        api_response = api_instance.get_transaction(receipt_number, payment_identifier, transaction_identifier)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TransactionsApi->get_transaction: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **receipt_number** | **str**| Receipt Number for the payment | 
 **payment_identifier** | **str**| Unique Identifier for the payment | 
 **transaction_identifier** | **str**| Unique Identifier for the transaction | 

### Return type

[**Transactions**](Transactions.md)

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

# **get_transactions**
> Transactions get_transactions(payment_identifier)

Get Transactions

Get Transactions for the payment

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
    api_instance = openapi_client.TransactionsApi(api_client)
    payment_identifier = 'payment_identifier_example' # str | Unique Identifier for the payment

    try:
        # Get Transactions
        api_response = api_instance.get_transactions(payment_identifier)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TransactionsApi->get_transactions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_identifier** | **str**| Unique Identifier for the payment | 

### Return type

[**Transactions**](Transactions.md)

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

# **update_transaction**
> Transaction update_transaction(payment_identifier, receipt_number, transaction_identifier)

Update a transaction

Updaate transaction for the payment.

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
    api_instance = openapi_client.TransactionsApi(api_client)
    payment_identifier = 'payment_identifier_example' # str | Unique Identifier for the payment
receipt_number = 'receipt_number_example' # str | Receipt Number for the payment
transaction_identifier = 'transaction_identifier_example' # str | Unique Identifier for the transaction

    try:
        # Update a transaction
        api_response = api_instance.update_transaction(payment_identifier, receipt_number, transaction_identifier)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TransactionsApi->update_transaction: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_identifier** | **str**| Unique Identifier for the payment | 
 **receipt_number** | **str**| Receipt Number for the payment | 
 **transaction_identifier** | **str**| Unique Identifier for the transaction | 

### Return type

[**Transaction**](Transaction.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | BadRequest |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

