from shopify import Shopify

def delete_unfulfilled_orders():
    sh = Shopify()
    orders = sh.get_orders()
    print(f"deleting {len(orders)} orders\n")
    for order in orders:
        sh.delete_order(order['id'])

if __name__ == '__main__':
    answer = input("""What process do you want to run?\nInput one of the following numbers to begin one of the corresponding processes.\n-------\n
    1 - delete all orders\n""")
    if answer == 1 or str(answer) == '1':
        delete_unfulfilled_orders()
    else: 
        print("not a valid answer.")