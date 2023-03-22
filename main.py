import tkinter as tk
from app import NotepadApp

#Set up window's properties and create the main loop
WIDTH, HEIGHT = 1080, 720
root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}+{root.winfo_screenwidth()//2 - WIDTH // 2}+{root.winfo_screenheight()//2 - HEIGHT // 2}")
root.wm_title("Notepad")
root.wm_iconbitmap("images/icon.ico")
app = NotepadApp(master=root)
root.protocol("WM_DELETE_WINDOW", app.quit_app)
app.mainloop()