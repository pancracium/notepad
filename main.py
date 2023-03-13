#NOTEPAD [b0.5 (06-03-2023)]

#Import necessary modules
import tkinter as tk
import datetime
import tkinter.messagebox as msgbox
import tkinter.filedialog as filedialog
from tkinter import PhotoImage
from tkinter import ttk

#Create a class for the main application
class Application(tk.Frame):
    def __init__(self, master=None):
        """Initiate the app."""
        super().__init__(master)
        self.pack(expand=True, fill="both")
        #Set up values
        self.saved_text = ""
        self.char_count = 0
        self.word_count = 0
        self.line_count = 0
        self.counter_visible = False
        self.file_path = None
        #Initiate methods.
        self.load_images()
        self.create_widgets()
        self.bind_keys()
    
    def load_images(self):
        """Load all images."""
        #Icons
        self.question_icon = PhotoImage(file="images/question.png")
        self.warning_image = PhotoImage(file="images/warning.png")
        self.error_icon = PhotoImage(file="images/error.png")
        #Menu images
        self.copy_image = PhotoImage(file="images/copy.png").subsample(2, 2)
        self.cut_image = PhotoImage(file="images/cut.png").subsample(2, 2)
        self.exit_image = PhotoImage(file="images/exit.png").subsample(2, 2)
        self.find_image = PhotoImage(file="images/find.png").subsample(2, 2)
        self.date_image = PhotoImage(file="images/insert_date.png").subsample(2, 2)
        self.new_image = PhotoImage(file="images/new.png").subsample(2, 2)
        self.open_image = PhotoImage(file="images/open.png").subsample(2, 2)
        self.paste_image = PhotoImage(file="images/paste.png").subsample(2, 2)
        self.redo_image = PhotoImage(file="images/redo.png").subsample(2, 2)
        self.replace_image = PhotoImage(file="images/replace.png").subsample(2, 2)
        self.save_as_image = PhotoImage(file="images/save_as.png").subsample(2, 2)
        self.select_all_image = PhotoImage(file="images/select_all.png").subsample(2, 2)
        self.toggle_counter_bar_image = PhotoImage(file="images/toggle_counter_bar.png").subsample(2, 2)
        self.undo_image = PhotoImage(file="images/undo.png").subsample(2, 2)
        self.zoom_in_image = PhotoImage(file="images/zoom_in.png").subsample(2, 2)
        self.zoom_out_image = PhotoImage(file="images/zoom_out.png").subsample(2, 2)
        self.zoom_reset_image= PhotoImage(file="images/zoom_reset.png").subsample(2, 2)
        self.zoom_to_image = PhotoImage(file="images/zoom_to.png").subsample(2, 2)

    def create_widgets(self):
        """Create the widgets."""
        #Create the text widget
        self.text = tk.Text(self)
        self.text.pack(expand=True, fill="both")
        self.text.bind("<KeyRelease>", lambda event: self.update_counter())
        #Set up a font
        self.text["font"] = ("Consolas", 11)
        #Create a menu bar
        self.menu_bar = tk.Menu(self.master)
        self.master.configure(menu=self.menu_bar)
        #Create a File tab in the menu bar
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save as", accelerator="CTRL+S", command=self.save_as, compound=tk.LEFT, image=self.save_as_image)
        self.file_menu.add_command(label="Open", accelerator="CTRL+O", command=self.open_file, compound=tk.LEFT, image=self.open_image)
        self.file_menu.add_command(label="New", accelerator="CTRL+N", command=self.new_note, compound=tk.LEFT, image=self.new_image)
        self.file_menu.add_command(label="Exit", accelerator="CTRL+Q", command=self.quit_app, compound=tk.LEFT, image=self.exit_image)
        #Create an Edit tab in the menu bar
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", accelerator="CTRL+Z", command=self.text.edit_undo, compound=tk.LEFT, image=self.undo_image)
        self.edit_menu.add_command(label="Redo", accelerator="CTRL+Y", command=self.text.edit_redo, compound=tk.LEFT, image=self.redo_image)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", accelerator="CTRL+F", command=self.find, compound=tk.LEFT, image=self.find_image)
        self.edit_menu.add_command(label="Replace", accelerator="CTRL+H", command=self.replace, compound=tk.LEFT, image=self.replace_image)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", accelerator="CTRL+X", command=self.cut, compound=tk.LEFT, image=self.cut_image)
        self.edit_menu.add_command(label="Copy",  accelerator="CTRL+C",command=self.copy, compound=tk.LEFT, image=self.copy_image)
        self.edit_menu.add_command(label="Paste",  accelerator="CTRL+V",command=self.paste, compound=tk.LEFT, image=self.paste_image)
        self.edit_menu.add_command(label="Select all",  accelerator="CTRL+A",command=self.select_all, compound=tk.LEFT, image=self.select_all_image)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Insert current date", accelerator="CTRL+D", command=self.insert_date, compound=tk.LEFT, image=self.date_image)
        #Create a View tab in the menu bar
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_checkbutton(label=f"Counter bar", accelerator="CTRL+B", command=self.toggle_counter, compound=tk.LEFT, image=self.toggle_counter_bar_image, variable=self.counter_visible)
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Zoom in", accelerator="CTRL+=", command=self.zoom_in, compound=tk.LEFT, image=self.zoom_in_image)
        self.view_menu.add_command(label="Zoom out", accelerator="CTRL+-", command=self.zoom_out, compound=tk.LEFT, image=self.zoom_out_image)
        self.view_menu.add_command(label="Reset zoom", accelerator="CTRL+0", command=self.zoom_reset, compound=tk.LEFT, image=self.zoom_reset_image)
        self.view_menu.add_command(label="Zoom to", accelerator="CTRL+\\", command=self.zoom_to, compound=tk.LEFT, image=self.zoom_to_image)
        #Create a frame to hold the counters
        self.counter_frame = tk.Frame(self.master)
        self.word_count_label = tk.Label(self.counter_frame, text=f"Words: {self.word_count}")
        self.word_count_label.pack(side="left", padx=(10, 5))
        self.char_count_label = tk.Label(self.counter_frame, text=f"Chars: {self.char_count}")
        self.char_count_label.pack(side="left", padx=5)
        self.line_count_label = tk.Label(self.counter_frame, text=f"Lines: {self.line_count}")
        self.line_count_label.pack(side="left", padx=5)
        self.counter_frame.pack(side="bottom", fill="x")
        self.counter_frame.pack_forget()
    
    def bind_keys(self):
        """Binds all methods to their corresponding keys."""
        #Undo CTRL + Z
        self.master.bind("<Control-z>", lambda event: self.text.edit_undo())
        self.master.bind("<Control-Z>", lambda event: self.text.edit_undo())
        #Redo CTRL + Y
        self.master.bind("<Control-y>", lambda event: self.text.edit_redo())
        self.master.bind("<Control-Y>", lambda event: self.text.edit_redo())
        #Quit CTRL + Q
        self.master.bind("<Control-q>", lambda event: self.quit_app())
        self.master.bind("<Control-q>", lambda event: self.quit_app())
        #Save as CTRL + S
        self.master.bind("<Control-s>", lambda event: self.save_as())
        self.master.bind("<Control-S>", lambda event: self.save_as())
        #Find CTRL + F
        self.master.bind("<Control-f>", lambda event: self.find())
        self.master.bind("<Control-F>", lambda event: self.find())
        #Replace CTRL + H
        self.master.bind("<Control-h>", lambda event: self.replace())
        self.master.bind("<Control-H>", lambda event: self.replace())
        #Cut CTRL + X
        self.master.bind("<Control-x>", lambda event: self.cut())
        self.master.bind("<Control-X>", lambda event: self.cut())
        #Copy CTRL + C
        self.master.bind("<Control-c>", lambda event: self.copy())
        self.master.bind("<Control-C>", lambda event: self.copy())
        #Paste CTRL + V
        self.master.bind("<Control-v>", lambda event: self.paste())
        self.master.bind("<Control-V>", lambda event: self.paste())
        #Select all CTRL + A
        self.master.bind("<Control-a>", lambda event: self.select_all())
        self.master.bind("<Control-A>", lambda event: self.select_all())
        #Open CTRL + O
        self.master.bind("<Control-o>", lambda event: self.open_file())
        self.master.bind("<Control-O>", lambda event: self.open_file())
        #Insert current date CTRL + D
        self.master.bind("<Control-d>", lambda event: self.insert_date())
        self.master.bind("<Control-D>", lambda event: self.insert_date())
        #New CTRL + N
        self.master.bind("<Control-n>", lambda event: self.new_note())
        self.master.bind("<Control-N>", lambda event: self.new_note())
        #Reset zoom CTRL + 0
        self.master.bind("<Control-0>", lambda event: self.zoom_reset())
        #Zoom in CTRL + =
        self.master.bind("<Control-equal>", lambda event: self.zoom_in())
        #Zoom out CTRL + -
        self.master.bind("<Control-minus>", lambda event: self.zoom_out())
        #Zoom to CTRL + \
        self.master.bind("<Control-backslash>", lambda event: self.zoom_to())
        #Toggle counter bar CTRL + B
        self.master.bind("<Control-b>", lambda event: self.toggle_counter())
        self.master.bind("<Control-B>", lambda event: self.toggle_counter())

    def cut(self):
        """Cut the selected text."""
        self.text.event_generate("<<Cut>>")
    
    def copy(self):
        """Copy the selected text."""
        self.text.event_generate("<<Copy>>")
    
    def paste(self):
        """Paste the clipboard content."""
        self.text.event_generate("<<Paste>>")
    
    def select_all(self):
        """Select all the text."""
        self.text.tag_add("sel", "1.0", "end")

    def find(self):
        """Create the find overlay."""
        #Create a new toplevel window
        find_window = tk.Toplevel(self)
        find_window.title("Find")

        #Create a label and entry for the user to enter his search query
        tk.Label(find_window, text="Find:").grid(row=0, column=0, sticky="w")
        query_entry = tk.Entry(find_window)
        query_entry.grid(row=0, column=1, sticky="we")

        #Add a button which will search for the query and highlight the matches in yellow
        def find_matches():
            #Make old matches stop being highlighted
            self.text.tag_remove("highlight", "1.0", "end")
            #Get the search query
            query = query_entry.get()
            #Highlight matches in yellow
            if query:
                start = "1.0"
                while True:
                    start = self.text.search(query, start, stopindex="end")
                    if not start:
                        break
                    end = f"{start}+{len(query)}c"
                    self.text.tag_add("highlight", start, end)
                    start = end
                self.text.tag_config("highlight", background="yellow")
                find_window.destroy()
        tk.Button(find_window, text="Find", command=find_matches).grid(row=0, column=2, sticky="e")
    
    def replace(self):
        """Create the replace overlay."""
        #Create a new toplevel window
        replace_window = tk.Toplevel(self)
        replace_window.title("Replace")

        #Create a label and entry for the user to enter his search query
        tk.Label(replace_window, text="Find:").grid(row=0, column=0, sticky="w")
        find_entry = tk.Entry(replace_window)
        find_entry.grid(row=0, column=1, sticky="we")

        #Create a label and entry for the user to enter the replacement query
        tk.Label(replace_window, text="Replace with:").grid(row=1, column=0, sticky="w")
        replace_entry = tk.Entry(replace_window)
        replace_entry.grid(row=1, column=1, sticky="we")

        #Add a button which will replace all occurrences of the find query with the replace query
        def replace_matches():
            #Get the search query and replacement
            find_query = find_entry.get()
            replace_query = replace_entry.get()
            #Replace matches
            if find_query and replace_query:
                text = self.text.get("1.0", "end-1c")
                updated_text = text.replace(find_query, replace_query)
                self.text.delete("1.0", "end")
                self.text.insert("1.0", updated_text)
                replace_window.destroy()
        tk.Button(replace_window, text="Replace All", command=replace_matches).grid(row=2, column=2, sticky="e")
    
    def zoom_in(self):
        """Increase the font size of the text by 1."""
        current_font = self.text["font"].split()[0]
        current_size = self.text["font"].split()[1]
        new_size = int(current_size) + 1
        self.text.config(font=(current_font, new_size))
    
    def zoom_out(self):
        """Decrease the font size of the text by 1."""
        current_font = self.text["font"].split()[0]
        current_size = self.text["font"].split()[1]
        new_size = int(current_size) - 1
        if new_size > 5:
            self.text.config(font=(current_font, new_size))
        else:
            msgbox.showerror(title="Error", message="Cannot make font smaller than 5!")
    
    def zoom_reset(self):
        """Change font size to 11."""
        current_font = self.text["font"].split()[0]
        self.text.config(font=(current_font, 11))

    def zoom_to(self):
        """Zoom to a specific number."""
        #Create a new toplevel window
        zoom_window = tk.Toplevel(self)
        zoom_window.title("Zoom to")
        #Create a label and entry for the user to enter the desired zoom number
        tk.Label(zoom_window, text="Zoom number: ").grid(row=0, column=0, sticky="w")
        number_entry = tk.Entry(zoom_window)
        number_entry.grid(row=0, column=1, sticky="we")
        #Add a button which will change the zoom number to the desired number
        def zoom_to_command():
            #Get the number
            number = number_entry.get()
            #Change the font size if the number is greater than 5
            if number:
                size = int(number)
                if size < 5:
                    msgbox.showerror(title="Error", message="Cannot make font smaller than 5!")
                else:
                    current_font = self.text["font"].split()[0]
                    self.text.config(font=(current_font, size))
                zoom_window.destroy()
        tk.Button(zoom_window, text="Zoom", command=zoom_to_command).grid(row=0, column=1, sticky="e")
    
    def insert_date(self):
        """Insert the current date to the text."""
        #Get the current date
        date = datetime.datetime.now()
        day = date.day
        month = date.month
        year = date.year
        hour = date.hour
        minute = date.minute
        #Insert the date in the desired format
        self.text.insert("insert", f"{day}/{month}/{year} {hour}:{minute}")
    
    def new_note(self):
        """Creates a new note, erasing all previous text."""
        #Get the text
        text = self.text.get("1.0", "end-1c")
        #Delete all text if the text is saved or if there's no text
        if text.isspace() or text == "" or text == self.saved_text: 
            self.text.delete("1.0", "end-1c")
        else:
            choice = msgbox.askyesnocancel(title="Warning", message="Do you want to save unsaved changes?")
            if choice: #Save the file if the user clicks yes
                self.save_as()
            elif not choice:
                if choice == None: #Do nothing if the user cancels
                    pass
                else: #Delete all text if the user clicks no
                    self.text.delete("1.0", "end-1c")
    
    def toggle_counter(self):
        """Toggle the visibility of the counter bar."""
        self.counter_visible = not self.counter_visible
        if self.counter_visible:
            self.counter_frame.pack(side="left", fill="x")
            self.view_menu.entryconfig(0, label="Counter bar", accelerator=str(self.counter_visible))
        else:
            self.counter_frame.pack_forget()
            self.view_menu.entryconfig(0, label="Counter bar", accelerator=str(self.counter_visible))

    def update_counter(self):
        """Update the word, character and line counters."""
        #Update only if the counter is visible
        if not self.counter_visible: 
            return "counter not visible"
        #Get the text
        text = self.text.get("1.0", "end-1c")
        #Update the character count
        self.char_count = len(text.replace("\n", ""))
        #Update the word count
        words = [word for word in text.split(" ") if word != "" or word != "\n"]
        self.word_count = len(words)
        #Update the line count
        lines = text.split("\n")
        self.line_count = len(lines)
        #Update the labels
        self.char_count_label.config(text=f"Chars: {self.char_count}")
        self.word_count_label.config(text=f"Words: {self.word_count}")
        self.line_count_label.config(text=f"Lines: {self.line_count}")

    def save_as(self):
        """Save the written text as a file."""
        #Prompt the user for a file name, extension an location
        file_path = filedialog.asksaveasfilename(initialdir="~/Desktop", initialfile="note.txt", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        #Save the text the user has written to the selected location
        if file_path:
            text = self.text.get("1.0", "end-1c")
            with open(file_path, "w") as file:
                file.write(text)
            self.saved_text = self.text.get("1.0", "end-1c")
    
    def open_file(self):
        """Opens the selected file."""
        #Opens a prompt window which ask the user for the desired file to be opened
        file_path = filedialog.askopenfilename(
            title="Open", 
            filetypes=[("Text Files", ".txt"), ("All Files", "*.*")]
            )

        #If the user gives a file, open it
        if file_path:
            self.file_path = file_path
            with open(file_path, "r") as f:
                file_contents = f.read()
            self.text.delete("1.0", "end")
            self.text.insert("1.0", file_contents)
            self.saved_text = file_contents
    
    def quit_app(self):
        """Asks to the user if he wants to save before closing."""
        #Get the text
        text = self.text.get("1.0", "end-1c")
        #Close if the text is saved or if there's no text
        if text.isspace() or text == "" or text == self.saved_text: 
            self.master.destroy()
        else:
            choice = msgbox.askyesnocancel(title="Warning", message="Do you want to save unsaved changes?")
            if choice: #Save the file if the user clicks yes
                self.save_as()
            elif not choice:
                if choice == None: #Do nothing if the user cancels
                    pass
                else: #Close the app if the user clicks no
                    self.master.destroy()

#Set up window's properties and create the main loop
WIDTH, HEIGHT = 1080, 720
root = tk.Tk()
root.geometry(f"1080x720+{root.winfo_screenwidth()//2 - WIDTH // 2}+{root.winfo_screenheight()//2 - HEIGHT // 2}")
root.wm_title("Notepad")
root.wm_iconbitmap("images/icon.ico")
app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", app.quit_app)
app.mainloop()