import csv
import sqlite3

def export_to_csv(user_id):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("SELECT date, category, amount FROM expenses WHERE user_id=?", (user_id,))
    data = cur.fetchall()

    conn.close()

    with open("C:/Users/Public/expenses_export.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount"])
        writer.writerows(data)

    print("Exported to expenses_export.csv")