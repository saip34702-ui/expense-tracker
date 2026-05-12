import sqlite3
import bcrypt

def connect():

    try:
        conn = sqlite3.connect("expenses.db")
        return conn

    except Exception as e:
        print("Database connection error:", e)
        return None


def init_db():
    """Create required tables and ensure `role` column on users table."""
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date TEXT,
        category TEXT,
        amount REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS income(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                source TEXT,
                amount REAL
            )
    """)

    # Ensure role column exists
    cur.execute("PRAGMA table_info(users)")
    cols = [row[1] for row in cur.fetchall()]
    if 'role' not in cols:
        cur.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")

    conn.commit()
    conn.close()


# ✅ REGISTER FUNCTION - bcrypt hashing added
def register(username, password):

    try:

        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
            (username, password, "user")
        )

        conn.commit()
        conn.close()

        return True
    
    except Exception as e:
        print("Registration error:", e)
        return False
   

# ✅ LOGIN FUNCTION - bcrypt verify added
def login(username, password):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()

    if user is None:
        return None

    # Database मधील hashed password शी compare करतो
    stored_hash = user[2]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return user
    else:
        return None


def add_expense(user_id, date, category, amount):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses VALUES (NULL, ?, ?, ?, ?)", (user_id, date, category, amount))
    conn.commit()
    conn.close()


def delete(expense_id):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()


def get_expenses(user_id):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def update_expense(expense_id, category, amount):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("UPDATE expenses SET category=?, amount=? WHERE id=?",
                (category, amount, expense_id))
    conn.commit()
    conn.close()


def get_total_expense(user_id):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id=?", (user_id,))
    total = cur.fetchone()[0]
    conn.close()
    return total if total else 0

def delete_user(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    
    conn.commit()
    conn.close()

def get_users():
    conn  = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username FROM users")
    data = cursor.fetchall()

    conn.close()
    return data

def get_user(username):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    conn.close()
    return user
    
def change_password(username, new_password):
    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute("UPDATE users SET password=? WHERE username=?",
                   (new_password, username)
                   )
    
    conn.commit()
    conn.close()

def change_password(user_id, new_password):

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password=? WHERE id=?",
        (new_password, user_id)
    )

    conn.commit()
    conn.close() 

def get_user_by_id(user_id):

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?",
               (user_id,))

    user = cursor.fetchone()

    conn.close()
    return user

def add_income(user_id, date, source, amount):
    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO income(user_id, date, source, amount) VALUES(?,?,?,?)",
        (user_id, date, source, amount)
    )

    conn.commit()
    conn.close()

def get_income(user_id):
    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM income WHERE user_id=?",
        (user_id,)
    )

    total =cursor.fetchone()[0]

    conn.close()

    return total if total else 0

def add_income(user_id, date, source, amount):

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO income(user_id, date, source, amount) VALUES(?,?,?,?)",
        (user_id, date, source, amount)
    )

    conn.commit()
    conn.close()


def get_income(user_id):

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM income WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


def get_total_income(user_id):

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE user_id=?",
        (user_id,)
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0