# Invoice

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**links** | [**list[Links]**](Links.md) |  | [optional] 
**id** | **int** | Unique identifier for invoice | [optional] 
**account_id** | **int** | id of the account | [optional] 
**created_by** | **str** | username of the account | [optional] 
**created_on** | **str** | invoice creation date | [optional] 
**payment_date** | **str** | date made payment | [optional] 
**payment_id** | **int** | payment identifier | [optional] 
**paid** | **float** | amount paid | [optional] 
**line_items** | [**list[PaymentLineItem]**](PaymentLineItem.md) |  | [optional] 
**reference_number** | **str** | reference number | [optional] 
**status_code** | **str** | Status of payment. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


