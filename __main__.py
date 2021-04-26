from shopify import Shopify


def delete_unfulfilled_orders():
    sh = Shopify()
    orders = sh.get_orders()
    print(f"deleting {len(orders)} orders\n")
    for order in orders:
        sh.delete_order(order['id'])


delete_unfulfilled_orders()