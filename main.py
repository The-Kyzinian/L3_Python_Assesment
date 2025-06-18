import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog as dialog
from tkinter import messagebox as msgbox
import json
import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.pages = {}
        for Page in (ResourcePage, BookerPage, UserPage, ViewerPage):
            page = Page(self.notebook, self)
            self.pages[Page.__name__] = page
            self.notebook.add(page, text=page.title)

class ResourcePage(ttk.Frame):
    title = "Resource Creator/Editor"
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller
        
        ttk.Button(self, text="Create Resource", command=self.create_resource).pack(pady=5)
        ttk.Button(self, text="Edit Resource", command=self.edit_resource).pack(pady=5)
        ttk.Button(self, text="Delete Resource", command=self.delete_resource).pack(pady=5)
        
    def create_resource(self):
        resource_name = dialog.askstring("Create Resource", "Enter resource name:")
        if resource_name:
            # Here you would add logic to save the resource
            msgbox.showinfo("Success", f"Resource '{resource_name}' created successfully.")
    def edit_resource(self):
        resource_name = dialog.askstring("Edit Resource", "Enter resource name to edit:")
        if resource_name: #exists:
            resource_key = dialog.askstring("Resource", "Enter resource name to edit:")
            if resource_name:
                # Here you would add logic to edit the resource
                msgbox.showinfo("Success", f"Resource '{resource_name}' edited successfully.")
        else:
            msgbox.showerror("Error", "Resource not found.")
        
    def delete_resource(self):
        resource_name = dialog.askstring("Delete Resource", "Enter resource name to delete:")
        if resource_name:
            # Here you would add logic to delete the resource
            msgbox.showinfo("Success", f"Resource '{resource_name}' deleted successfully.")
    
        
class BookerPage(ttk.Frame):
    title = "Booking System"
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller
    
class UserPage(ttk.Frame):
    title = "Booking System"
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller 
        
class ViewerPage(ttk.Frame):
    title = "Resource/Booking Viewer"
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller

MyApp = App()
MyApp.mainloop()