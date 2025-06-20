import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog as dialog
from tkinter import messagebox as msgbox
import json
import datetime

class get_users:
    def __init__(self, filepath="users.json"):
        self.filepath = filepath
        self.load_users()
        self.save_users()
    def load_users(self):
        try:
            with open(self.filepath, 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = {}
        except json.JSONDecodeError:
            self.users = {}
            
    def save_users(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.users, file, indent=4)

class get_resources:
    def __init__(self, filepath="resources.json"):
        self.filepath = filepath
        self.load_resources()
        self.save_resources()
    def load_resources(self):
        try:
            with open(self.filepath, 'r') as file:
                self.resources = json.load(file)
        except FileNotFoundError:
            self.resources = {}
        except json.JSONDecodeError:
            self.resources = {}
    def save_resources(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.resources, file, indent=4)
            
class get_bookings:
    def __init__(self, filepath="bookings.json"):
        self.filepath = filepath
        self.load_bookings()
        self.save_bookings()
    def load_bookings(self):
        try:
            with open(self.filepath, 'r') as file:
                self.bookings = json.load(file)
        except FileNotFoundError:
            self.bookings = {}
        except json.JSONDecodeError:
            self.bookings = {}
    def save_bookings(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.bookings, file, indent=4)

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
    def __init__(self, parent, main_app):
        super().__init__(parent, padding=10)
        self.main_app = main_app
        self.users = get_users() 
        
        ttk.Button(self, text="Create New User", command=self.create_user).pack(pady=5)
        ttk.Button(self, text="Edit User Profile", command=self.edit_user).pack(pady=5)
        ttk.Button(self, text="Delete User", command=self.delete_user).pack(pady=5)
    
    def create_user(self):
        while True:
            user_name = dialog.askstring("Create New User", "Enter Username:")
            if user_name not in self.users.users:
                break
            else:
                msgbox.showerror("Error", "User already exists.")
        full_name = dialog.askstring("Full Name", "Enter Full Name:")
        password = dialog.askstring("Password", "Enter Password:", show='*')
        self.users.users[user_name] = {"full_name": full_name, "password": password}
        self.users.save_users()
        msgbox.showinfo("Success", f"New user '{user_name}' created successfully.")
        
    def edit_user(self): 
        while True:    
            user_name = dialog.askstring("Edit User", "Enter username to be edited:")
            if user_name in self.users.users:
                password = dialog.askstring("Login", "Enter password to edit user:", show='*')
                if password == self.users.users[user_name]["password"]:
                    while True:
                        new_username = dialog.askstring("Edit Username", "Enter new username:", initialvalue=user_name)
                        # If username changed and is not taken
                        if new_username != user_name:
                            if new_username in self.users.users:
                                msgbox.showerror("Error", "New username already exists.")
                            break
                    self.users.users[new_username] = self.users.users.pop(user_name)
                    user_name = new_username  
                    full_name = dialog.askstring("Edit Full Name", "Enter new full name:", initialvalue=self.users.users[user_name]["full_name"])
                    new_password = dialog.askstring("Edit Password", "Enter new password (leave blank to keep current):", show='*')
                    if full_name:
                        self.users.users[user_name]["full_name"] = full_name
                    if new_password:
                        self.users.users[user_name]["password"] = new_password
                    self.users.save_users()
                    msgbox.showinfo("Success", f"User '{user_name}' updated successfully.")
                    break
                else:
                    msgbox.showerror("Error", "Incorrect password.")
                    break
            else:
                msgbox.showerror("Error", "User does not exist.")
        
    def delete_user(self):
        while True:
            user_name = dialog.askstring("Delete User", "Enter username to be deleted:")
            if user_name in self.users.users:
                password = dialog.askstring("Login", "Enter password to delete user:", show='*')
                if password == self.users.users[user_name]["password"]:
                    confirm = msgbox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{user_name}'?")
                    if confirm:
                        del self.users.users[user_name]
                        self.users.save_users()
                        msgbox.showinfo("Success", f"User '{user_name}' deleted successfully.")
                        break
                    else:
                        msgbox.showinfo("Cancelled", "User deletion cancelled.")
                        break
                else:
                    msgbox.showerror("Error", "Incorrect password.")
                    break
            else:
                msgbox.showerror("Error", "User does not exist.")    
    
class ResourcePage(ttk.Frame):
    title = "Resource Creator/Editor"
    def __init__(self, parent, main_app):
        super().__init__(parent, padding=10)
        self.main_app = main_app
        self.users = get_users() 
        self.resources = get_resources()
        
        ttk.Button(self, text="Create Resource", command=self.create_resource).pack(pady=5)
        ttk.Button(self, text="Edit Resource", command=self.edit_resource).pack(pady=5)
        ttk.Button(self, text="Delete Resource", command=self.delete_resource).pack(pady=5)
        
    def create_resource(self):
        while True:
            resource_name = dialog.askstring("Create Resource", "Enter resource name:")
            if resource_name not in self.resources.resources:
                description = dialog.askstring("Resource Description", "Enter resource description:")            
                is_available = msgbox.askyesno("Availability", "Is the resource available?:")
                if is_available:
                    availability = True
                else:
                    availability = False
                is_owned = msgbox.askyesno("Ownership", "Is the resource owned by someone?:")
                while True:
                    if is_owned:
                        owner_name = dialog.askstring("Owner Name", "Enter owner's username:")
                        if owner_name in self.users.users:
                            break
                        else:
                            msgbox.showerror("Error", "Owner does not exist. Please enter a valid username.")
                    else:
                        confirm = msgbox.askyesno("Ownership", "Resource will be editable by anyone. Continue?")
                        if confirm:
                            owner_name = None
                            break
                        else:
                            msgbox.showinfo("Understood", "Understood.")
            
                self.resources.resources[resource_name] = {
                    "description": description,
                    "available": availability,
                    "owner": owner_name,
                    "days_booked": [],
                }
                msgbox.showinfo("Success", f"Resource '{resource_name}' created successfully.")   
                self.resources.save_resources()
                break  
            else:
                msgbox.showerror("Error", "Resource already exists.")
            
    def edit_resource(self):
        while True:    
            resource_name = dialog.askstring("Edit Resource", "Enter resource name to edit:")
            if resource_name in self.resources.resources:
                if "owner" in self.resources.resources[resource_name] == None:
                    while True:    
                        new_resource_name = dialog.askstring("Edit Resource Name", "Enter new resource name:", initialvalue=resource_name)
                        if new_resource_name != resource_name:
                            if new_resource_name in self.resources.resources:
                                msgbox.showerror("Error", "Resource name already exists.")
                            else:
                                resource_name = new_resource_name
                                break
                    description = dialog.askstring("Resource Description", "Enter new resource description:", initialvalue=self.resources.resources[resource_name]["description"])
                    is_available = msgbox.askyesno("Availability", "Is the resource available?:")
                    if is_available:
                        availability = True
                    else:
                        availability = False
                    change_owner = msgbox.askyesno("Change Owner", "Do you want to change the owner of this resource?")
                    if change_owner:    
                        is_owned = msgbox.askyesno("Ownership", "Is the resource owned by someone?:")
                        if is_owned:
                            while True:
                                owner_name = dialog.askstring("Owner Name", "Enter owner's username:", initialvalue=owner)
                                if owner_name in self.users.users:
                                    break
                                else:
                                    msgbox.showerror("Error", "Owner does not exist. Please enter a valid username.")     
                    else:
                        owner_name = self.resources.resources[resource_name]["owner"]
                    self.resources.resources[resource_name] = {
                        "description": description,
                        "available": availability,
                        "owner": owner_name,
                    }
                    msgbox.showinfo("Success", f"Resource '{resource_name}' edited successfully.")
                    self.resources.save_resources()
                    break
                else:
                    owner = self.resources.resources[resource_name]["owner"]
                    password = dialog.askstring("Login", "Enter password to edit resource:", show='*')
                    if password == self.users.users[owner]["password"]:
                        pass
                    else:
                        msgbox.showerror("Error", "Incorrect password.")
                        break
                    while True:    
                        new_resource_name = dialog.askstring("Edit Resource Name", "Enter new resource name:", initialvalue=resource_name)
                        if new_resource_name != resource_name:
                            if new_resource_name in self.resources.resources:
                                msgbox.showerror("Error", "Resource name already exists.")
                            else:
                                resource_name = new_resource_name
                                break
                    description = dialog.askstring("Resource Description", "Enter new resource description:", initialvalue=self.resources.resources[resource_name]["description"])
                    is_available = msgbox.askyesno("Availability", "Is the resource available?:")
                    if is_available:
                        availability = True
                    else:
                        availability = False
                    change_owner = msgbox.askyesno("Change Owner", "Do you want to change the owner of this resource?")
                    if change_owner:    
                        is_owned = msgbox.askyesno("Ownership", "Is the resource owned by someone?:")
                        if is_owned:
                            while True:
                                owner_name = dialog.askstring("Owner Name", "Enter owner's username:", initialvalue=owner)
                                if owner_name in self.users.users:
                                    break
                                else:
                                    msgbox.showerror("Error", "Owner does not exist. Please enter a valid username.")     
                    else:
                        owner_name = self.resources.resources[resource_name]["owner"]
                    self.resources.resources[resource_name] = {
                        "description": description,
                        "available": availability,
                        "owner": owner_name,
                    }
                    msgbox.showinfo("Success", f"Resource '{resource_name}' edited successfully.")
                    self.resources.save_resources()
                    break
            else:
                msgbox.showerror("Error", "Resource does not exist.")
        
    def delete_resource(self):
        while True:
            resource_name = dialog.askstring("Delete Resource", "Enter resource name to delete:")
            if resource_name in self.resources.resources:
                if "owner" in self.resources.resources[resource_name] == None:
                    confirm = msgbox.askyesno("Confirm Delete", f"Are you sure you want to delete resource '{resource_name}'?")
                    if confirm:
                        del self.resources.resources[resource_name]
                        self.resources.save_resources()
                        msgbox.showinfo("Success", f"Resource '{resource_name}' deleted successfully.")
                        break
                    else:
                        msgbox.showinfo("Cancelled", "Resource deletion cancelled.")
                        break
                else:
                    owner = self.resources.resources[resource_name]["owner"]
                    password = dialog.askstring("Login", "Enter password to edit resource:", show='*')
                    if password == self.users.users[owner]["password"]:
                        pass
                    else:
                        msgbox.showerror("Error", "Incorrect password.")
                        break
                    confirm = msgbox.askyesno("Confirm Delete", f"Are you sure you want to delete resource '{resource_name}'?")
                    if confirm:
                        del self.resources.resources[resource_name]
                        self.resources.save_resources()
                        msgbox.showinfo("Success", f"Resource '{resource_name}' deleted successfully.")
                        break
                    else:
                        msgbox.showinfo("Cancelled", "Resource deletion cancelled.")
                        break
            else:
                msgbox.showerror("Error", "Resource does not exist.")
        
class BookerPage(ttk.Frame):
    title = "Booking System"
    def __init__(self, parent, main_app):
        super().__init__(parent, padding=10)
        self.main_app = main_app
        self.users = get_users()
        self.resources = get_resources()
        self.bookings = get_bookings()
        
        ttk.Button(self, text="Create Booking", command=self.create_booking).pack(pady=5)
        ttk.Button(self, text="Edit Booking", command=self.edit_booking).pack(pady=5)
        ttk.Button(self, text="Delete Booking", command=self.delete_booking).pack(pady=5)
    
    def create_booking(self):
        while True:
            booking_name = dialog.askstring("Create Booking", "Enter booking name:")
            if booking_name not in self.bookings.bookings:
                while True:
                    user_name = dialog.askstring("User Name", "Enter username for booking:")
                    if user_name in self.users.users:
                        password = dialog.askstring("Login", "Enter password to book resource:", show='*')
                        if password == self.users.users[user_name]["password"]:
                            break
                        else:
                            msgbox.showerror("Error", "Incorrect password.")
                            return
                    else:
                        msgbox.showerror("Error", "User does not exist. Please enter a valid username.")
                while True:            
                    resource_name = dialog.askstring("Resource Name", "Enter resource name to book:")
                    if resource_name in self.resources.resources:
                        if self.resources.resources[resource_name]["available"]:
                            break
                        else:
                            msgbox.showerror("Error", "Resource is not available for booking.")
                    else:
                        msgbox.showerror("Error", "Resource does not exist. Please enter a valid resource name.")
                while True:
                    booking_start_date = dialog.askstring("Booking Date", "Enter booking date (YYYY-MM-DD):")
                    try:
                        booking_start_date = datetime.datetime.strptime(booking_start_date, "%Y-%m-%d").date()
                        if booking_start_date < datetime.date.today():
                            msgbox.showerror("Error", "Booking date cannot be in the past.")
                        else:
                            booked_dates = [
                                datetime.datetime.strptime(d, "%Y-%m-%d").date()
                                if isinstance(d, str) else d
                                for d in self.resources.resources[resource_name]["days_booked"]
                            ]
                            if booking_start_date in booked_dates:
                                msgbox.showerror("Error", "Resource is already booked for this date.")
                            else:  
                                break
                    except ValueError:
                        msgbox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                while True:
                    booking_end_date = dialog.askstring("Booking Date", "Enter booking end date (YYYY-MM-DD):")
                    try:
                        booking_end_date = datetime.datetime.strptime(booking_end_date, "%Y-%m-%d").date()
                        if booking_end_date <= booking_start_date:
                            msgbox.showerror("Error", "End date must be after start date.")
                        else:
                            booked_dates = [
                                datetime.datetime.strptime(d, "%Y-%m-%d").date()
                                if isinstance(d, str) else d
                                for d in self.resources.resources[resource_name]["days_booked"]
                            ]
                            if booking_end_date in booked_dates:
                                msgbox.showerror("Error", "Resource is already booked for this date.")
                            else:
                                break
                    except ValueError:
                        msgbox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                days_booked = [(booking_start_date + datetime.timedelta(days=i)).isoformat()
                    for i in range((booking_end_date - booking_start_date).days + 1)]
                self.resources.resources[resource_name]["days_booked"].extend(days_booked)
                self.resources.save_resources()
                self.bookings.bookings[booking_name] = {
                    "user": user_name,
                    "resource": resource_name,
                    "start_date": booking_start_date.isoformat(),
                    "end_date": booking_end_date.isoformat(),
                }
                self.bookings.save_bookings()
                msgbox.showinfo("Success", f"Booking '{booking_name}' created successfully.")
                break
            else:
                msgbox.showerror("Error", "Booking does not exist.")
        
    def edit_booking(self):
        booking_name = dialog.askstring("Edit Booking", "Enter booking name to edit:")
        if booking_name:
                # Here you would add logic to edit the resource
                msgbox.showinfo("Success", f"Booking '{booking_name}' edited successfully.")
        else:
            msgbox.showerror("Error", "Booking does not exist.")
        
    def delete_booking(self):
        booking_name = dialog.askstring("Delete Booking", "Enter booking name to delete:")
        if booking_name:
            # Here you would add logic to delete the resource
            msgbox.showinfo("Success", f"Booking '{booking_name}' deleted successfully.")
        else:
            msgbox.showerror("Error", "Booking does not exist.")
        
class ViewerPage(ttk.Frame):
    title = "Resource/Booking Viewer"
    def __init__(self, parent, main_app):
        super().__init__(parent, padding=10)
        self.main_app = main_app 

        ttk.Button(self, text="View users", command=self.view_users).pack(pady=5)
    
    def view_users(self):
        user_list = "\n".join(self.main_app.pages['UserPage'].users.users.keys())
        if user_list:
            msgbox.showinfo("Users", f"Current Users:\n{user_list}")
        else:
            msgbox.showinfo("Users", "No users found.")
        
MyApp = App()
MyApp.mainloop()