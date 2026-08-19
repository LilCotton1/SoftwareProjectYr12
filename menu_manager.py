from database import get_connection

#Loads menu from database
def load_menu():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT name, price, stock, category, description, daily_special
        FROM menu
    """)
    rows = cursor.fetchall()
    connection.close()

    menu = {}
    for name, price, stock, category, description, daily_special in rows:
        menu[name] = {
            "price": price,
            "stock": stock,
            "category": category,
            "description": description or "",
            "daily_special": bool(daily_special)
        }

    return menu


# Get menu item ID by name
def get_menu_item_id(name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM menu WHERE name = ?", (name,))
    result = cursor.fetchone()
    connection.close()

    if result:
        return result[0]
    return None


# Add a new menu item
def add_menu_item(name, price, stock, category, description, daily_special):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO menu (name, price, stock, category, description, daily_special)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            price,
            stock,
            category,
            description,
            int(daily_special)
        ))
        connection.commit()
        connection.close()
        return True

    except:
        connection.close()
        return False


# Update an existing menu item
def update_menu_item(name, price, stock, category, description, daily_special):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE menu
        SET price = ?, stock = ?, category = ?, description = ?, daily_special = ?
        WHERE name = ?
    """, (
        price,
        stock,
        category,
        description,
        int(daily_special),
        name
    ))
    connection.commit()
    success = cursor.rowcount > 0
    connection.close()

    return success


# Delete a menu item
def delete_menu_item(name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM menu WHERE name = ?", (name,))
    connection.commit()
    success = cursor.rowcount > 0
    connection.close()

    return success


# Reduce stock of a menu item
def reduce_stock(name, quantity):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE menu
        SET stock = stock - ?
        WHERE name = ? AND stock >= ?
    """, (
        quantity,
        name,
        quantity
    ))
    connection.commit()
    success = cursor.rowcount > 0
    connection.close()

    return success
