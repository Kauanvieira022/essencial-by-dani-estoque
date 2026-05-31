import customtkinter as ctk

from database.create_tables import create_tables
from views.main_window import MainWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

create_tables()

app = MainWindow()
app.mainloop()