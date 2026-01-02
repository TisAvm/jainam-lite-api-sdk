"""
Custom Exceptions for Jainam Lite API SDK

Error codes mapped from Jainam API documentation.
"""


class JainamApiException(Exception):
    """Base exception for all Jainam API errors."""
    
    def __init__(self, message: str, error_code: str = None, response: dict = None):
        self.message = message
        self.error_code = error_code
        self.response = response
        super().__init__(self.message)
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class JainamAuthError(JainamApiException):
    """Authentication or session related errors."""
    pass


class JainamOrderError(JainamApiException):
    """Order placement, modification, or cancellation errors."""
    pass


class JainamValidationError(JainamApiException):
    """Input validation errors."""
    pass


class JainamNetworkError(JainamApiException):
    """Network or connection errors."""
    pass


class JainamRateLimitError(JainamApiException):
    """Rate limit exceeded error."""
    pass


# Error code to message mapping from Jainam API documentation
ERROR_CODES = {
    "EC003": "An error occurred. Please try again later.",
    "EC087": "Session Expired",
    "EC088": "Single order slicing limit exceeded",
    "EC900": "'exchange' cannot be empty or null.",
    "EC901": "'exchange' should be one of the following values: { 'NSE', 'BSE', 'MCX', 'NFO', 'BFO', 'CDS', 'BCD'}.",
    "EC902": "'tradingSymbol' cannot be empty or null.",
    "EC903": "'quantity' cannot be empty or null.",
    "EC904": "'quantity' should be a positive number.",
    "EC906": "'product' cannot be empty or null.",
    "EC907": "'transactionType' cannot be empty or null.",
    "EC908": "'token' cannot be empty or null.",
    "EC909": "'disclosedQty' cannot be empty or null.",
    "EC910": "'price' cannot be empty or null.",
    "EC911": "'triggerPrice' cannot be empty or null.",
    "EC912": "Failed to place the order.",
    "EC913": "Failed to retrieve user details.",
    "EC914": "'Request parameter' cannot be empty or null.",
    "EC915": "Failed to retrieve the order book.",
    "EC916": "No orders found for this user.",
    "EC917": "Failed to retrieve order history.",
    "EC918": "No order history found for the given order ID.",
    "EC919": "Failed to retrieve the position book.",
    "EC920": "No positions found for this user.",
    "EC921": "Failed to retrieve holdings.",
    "EC922": "No holdings found for this user.",
    "EC923": "Failed to retrieve profile details.",
    "EC924": "Failed to retrieve RMS limits.",
    "EC925": "'nestOrderNo' cannot be empty or null.",
    "EC926": "No trades found for this user.",
    "EC927": "Failed to retrieve the trade book.",
    "EC929": "'transactionType' should be one of the following values: {'BUY', 'SELL'}.",
    "EC930": "'orderType' should be one of the following values: {'LIMIT', 'MARKET', 'SL', 'SLM'}.",
    "EC932": "'validity' should be one of the following values: {'DAY', 'IOC'}.",
    "EC933": "'priceType' cannot be empty or null.",
    "EC934": "'orderType' cannot be empty or null.",
    "EC935": "Failed to retrieve the single order margin.",
    "EC936": "'product' cannot be empty or null.",
    "EC937": "Failed to cancel all orders.",
    "EC938": "No open orders to cancel from the order book.",
    "EC939": "Failed to retrieve the span margin.",
    "EC941": "'instrumentId' cannot be empty or null.",
    "EC942": "'orderComplexity' cannot be empty or null.",
    "EC944": "'validity' cannot be empty or null.",
    "EC945": "'brokerOrderId' cannot be empty or null.",
    "EC946": "Invalid 'instrumentId'. It must contain only numeric characters.",
    "EC947": "'instrumentId' does not exist.",
    "EC948": "'quantity' cannot exceed 50,000,000.",
    "EC949": "'quantity' should be a positive number.",
    "EC950": "'price' is required and cannot be empty or null.",
    "EC951": "'slTriggerPrice' is required and cannot be empty or null.",
    "EC953": "'targetPrice' is required and cannot be empty or null.",
    "EC954": "'quantity' should be a multiple of the lot size.",
    "EC957": "Invalid 'price'.",
    "EC958": "'price' cannot be zero or negative.",
    "EC959": "Invalid 'slTriggerPrice'.",
    "EC960": "'slTriggerPrice' cannot be zero or negative.",
    "EC962": "'stopLossPrice' cannot be zero or negative.",
    "EC963": "Invalid 'targetPrice'.",
    "EC964": "'targetPrice' cannot be zero or negative.",
    "EC966": "'trailingSlAmount' cannot be empty or null for SL order type.",
    "EC967": "'trailingSlAmount' should be a positive number.",
    "EC968": "'trailingSlAmount' cannot be zero or negative.",
    "EC969": "'Product' should be either 'NORMAL' or 'INTRADAY'.",
    "EC970": "'disclosedQuantity' is not applicable for this segment.",
    "EC971": "'orderTag' should not exceed 50 characters.",
    "EC972": "'algoId' should not exceed 12 characters.",
    "EC973": "For a buy order, 'slTriggerPrice' should be less than the 'price'.",
    "EC974": "For a sell order, 'slTriggerPrice' should be greater than the 'price'.",
    "EC975": "'disclosedQuantity' cannot exceed the total order 'quantity'.",
    "EC979": "Invalid 'brokerOrderId'.",
    "EC980": "Invalid 'instrumentId'.",
    "EC981": "Invalid 'disclosedQty'.",
    "EC982": "For 'AMO', 'disclosedQuantity' should be zero.",
    "EC983": "Invalid 'algoId'.",
    "EC984": "Invalid 'orderTag'.",
    "EC986": "SpanMargin is not allowed for 'NSEEQ' and 'BSEEQ'.",
    "EC988": "'marketProtection' should be a positive number.",
    "EC990": "'quantity' should be a multiple of the lot size.",
    "EC991": "'disclosedQuantity' should be a multiple of the lot size.",
    "EC992": "Unable to modify the given order. 'brokerOrderId' is invalid.",
    "EC993": "Provided 'brokerOrderId' is not in a valid state to modify the order.",
    "EC994": "The given 'brokerOrderId' is not in your order book.",
    "EC996": "'validity' of IOC is not allowed for AMO orders.",
    "EC997": "The specified order is not available in the order book and cannot be canceled.",
    "EC998": "The specified order is not available in the order book, and order history cannot be retrieved.",
    "EC999": "The specified order is not available in the order book and cannot be modified.",
    "EC801": "Orders with exchange 'BSEEQ/BSEFO/BSECURR' cannot be modified to order type 'SL'.",
    "EC806": "'exchange' accepts only {'NSEEQ', 'BSEEQ'}.",
    "EC807": "'product' - 'NORMAL' is not allowed in cash segment.",
    "EC813": "'deviceId' cannot exceed 98 characters.",
    "EC814": "'brokerOrderId' cannot be empty or null.",
    "EC815": "Invalid 'brokerOrderId'.",
    "EC819": "Only the trigger price field can be modified.",
    "EC822": "SL trigger price should be lower than price.",
    "EC823": "SL trigger price should be higher than price.",
    "EC826": "Please enter a price.",
    "EC827": "Please enter a target price.",
    "EC828": "Please enter an SL trigger price.",
    "EC829": "AMO is not allowed for this product.",
    "EC830": "AMO is not allowed for this order type.",
    "EC831": "AMO is not allowed for this validity.",
    "EC832": "AMO is not allowed for this segment.",
    "EC834": "Market protection cannot be modified.",
    "EC837": "This product is not allowed for this segment.",
    "EC838": "This order type is not allowed.",
    "EC843": "Only price and quantity fields can be modified.",
    "EC844": "Only price and order type fields can be modified.",
    "EC852": "This product is not allowed.",
    "EC855": "Modification is not allowed.",
    "EC856": "SL trigger price should be less than main leg price.",
    "EC857": "SL trigger price should be more than main leg price.",
    "EC858": "Order placement not allowed for this exchange.",
    "EC865": "'product' - 'Delivery' is not allowed in FnO segment.",
    "EC868": "Position not found for the specified instrument.",
    "EC869": "Insufficient buy quantity available for conversion.",
    "EC870": "Insufficient sell quantity available for conversion.",
    "EC871": "Conversion of overnight BUY positions in options is not allowed.",
    "EC873": "Failed to convert positions.",
    "EC082": "Invalid parameter: 'deviceId' cannot be empty or null.",
    "EC086": "You are a read-only user and are not allowed to place, modify, or cancel orders.",
    "EC089": "'disclosedQuantity' cannot be same as the total order 'quantity'.",
    "EC090": "'exchange' should be one of the following values: { 'NSE', 'BSE', 'MCX', 'NFO', 'BFO'}.",
    "EC091": "'orderComplexity' should be one of the following values: {'REGULAR', 'AMO'}.",
    "EC092": "'product' should be one of the following values: {'INTRADAY', 'LONGTERM', 'MTF'}.",
}


def get_error_message(error_code: str) -> str:
    """Get human-readable error message for an error code."""
    return ERROR_CODES.get(error_code, f"Unknown error: {error_code}")


def raise_from_response(response: dict):
    """
    Raise appropriate exception based on API response.
    
    Args:
        response: API response dictionary
        
    Raises:
        JainamApiException or subclass based on error type
    """
    if response.get("status") == "Ok":
        return
    
    error_code = response.get("errorCode") or response.get("error_code")
    message = response.get("message") or get_error_message(error_code)
    
    # Determine exception type based on error code
    if error_code == "EC087":
        raise JainamAuthError(message, error_code, response)
    elif error_code and error_code.startswith("EC9"):
        # EC9xx are validation errors
        raise JainamValidationError(message, error_code, response)
    elif error_code in ("EC912", "EC937", "EC992", "EC993", "EC997", "EC999"):
        # Order-related errors
        raise JainamOrderError(message, error_code, response)
    else:
        raise JainamApiException(message, error_code, response)
