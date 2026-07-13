"""
tools.py

Business tools for SmartKart AI Customer Support.
"""

from langchain_core.tools import tool


# --------------------------------------------------
# Mock Database
# --------------------------------------------------

ORDERS = {
    "ORD1001": "Processing",
    "ORD1002": "Shipped",
    "ORD1003": "Delivered",
    "ORD1004": "Cancelled",
}

CUSTOMERS = {
    "CUS1001": "Premium Member",
    "CUS1002": "Regular Member",
    "CUS1003": "Account Suspended",
}

DELIVERY = {
    "Chennai": "2 Business Days",
    "Bangalore": "3 Business Days",
    "Hyderabad": "4 Business Days",
    "Mumbai": "5 Business Days",
}


# --------------------------------------------------
# Order Status Tool
# --------------------------------------------------

@tool
def get_order_status(order_id: str) -> str:
    """
    Returns the current status of a customer's order.
    """

    order_id = order_id.upper().strip()

    if order_id not in ORDERS:
        return f"Order '{order_id}' was not found."

    return ORDERS[order_id]


# --------------------------------------------------
# Refund Eligibility Tool
# --------------------------------------------------

@tool
def check_refund_eligibility(days_since_purchase: int) -> str:
    """
    Determines refund eligibility.
    """

    if days_since_purchase < 0:
        return "Invalid number of days."

    if days_since_purchase <= 30:
        return "Eligible for full refund."

    return "Refund period has expired."


# --------------------------------------------------
# Delivery Estimate Tool
# --------------------------------------------------

@tool
def get_delivery_estimate(city: str) -> str:
    """
    Returns estimated delivery time.
    """

    city = city.title().strip()

    if city not in DELIVERY:
        return "Delivery estimate unavailable."

    return DELIVERY[city]


# --------------------------------------------------
# Customer Account Tool
# --------------------------------------------------

@tool
def get_account_status(customer_id: str) -> str:
    """
    Returns customer account status.
    """

    customer_id = customer_id.upper().strip()

    if customer_id not in CUSTOMERS:
        return "Customer not found."

    return CUSTOMERS[customer_id]