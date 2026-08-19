import hashlib
from database import get_connection

# Hashes passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Signup
def signup(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("""
            INSERT INTO users (username, password, role, balance)
            VALUES (?, ?, ?, ?)
        """, (
            username,
            hashed_password,
            "student",
            0.00
        ))
        connection.commit()
        connection.close()

        return True

    except:
        connection.close()
        return False


# Login
def login(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    hashed_password = hash_password(password)
    cursor.execute("""
        SELECT role
        FROM users
        WHERE username = ? AND password = ?
    """, (
        username,
        hashed_password
    ))

    result = cursor.fetchone()
    connection.close()

    if result:
        return result[0]
    return None


# Get balance
def get_balance(username):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT balance
        FROM users
        WHERE username = ?
    """, (username,))

    result = cursor.fetchone()
    connection.close()

    if result:
        return result[0]

    return None


# Add money
def add_balance(username, amount):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET balance = balance + ?
        WHERE username = ?
    """, (
        amount,
        username
    ))
    connection.commit()
    success = cursor.rowcount > 0
    connection.close()

    return success


# Load every user
def load_users():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT username, role, balance FROM users")
    rows = cursor.fetchall()
    connection.close()

    users = {}
    for username, role, balance in rows:
        users[username] = {"role": role, "balance": balance}

    return users


# Updates users
def update_user(username, role, balance):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE users
        SET role = ?, balance = ?
        WHERE username = ?
    """, (
        role,
        balance,
        username
    ))
    connection.commit()
    success = cursor.rowcount > 0
    connection.close()

    return success


# Delete a user
def delete_user(username):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    connection.commit()
    success = cursor.rowcount > 0
    connection.close()

    return success