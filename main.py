import customtkinter as ctk

from database.create_tables import create_tables
from views.main_window import MainWindow


def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    create_tables()

    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
