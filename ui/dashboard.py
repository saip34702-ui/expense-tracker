from utils import pdf_export
import tkinter as tk
from tkinter import ttk
from database import db
from utils import charts, export
from datetime import datetime
from tkcalendar import DateEntry

current_theme = ["light"]

def show_popup(title, msg):
    
    pop = tk.Toplevel()

    pop.title(title)

    pop.geometry("260x130")

    tk.Label(pop,
             text=msg,
             font=("Arial", 11)).pack(pady=20)
    
    tk.Button(pop,
              text="OK",
              width=10,
              bg="#4CAF50",
              fg="white",
              command=pop.destroy).pack()

def open_dashboard(user_id, role, parent):

    window = tk.Toplevel()
    window.title("Expense Dashboard")
    window.geometry("1200x700")
    window.configure(bg="#f5f5f5")

    # ================= CLOSE =================
    def on_close():
        window.destroy()
        parent.deiconify()

    window.protocol("WM_DELETE_WINDOW", on_close)

    # ================= LOGOUT =================
    def logout():
        pop = tk.Toplevel(window)
        pop.title("Logout")
        pop.geometry("250x120")
        pop.resizable(False, False)

        tk.Label(pop,
                 text="Do you want to logout?",
                 font=("Arial", 11)).pack(pady=15)

        btns = tk.Frame(pop)
        btns.pack()

        def yes():
            pop.destroy()
            window.destroy()
            parent.deiconify()

        tk.Button(btns, text="Yes",
                  bg="green", fg="white",
                  width=8,
                  command=yes).pack(side="left", padx=10)

        tk.Button(btns, text="No",
                  bg="red", fg="white",
                  width=8,
                  command=pop.destroy).pack(side="right", padx=10)

    # ================= MAIN =================
    main = tk.Frame(window)
    main.pack(fill="both", expand=True)

    # ================= SIDEBAR =================
    sidebar = tk.Frame(main, width=220, bg="#2c3e50")
    sidebar.pack(side="left", fill="y")

    # ================= CONTENT =================
    content = tk.Frame(main, bg="#f5f5f5")
    content.pack(side="right", fill="both", expand=True)

    # ================= THEME =================
    def apply_theme():

        if current_theme[0] == "dark":

            content.config(bg="#1e1e1e")
            sidebar.config(bg="#121212")

            title.config(bg="#1e1e1e", fg="white")
            total_label.config(bg="#1e1e1e", fg="#00ff99")
            top_label.config(bg="#1e1e1e", fg="#ff66cc")
            insight_label.config(bg="#1e1e1e", fg="#00cccc")

            filter_frame.config(bg="#1e1e1e")
            date_frame.config(bg="#1e1e1e")
            graph_frame.config(bg="#1e1e1e")

        else:

            content.config(bg="#f5f5f5")
            sidebar.config(bg="#2c3e50")

            title.config(bg="#f5f5f5", fg="black")
            total_label.config(bg="#f5f5f5", fg="#4CAF50")
            top_label.config(bg="#f5f5f5", fg="#E91E63")
            insight_label.config(bg="#f5f5f5", fg="#009688")

            filter_frame.config(bg="#f5f5f5")
            date_frame.config(bg="#f5f5f5")
            graph_frame.config(bg="#f5f5f5")

    def set_light():
        current_theme[0] = "light"
        apply_theme()

    def set_dark():
        current_theme[0] = "dark"
        apply_theme()

    # ================= TITLE =================
    title = tk.Label(content,
                     text="Expense Dashboard",
                     font=("Arial", 22, "bold"),
                     bg="#f5f5f5")
    title.pack(pady=10)

    # ================= THEME ICONS =================
    theme_frame = tk.Frame(content, bg="#f5f5f5")
    theme_frame.place(relx=0.95, rely=0.02, anchor="ne")

    tk.Button(theme_frame,
              text="☀️",
              font=("Arial", 14),
              bd=0,
              bg="#FFD54F",
              command=set_light).pack(side="left", padx=3)

    tk.Button(theme_frame,
              text="🌙",
              font=("Arial", 14),
              bd=0,
              bg="#90CAF9",
              command=set_dark).pack(side="left", padx=3)

    # ================= LABELS =================
    total_label = tk.Label(content,
                           text="Total: ₹ 0",
                           font=("Arial", 15, "bold"),
                           bg="#f5f5f5",
                           fg="#4CAF50")
    total_label.pack()

    income_label = tk.Label(content,
                            text="Income: ₹ 0",
                            font=("Arial", 13, "bold"),
                            bg="#f5f5f5",
                            fg="#2196F3")
    income_label.pack()

    balance_label = tk.Label(content,
                             text="Balance: ₹ 0",
                             font=("Arial", 13, "bold"),
                             bg="#f5f5f5",
                             fg="#FF5722")
    balance_label.pack()

    top_label = tk.Label(content,
                         text="Top Category: -",
                         font=("Arial", 12, "bold"),
                         bg="#f5f5f5",
                         fg="#E91E63")
    top_label.pack()

    insight_label = tk.Label(content,
                             text="Insight: -",
                             font=("Arial", 11),
                             bg="#f5f5f5",
                             fg="#009688")
    insight_label.pack()

    # ================= MONTH FILTER =================
    filter_frame = tk.Frame(content, bg="#f5f5f5")
    filter_frame.pack(pady=5)

    tk.Label(filter_frame,
             text="Filter Month:",
             bg="#f5f5f5").pack(side="left", padx=5)

    month_var = tk.StringVar()

    month_box = ttk.Combobox(filter_frame,
                             textvariable=month_var,
                             width=12,
                             state="readonly")
    month_box.pack(side="left")

    # ================= DATE FILTER =================
    date_frame = tk.Frame(content, bg="#f5f5f5")
    date_frame.pack(pady=5)

    tk.Label(date_frame,
             text="From:",
             bg="#f5f5f5").pack(side="left", padx=5)

    from_date = DateEntry(date_frame,
                          width=12,
                          date_pattern='yyyy-mm-dd')
    from_date.pack(side="left", padx=5)

    tk.Label(date_frame,
             text="To:",
             bg="#f5f5f5").pack(side="left", padx=5)

    to_date = DateEntry(date_frame,
                        width=12,
                        date_pattern='yyyy-mm-dd')
    to_date.pack(side="left", padx=5)

    # ================= TABLE =================
    table_frame = tk.Frame(content)
    table_frame.pack(pady=10)

    tree = ttk.Treeview(table_frame,
                        columns=("ID", "Date", "Category", "Amount"),
                        show="headings",
                        height=12)

    for col in ("ID", "Date", "Category", "Amount"):
        tree.heading(col, text=col)

    tree.column("ID", width=50)
    tree.column("Date", width=120)
    tree.column("Category", width=180)
    tree.column("Amount", width=120)

    tree.pack()

    # ================= GRAPH FRAME =================
    graph_frame = tk.Frame(content, bg="#f5f5f5")
    graph_frame.pack(fill="both", expand=True)

    # ================= LOAD MONTHS =================
    def load_months():

        rows = db.get_expenses(user_id)

        months = sorted(set([row[2][:7] for row in rows]))

        if months:
            month_box["values"] = ["All"] + months
            month_box.current(0)
        else:
            month_box["values"] = ["All"]
            month_box.current(0)

    # ================= LOAD DATA =================
    def load_data():

        for row in tree.get_children():
            tree.delete(row)

        rows = db.get_expenses(user_id)

        selected_month = month_var.get()

        start_date = from_date.get()
        end_date = to_date.get()

        total = 0
        category_sum = {}

        for row in rows:

            expense_date = row[2]

            if expense_date < start_date or expense_date > end_date:
                continue

            if selected_month != "All":
                if not row[2].startswith(selected_month):
                    continue

            tree.insert("",
                        tk.END,
                        values=(row[0],
                                row[2],
                                row[3],
                                f"₹ {row[4]}"))

            total += float(row[4])

            category_sum[row[3]] = category_sum.get(row[3], 0) + float(row[4])

        total_label.config(text=f"Total: ₹ {int(total)}")

        income = db.get_total_income(user_id)

        income_label.config(
            text=f"Income: ₹ {int(income)}"
        )

        balance = income - total

        balance_label.config(
            text=f"Balance: ₹ {int(balance)}"
        )

        if category_sum:
            top = max(category_sum, key=category_sum.get)
            top_label.config(text=f"Top Category: {top}")

        if total > 80000:
            insight_label.config(text="Insight: High spending ⚠️")
        elif total > 40000:
            insight_label.config(text="Insight: Moderate 👍")
        else:
            insight_label.config(text="Insight: Good control 💰")

    # ================= GRAPH =================
    def show_graph_embed():

        for widget in graph_frame.winfo_children():
            widget.destroy()

        chart = charts.get_chart_figure(user_id)

        if not chart:
            tk.Label(graph_frame,
                     text="No data available",
                     font=("Arial", 12),
                     bg="#f5f5f5").pack()
            return

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        canvas = FigureCanvasTkAgg(chart, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both",
                                    expand=True,
                                    padx=20,
                                    pady=10)

    # ================= REFRESH =================
    def refresh_all():
        load_data()
        show_graph_embed()

    month_box.bind("<<ComboboxSelected>>",
                   lambda e: refresh_all())

    # ================= FUNCTIONS =================
    def add_income():
        win = tk.Toplevel()

        win.title("Add Income")

        win.geometry("300x280")

        tk.Label(win,
                 text="Income Source").pack(pady=5)
        
        source = tk.Entry(win, width=25)
        source.pack()

        tk.Label(win,
                 text="Amount").pack(pady=5)
        
        amount = tk.Entry(win, width=25)
        amount.pack()

        def save():
            try:

                amt = float(amount.get())

            except:
                show_popup("Error", "Invalid amount")

                return
            
            db.add_income(
                user_id,
                datetime.now().strftime("%Y-%m-%d"),
                source.get(),
                amt
            )

            show_popup("Success",
                       "Income added!")
            
            win.destroy()

            load_data()

        tk.Button(win,
                      text="Save",
                      bg="#4CAF50",
                      fg="white",
                      width=15,
                      command=save).pack(pady=15)
    
    def open_profile():

        win = tk.Toplevel()

        win.title("My Profile")

        win.geometry("350x300")

        win.configure(bg="#f5f5f5")

        #================== DATA =================

        user_data = db.get_user_by_id(user_id)

        username = user_data[1]
        role_name = user_data[3]

        #================TITLE =================

        tk.Label(win,
                 text="User profile",
                 font=("Arial", 16, "bold"),
                 bg="#f5f5f5",
                 fg="#333").pack(pady=15)
        
        #================ PROFILE ICON =================

        tk.Label(win,
                 text="👤",
                 font=("Arial", 45),
                 bg="#f5f5f5").pack()
        
        #================ USERNAME =================

        tk.Label(win,
                 text=f"Username: {username}",
                 font=("Arial", 12, "bold"),
                 bg="#f5f5f5").pack(pady=10)
        
        #================ ROLE =================

        tk.Label(win,
                 text=f"Role: {role_name}",
                 font=("Arial", 11),
                 bg="#f5f5f5",
                 fg="#666").pack()
        
        #================ TOTAL EXPENSE ================
        
        total = db.get_total_expense(user_id)

        tk.Label(win,
                 text=f"Total Expense: ₹ {total}",
                 font=("Arial", 12),
                 bg="#f5f5f5",
                 fg="#4CAF50").pack(pady=15)
        
        #================ CLOSE BUTTON =================

        tk.Button(win,
                  text="Close",
                  width=15,
                  bg="#2196F3",
                  fg="white",
                  command=win.destroy).pack(pady=15)

    def change_password():

        win = tk.Toplevel()

        win.title("Change password")
        
        win.geometry("300x220")

        tk.Label(win, text="New Password",
                 font=("Arial", 11)).pack(pady=10)
        
        new_pass = tk.Entry(win, show="*", width=25)
        new_pass.pack()

        tk.Label(win,
                 text="Confirm password",
                 font=("Arial", 11)).pack(pady=10)
        
        confirm_pass = tk.Entry(win, show="*", width=25)
        confirm_pass.pack()

        def save_password():

            p1 = new_pass.get()
            p2 = confirm_pass.get()

            if p1 == "" or p2== "":
                show_popup("Error",
                           "Fields cannot be emptyb")
                return
            
            if p1 != p2:
                show_popup("Error",
                           "Passwords do not match")
                return
            
            import bcrypt

            hashed = bcrypt.hashpw(
                p1.encode(),
                bcrypt.gensalt()
            )

            db.change_password(user_id, hashed)

            show_popup("Success",
                       "Password changed!")
            
            win.destroy()

        tk.Button(win,
                  text="Save",
                  bg="#4CAF50",
                  fg="white",
                  width=15,
                  command=save_password).pack(pady=20)    

    def add_expense():

        win = tk.Toplevel(window)
        win.title("Add Expense")
        win.geometry("300x250")

        tk.Label(win, text="Category").pack(pady=5)

        cat = tk.Entry(win)
        cat.pack()

        tk.Label(win, text="Amount").pack(pady=5)

        amt = tk.Entry(win)
        amt.pack()

        def save():

            try:
                amount = float(amt.get())
            except:
                return

            db.add_expense(user_id,
                           datetime.now().strftime("%Y-%m-%d"),
                           cat.get(),
                           amount)

            win.destroy()
            refresh_all()

        tk.Button(win,
                  text="Save",
                  bg="#4CAF50",
                  fg="white",
                  command=save).pack(pady=10)

    def delete_expense():

        selected = tree.selection()

        if not selected:
            return

        item = tree.item(selected[0])

        db.delete(item["values"][0])

        refresh_all()

    def edit_expense():

        selected = tree.selection()

        if not selected:
            return

        item = tree.item(selected[0])
        values = item["values"]

        win = tk.Toplevel(window)
        win.title("Edit Expense")
        win.geometry("300x250")

        tk.Label(win, text="Category").pack()

        cat = tk.Entry(win)
        cat.insert(0, values[2])
        cat.pack()

        tk.Label(win, text="Amount").pack()

        amt = tk.Entry(win)
        amt.insert(0, values[3].replace("₹ ", ""))
        amt.pack()

        def update():

            db.update_expense(values[0],
                              cat.get(),
                              float(amt.get()))

            win.destroy()
            refresh_all()

        tk.Button(win,
                  text="Update",
                  bg="#2196F3",
                  fg="white",
                  command=update).pack(pady=10)

    def delete_user():

        if role != "admin":
            return

        win = tk.Toplevel(window)
        win.title("Delete User")
        win.geometry("250x200")

        users = db.get_users()

        user_map = {u[1]: u[0] for u in users}

        combo = ttk.Combobox(win,
                             values=list(user_map.keys()))
        combo.pack(pady=10)

        def delete():

            db.delete_user(user_map[combo.get()])

            win.destroy()

        tk.Button(win,
                  text="Delete",
                  bg="red",
                  fg="white",
                  command=delete).pack(pady=10)

    # ================= SIDEBAR =================
    tk.Label(sidebar,
             text="MENU",
             bg="#2c3e50",
             fg="white",
             font=("Arial", 14, "bold")).pack(pady=15)

    btn_frame = tk.Frame(sidebar, bg="#2c3e50")

    visible = [False]

    def toggle_menu():

        if visible[0]:
            btn_frame.pack_forget()
            visible[0] = False
        else:
            btn_frame.pack(pady=10)
            visible[0] = True

    tk.Button(sidebar,
              text="☰ Menu",
              bg="#34495e",
              fg="white",
              width=16,
              command=toggle_menu).pack(pady=10)

    # ================= BUTTON MAKER =================
    def make(text, cmd, color, hover_c, r, c):

        b = tk.Button(btn_frame,
                      text=text,
                      command=cmd,
                      bg=color,
                      fg="white",
                      width=15)

        b.grid(row=r,
               column=c,
               padx=5,
               pady=5)

        b.bind("<Enter>",
               lambda e: b.config(bg=hover_c))

        b.bind("<Leave>",
               lambda e: b.config(bg=color))

    # ================= BUTTONS =================
    make("Add", add_expense,
         "#4CAF50", "#45a049", 0, 0)

    make("Delete", delete_expense,
         "#f44336", "#d32f2f", 0, 1)

    make("Edit", edit_expense,
         "#2196F3", "#1976D2", 0, 2)

    make("Chart",
         lambda: charts.show_chart(user_id),
         "#9C27B0", "#7B1FA2", 1, 0)

    make("Monthly",
         lambda: charts.show_monthly_chart(user_id),
         "#673AB7", "#512DA8", 1, 1)

    make("Last 7 Days",
         lambda: charts.show_last7days_chart(user_id),
         "#795548", "#5D4037", 1, 2)

    make("Export",
         lambda: export.export_to_csv(user_id),
         "#FF9800", "#FB8C00", 2, 0)

    make("Refresh",
         refresh_all,
         "#607D8B", "#455A64", 2, 1)

    make("Logout",
         logout,
         "#000000", "#333333", 2, 2)
    
    make("password",
         change_password,
         "#E91E63",
         "#C2185B",
         3,
         1)
    
    make("profile",
         open_profile,
         "#009688",
         "#00796B",
         3,
         2)
    
    make("Add Income",
     add_income,
     "#009688",
     "#00796B",
     4,
     0)
    
    make("PDF Export",
     lambda: pdf_export.export_pdf(user_id),
     "#E91E63",
     "#C2185B",
     5,
     0)

    tk.Button(btn_frame,
              text="Delete User",
              command=delete_user,
              bg="gray",
              fg="white",
              width=15).grid(row=3,
                             column=0,
                             pady=5)

    # ================= START =================
    load_months()
    load_data()
    show_graph_embed()
    apply_theme()