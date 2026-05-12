from database import db
from ui.login import open_login

if __name__ == '__main__':
    try:
        db.init_db()

        print("App Started")

        open_login()   # 👈 login screen

    except Exception as e:
        print("ERROR:", e)