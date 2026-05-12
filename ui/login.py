import tkinter as tk
from database import db
from ui import dashboard
import bcrypt

# ================= CUSTOM POPUP =================

def show_popup(title, msg):

    pop = tk.Toplevel()
    pop.title(title)
    pop.geometry("260x130")
    pop.resizable(False, False)

    tk.Label(pop,
             text=msg,
             font=("Arial", 11)).pack(pady=20)

    tk.Button(pop,
              text="OK",
              width=10,
              bg="#4CAF50",
              fg="white",
              command=pop.destroy).pack()

# ================= LOGIN WINDOW =================

def open_login():

    # ================= LOGIN =================

    def login_user():

        username = entry_username.get()
        password = entry_password.get()

        user = db.get_user(username)

        if user:

            if bcrypt.checkpw(password.encode(), user[2]):

                show_popup("Success",
                           "Login successful!")

                window.withdraw()

                dashboard.open_dashboard(
                    user[0],
                    user[3],
                    window
                )

            else:

                show_popup("Error",
                           "Invalid password")

        else:

            show_popup("Error",
                       "User not found")

    # ================= REGISTER =================

    def register_user():

        username = entry_username.get()
        password = entry_password.get()

        if username == "" or password == "":

            show_popup("Error",
                       "Fields cannot be empty")

            return

        try:

            hashed = bcrypt.hashpw(
                password.encode(),
                bcrypt.gensalt()
            )

            success = db.register(username, hashed)

            if success:

                show_popup("Success",
                           "User Registered!")

            else:

                show_popup("Error",
                           "Username already exists!")

        except Exception as e:

            print("Registration error:", e)

            show_popup("Error", str(e))

    def forget_password():

        win = tk.Toplevel()

        win.title("Forget Password")

        win.geometry("320x250")

        tk.Label(win,
                 text="Username").pack(pady=5)
        
        user_entry = tk.Entry(win, width=30)
        user_entry.pack()

        tk.Label(win,
                 text="New Password").pack(pady=5)
        
        new_pass = tk.Entry(win,
                            show="*",
                            width=30)
        
        new_pass.pack()

        tk.Label(win,
                 text="Confirm Password").pack(pady=5)
        
        confirm_pass = tk.Entry(win,
                                show="*",
                                width=30)
        
        confirm_pass.pack()

        def save():

            username = user_entry.get()

            p1 = new_pass.get()
            p2 = confirm_pass.get()

            if p1 != p2:

                show_popup("Error",
                           "Passwords do not match")
                
                return
            
            user = db.get_user(username)

            if user is None:

                show_popup("Error",
                           "User not found")
                
                return
            
            hashed = bcrypt.hashpw(
                p1.encode(),
                bcrypt.gensalt()
            )

            db.change_password(user[0], hashed)

            show_popup("Success",
                       "Password Changed!")
            
            win.destroy()

        tk.Button(win,
                  text="Save",
                  bg="#4CAF50",
                  fg="white",
                  command=save).pack(pady=15)


    # ================= UI =================

    window = tk.Tk()

    window.title("Expense Tracker Login")

    window.geometry("350x300")

    window.configure(bg="#f5f5f5")

    # ================= TITLE =================

    tk.Label(window,
             text="Expense Tracker",
             font=("Arial", 20, "bold"),
             bg="#f5f5f5",
             fg="#333").pack(pady=20)

    # ================= USERNAME =================

    tk.Label(window,
             text="Username",
             font=("Arial", 11),
             bg="#f5f5f5").pack()

    entry_username = tk.Entry(window,
                              width=30,
                              font=("Arial", 11))

    entry_username.pack(pady=5)

    # ================= PASSWORD =================

    tk.Label(window,
             text="Password",
             font=("Arial", 11),
             bg="#f5f5f5").pack()

    entry_password = tk.Entry(window,
                              show="*",
                              width=30,
                              font=("Arial", 11))

    entry_password.pack(pady=5)

    # ================= BUTTONS =================

    tk.Button(window,
              text="Login",
              width=20,
              bg="#4CAF50",
              fg="white",
              font=("Arial", 10, "bold"),
              command=login_user).pack(pady=12)

    tk.Button(window,
              text="Signup",
              width=20,
              bg="#2196F3",
              fg="white",
              font=("Arial", 10, "bold"),
              command=register_user).pack()
    
    tk.Button(window,
              text="Forget Password",
              width=20,
              bg="#FF9800",
              fg="white",
              command=forget_password).pack(pady=10)

    window.mainloop()