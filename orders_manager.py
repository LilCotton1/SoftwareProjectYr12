from datetime import datetime

from database import get_connection

#Creates a new order in the database
def create_order(username, cart, total):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO orders (username, total, status, date)
            VALUES (?, ?, ?, ?)
        """, (
            username,
            total,
            "Pending",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        order_id = cursor.lastrowid

        for cart_item in cart:
            cursor.execute("SELECT id, stock FROM menu WHERE name = ?", (cart_item["item"],))
            row = cursor.fetchone()

            if row is None or row[1] < cart_item["quantity"]:
                raise ValueError(f"Not enough stock for {cart_item['item']}")

            menu_item_id = row[0]

            cursor.execute("""
                INSERT INTO order_items (order_id, menu_item_id, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (
                order_id,
                menu_item_id,
                cart_item["quantity"],
                cart_item["price"]
            ))

            cursor.execute("""
                UPDATE menu
                SET stock = stock - ?
                WHERE id = ?
            """, (
                cart_item["quantity"],
                menu_item_id
            ))

        connection.commit()
        connection.close()
        return order_id

    except Exception:
        connection.rollback()
        connection.close()
        return None


#Loads all orders
def load_orders():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, username, total, status, date
        FROM orders
        ORDER BY id DESC
    """)
    order_rows = cursor.fetchall()

    orders = []
    for order_id, username, total, status, date in order_rows:
        cursor.execute("""
            SELECT menu.name, order_items.quantity, order_items.price
            FROM order_items
            JOIN menu ON menu.id = order_items.menu_item_id
            WHERE order_items.order_id = ?
        """, (order_id,))

        items = []
        for name, quantity, price in cursor.fetchall():
            items.append({"item": name, "quantity": quantity, "price": price})

        orders.append({
            "id": order_id,
            "username": username,
            "total": total,
            "status": status,
            "date": date,
            "items": items
        })

    connection.close()
    return orders


#Loads orders for a user
def load_orders_for_user(username):
    return [order for order in load_orders() if order["username"] == username]


#Updates status of order
def update_order_status(order_id, status):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?
    """, (
        status,
        order_id
    ))
    connection.commit()
    success = cursor.rowcount > 0
    connection.close()

    return success
