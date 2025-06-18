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
        for Page in (UserPage, ResourcePage, BookerPage, ViewerPage):
            page = Page(self.notebook, self)
            self.pages[Page.__name__] = page
            self.notebook.add(page, text=page.title)

class UserPage(ttk.Frame):
    title = "User Portal"
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller 
        
        ttk.Button(self, text="Create New User", command=self.create_user).pack(pady=5)
        ttk.Button(self, text="Edit User Profile", command=self.edit_user).pack(pady=5)
        ttk.Button(self, text="Delete User", command=self.delete_user).pack(pady=5)
        ttk.Button(self, text="Sign In", command=self.sign_in).pack(pady=5)
    
    def create_user(self):
        user_name = dialog.askstring("Create New User", "Enter Username:")
        if user_name:
            # Here you would add logic to save the resource
            msgbox.showinfo("Success", f"New user '{user_name}' created successfully.")
    
    def edit_user(self):
        user_name = dialog.askstring("Edit Resource", "Enter resource name to edit:")
        if user_name: #exists:
            resource_key = dialog.askstring("Resource", "Enter resource name to edit:")
            if user_name:
                # Here you would add logic to edit the resource
                msgbox.showinfo("Success", f"Resource '{user_name}' edited successfully.")
        else:
            msgbox.showerror("Error", "Resource not found.")
        
    def delete_user(self):
        user_name = dialog.askstring("Delete Resource", "Enter resource name to delete:")
        if user_name:
            # Here you would add logic to delete the resource
            msgbox.showinfo("Success", f"Resource '{user_name}' deleted successfully.")    
    
    def sign_in(self):
        a+=1
    
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
        else:
            msgbox.showerror("Error", "Resource not found.")
            
    def edit_resource(self):
        resource_name = dialog.askstring("Edit Resource", "Enter resource name to edit:")
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
        else:
            msgbox.showerror("Error", "Resource not found.")
        
class BookerPage(ttk.Frame):
    title = "Booking System"
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller
        
        ttk.Button(self, text="Create Booking", command=self.create_booking).pack(pady=5)
        ttk.Button(self, text="Edit Booking", command=self.edit_booking).pack(pady=5)
        ttk.Button(self, text="Delete Booking", command=self.delete_booking).pack(pady=5)
    
    def create_booking(self):
        booking_name = dialog.askstring("Create Booking", "Enter booking name:")
        if booking_name:
            # Here you would add logic to save the resource
            msgbox.showinfo("Success", f"Booking '{booking_name}' created successfully.")
        else:
            msgbox.showerror("Error", "Booking not found.")
        
    def edit_booking(self):
        booking_name = dialog.askstring("Edit Booking", "Enter booking name to edit:")
        if booking_name:
                # Here you would add logic to edit the resource
                msgbox.showinfo("Success", f"Booking '{booking_name}' edited successfully.")
        else:
            msgbox.showerror("Error", "Booking not found.")
        
    def delete_resource(self):
        booking_name = dialog.askstring("Delete Booking", "Enter booking name to delete:")
        if booking_name:
            # Here you would add logic to delete the resource
            msgbox.showinfo("Success", f"Booking '{booking_name}' deleted successfully.")
        else:
            msgbox.showerror("Error", "Booking not found.")
        
class ViewerPage(ttk.Frame):
    title = "Resource/Booking Viewer"
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller

MyApp = App()
MyApp.mainloop()