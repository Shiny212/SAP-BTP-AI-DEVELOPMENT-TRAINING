"""
tools.py

Business Tools for
SmartKart AI Customer Support.
"""

from langchain_core.tools import tool


# ==========================================================
# Order Status Tool
# ==========================================================

@tool
def check_order_status(order_id: str) -> str:
    """
    Returns the current status of a customer's order.
    """

    orders = {
        "ORD1001": "Processing",
        "ORD1002": "Shipped",
        "ORD1003": "Delivered",
        "ORD1004": "Out for Delivery",
        "ORD1005": "Cancelled",
    }

    status = orders.get(order_id.upper())

    if status:
        return (
            f"Order {order_id.upper()} "
            f"is currently {status}."
        )

    return f"Order {order_id.upper()} was not found."


# ==========================================================
# Discount Calculator Tool
# ==========================================================

@tool
def calculate_discount(
    customer_type: str,
    amount: float,
) -> str:
    """
    Calculates the discount amount based on the customer type.
    """

    customer_type = customer_type.lower()

    if customer_type == "premium":
        discount = 10
    elif customer_type == "standard":
        discount = 5
    else:
        discount = 0

    discount_amount = amount * discount / 100
    final_amount = amount - discount_amount

    return (
        f"Original Amount : ₹{amount:.2f}\n"
        f"Discount        : {discount}%\n"
        f"Discount Amount : ₹{discount_amount:.2f}\n"
        f"Final Amount    : ₹{final_amount:.2f}"
    )


# ==========================================================
# Delivery Charge Tool
# ==========================================================

@tool
def calculate_delivery_charge(
    amount: float,
) -> str:
    """
    Calculates the delivery charge based on the purchase amount.
    """

    if amount >= 2000:
        return "Delivery Charge : FREE"

    return "Delivery Charge : ₹100"


# ==========================================================
# Estimated Delivery Tool
# ==========================================================

@tool
def get_estimated_delivery(
    city: str,
) -> str:
    """
    Returns the estimated delivery time for the specified city.
    """

    delivery_data = {
        "chennai": "2 Business Days",
        "coimbatore": "2 Business Days",
        "trichy": "3 Business Days",
        "madurai": "3 Business Days",
        "bangalore": "4 Business Days",
        "hyderabad": "5 Business Days",
    }

    delivery = delivery_data.get(city.lower())

    if delivery:
        return (
            f"Estimated Delivery : {delivery}"
        )

    return "Delivery estimate unavailable for the specified city."