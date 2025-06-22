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
        #Generates pages for the notebook
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
        self.resources = get_resources()
        self.bookings = get_bookings()

        ttk.Button(self, text="Create New User", command=self.create_user).pack(pady=5)
        ttk.Button(self, text="Edit User Profile", command=self.edit_user).pack(pady=5)
        ttk.Button(self, text="Delete User", command=self.delete_user).pack(pady=5)

    def create_user(self):
        self.users.load_users()
        self.resources.load_resources()
        self.bookings.load_bookings()
        while True:
            username = dialog.askstring("Create New User", "Enter Username:")
            if username == None:
                msgbox.showinfo("Cancelled", "User creation cancelled.")
                return
            elif username == "":
                msgbox.showerror("Error", "Username cannot be empty.")
            elif username not in self.users.users:
                break
            else:
                msgbox.showerror("Error", "User already exists.")
        while True:
            full_name = dialog.askstring("Full Name", "Enter Full Name (Optional):")
            if full_name == None:
                    msgbox.showinfo("Cancelled", "User creation cancelled.")
                    return
            else:
                break
        while True:
            password = dialog.askstring("Password", "Enter Password:", show='*')
            if password == None:
                msgbox.showinfo("Cancelled", "User creation cancelled.")
                return
            elif password == "":
                msgbox.showerror("Error", "Password cannot be empty.")
            else:
              break  
        self.users.users[username] = {"full_name": full_name, "password": password}
        self.users.save_users()
        msgbox.showinfo("Success", f"New user '{username}' created successfully.")

    def edit_user(self): 
        self.users.load_users()
        self.resources.load_resources()
        self.bookings.load_bookings()
        while True:    
            user_name = dialog.askstring("Edit User", "Enter username to be edited:")
            if user_name == None:
                msgbox.showinfo("Cancelled", "User edit cancelled.")
                return
            elif user_name == "":
                msgbox.showerror("Error", "Username cannot be empty.")
            elif user_name in self.users.users:
                while True:
                    password = dialog.askstring("Login", "Enter password to edit user:", show='*')
                    if password == None:
                        msgbox.showinfo("Cancelled", "User edit cancelled.")
                        return
                    elif password == "":
                        msgbox.showerror("Error", "Password cannot be empty.")
                    elif password == self.users.users[user_name]["password"]:
                        while True:
                            new_username = dialog.askstring("Edit Username", "Enter new username:", initialvalue=user_name)
                            if new_username == None:
                                msgbox.showinfo("Cancelled", "User edit cancelled.")
                                return
                            elif new_username == "":
                                msgbox.showerror("Error", "Username cannot be empty.")
                            elif new_username != user_name:
                                if new_username in self.users.users:
                                    msgbox.showerror("Error", "New username already exists.")
                                else:
                                    break
                            else:
                                break
                        self.users.users[new_username] = self.users.users.pop(user_name)
                        old_user_name = user_name
                        user_name = new_username  
                        while True:
                            full_name = dialog.askstring("Edit Full Name", "Enter new full name:", initialvalue=self.users.users[user_name]["full_name"])
                            if full_name == None:
                                msgbox.showinfo("Cancelled", "User edit cancelled.")
                                return
                            elif full_name == "":
                                msgbox.showerror("Error", "Full name cannot be empty.")
                            else:
                                break
                        while True:
                            new_password = dialog.askstring("Edit Password", "Enter new password (leave blank to keep current):", show='*')
                            if new_password == None:
                                msgbox.showinfo("Cancelled", "User edit cancelled.")
                                return
                            elif new_password == "":
                                new_password = self.users.users[user_name]["password"]
                                break
                            else:
                                break
                        if full_name:
                            self.users.users[user_name]["full_name"] = full_name
                        if new_password:
                            self.users.users[user_name]["password"] = new_password
                        # Update bookings and resources with new username
                        for booking_name, booking in self.bookings.bookings.items():
                            if booking["owner"] == user_name:
                                self.bookings.bookings[booking_name]["owner"] = user_name
                        for resource in self.resources.resources.values():
                            if resource.get("owner") == old_user_name:
                                resource["owner"] = user_name 
                        self.users.save_users()
                        msgbox.showinfo("Success", f"User '{user_name}' updated successfully.")
                        return
                    else:
                        msgbox.showerror("Error", "Incorrect password.")
                        return
            else:
                msgbox.showerror("Error", "User does not exist.")

   def delete_user(self):
        self.users.load_users()
        self.resources.load_resources()
        self.bookings.load_bookings()
        while True:
            username = dialog.askstring("Delete User", "Enter username to be deleted:")
            if username == None:
                msgbox.showinfo("Cancelled", "User deletion cancelled.")
                return
            elif username == "":
                msgbox.showerror("Error", "Username cannot be empty.")
            elif username in self.users.users:
                while True:
                    password = dialog.askstring("Login", "Enter password to delete user:", show='*')
                    if password == None:
                        msgbox.showinfo("Cancelled", "User deletion cancelled.")
                        return
                    elif password == "":
                        msgbox.showerror("Error", "Password cannot be empty.")
                    elif password == self.users.users[username]["password"]:
                        confirm = msgbox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?")
                        if confirm:
                            del self.users.users[username]
                            self.users.save_users()
                            msgbox.showinfo("Success", f"User '{username}' deleted successfully.")
                            #Tranfer out user's resources
                            for resource in self.resources.resources.values():
                                if resource.get("owner") == username:
                                    replace_resource = dialog.askyesno("Resource Ownership", f"User '{username}' owns resource '{resource}'. Do you want to transfer ownership to another user?")
                                    if replace_resource:
                                        new_owner = dialog.askstring("New Owner", "Enter new owner's username:")
                                        if new_owner in self.users.users:
                                            resource["owner"] = new_owner
                                            self.resources.save_resources()
                                            msgbox.showinfo("Success", f"Resource ownership transferred to '{new_owner}'.")
                                        else:
                                            msgbox.showerror("Error", "New owner does not exist.")
                                    else:
                                        resource["owner"] = None
                                        self.resources.save_resources()
                            #Removes user's bookings and updates resources
                            for booking in list(self.bookings.bookings.values()):
                                booking_name = self.bookings.bookings[booking]
                                if booking["owner"] == username:
                                    resource_name = self.bookings.bookings[booking_name]["resource"]
                                    start_date = datetime.datetime.strptime(self.bookings.bookings[booking_name]["start_date"], "%Y-%m-%d").date()
                                end_date = datetime.datetime.strptime(self.bookings.bookings[booking_name]["end_date"], "%Y-%m-%d").date()
                                days_booked = [(start_date + datetime.timedelta(days=i)).isoformat()
                                    for i in range((end_date - start_date).days + 1)]
                                self.resources.resources[resource_name]["days_booked"] = [
                                    d for d in self.resources.resources[resource_name]["days_booked"]
                                    if d not in days_booked
                                ]
                                self.resources.save_resources()
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
        self.bookings = get_bookings()

        ttk.Button(self, text="Create Resource", command=self.create_resource).pack(pady=5)
        ttk.Button(self, text="Edit Resource", command=self.edit_resource).pack(pady=5)
        ttk.Button(self, text="Delete Resource", command=self.delete_resource).pack(pady=5)

    def create_resource(self):
        self.users.load_users()
        self.resources.load_resources()
        self.bookings.load_bookings()
        while True:
            resource_name = dialog.askstring("Create Resource", "Enter resource name:")
            if resource_name == None:
                msgbox.showinfo("Cancelled", "Resource creation cancelled.")
                return
            elif resource_name == "":
                msgbox.showerror("Error", "Resource name cannot be empty.")
            elif resource_name not in self.resources.resources:
                while True:
                    description = dialog.askstring("Resource Description", "Enter resource description (Optional):") 
                    if description == None:
                        msgbox.showinfo("Cancelled", "Resource creation cancelled.")
                        return
                    else:
                        break
                is_available = msgbox.askyesno("Availability", "Is the resource available?:")
                if is_available:
                    availability = True
                else:
                    availability = False
                is_owned = msgbox.askyesno("Ownership", "Is the resource owned by someone?:")
                while True:
                    if is_owned:
                        owner_name = dialog.askstring("Owner Name", "Enter owner's username:")
                        if owner_name == None:
                            msgbox.showinfo("Cancelled", "Resource creation cancelled.")
                            return
                        elif owner_name == "":
                            msgbox.showerror("Error", "Owner name cannot be empty.")
                        elif owner_name in self.users.users:
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
        self.users.load_users()
        self.resources.load_resources()
        self.bookings.load_bookings()
        while True:
            resource_name = dialog.askstring("Edit Resource", "Enter resource name to edit:")
            if resource_name == None:
                msgbox.showinfo("Cancelled", "Resource edit cancelled.")
                return
            elif resource_name == "":
                msgbox.showerror("Error", "Resource name cannot be empty.")
            elif resource_name in self.resources.resources:
                if "owner" in self.resources.resources[resource_name] == None:
                    while True:
                        new_resource_name = dialog.askstring("Edit Resource Name", "Enter new resource name:", initialvalue=resource_name)
                        if new_resource_name == None:
                            msgbox.showinfo("Cancelled", "Resource edit cancelled.")
                            return
                        elif new_resource_name == "":
                            msgbox.showerror("Error", "Resource name cannot be empty.")
                        elif new_resource_name != resource_name:
                            if new_resource_name in self.resources.resources:
                                msgbox.showerror("Error", "Resource name already exists.")
                            else:
                                old_resource_name = resource_name
                                resource_name = new_resource_name
                                break
                    while True:
                        description = dialog.askstring("Resource Description", "Enter new resource description:", initialvalue=self.resources.resources[resource_name]["description"])
                        if description == None:
                            msgbox.showinfo("Cancelled", "Resource edit cancelled.")
                            return
                        else:
                            break
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
                                if owner_name == None:
                                    msgbox.showinfo("Cancelled", "Resource edit cancelled.")
                                    return
                                elif owner_name == "":
                                    msgbox.showerror("Error", "Owner name cannot be empty.")
                                elif owner_name in self.users.users:
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
                    #Update bookings with new resource name
                    for booking_name, booking in list(self.bookings.bookings.items()):
                        if booking["resource"] == old_resource_name:
                            self.bookings.bookings[booking_name]["resource"] = resource_name
                    msgbox.showinfo("Success", f"Resource '{resource_name}' edited successfully.")
                    self.resources.save_resources()
                    break
                else:
                    owner = self.resources.resources[resource_name]["owner"]
                    while True:
                        password = dialog.askstring("Login", "Enter password to edit resource:", show='*')
                        if password == None:
                            msgbox.showinfo("Cancelled", "Resource edit cancelled.")
                            return
                        elif password == "":
                            msgbox.showerror("Error", "Password cannot be empty.")
                        elif password == self.users.users[owner]["password"]:
                            break
                        else:
                            msgbox.showerror("Error", "Incorrect password.")
                            return
                    while True:    
                        new_resource_name = dialog.askstring("Edit Resource Name", "Enter new resource name:", initialvalue=resource_name)
                        if new_resource_name == None:
                            msgbox.showinfo("Cancelled", "Resource edit cancelled.")
                            return
                        elif new_resource_name == "":
                            msgbox.showerror("Error", "Resource name cannot be empty.")
                        elif new_resource_name != resource_name:
                            if new_resource_name in self.resources.resources:
                                msgbox.showerror("Error", "Resource name already exists.")
                            else:
                                old_resource_name = resource_name
                                resource_name = new_resource_name
                                break
                        else:
                            old_resource_name = resource_name
                            break
                    while True:
                        description = dialog.askstring("Resource Description", "Enter new resource description:", initialvalue=self.resources.resources[resource_name]["description"])
                        if description == None:
                            msgbox.showinfo("Cancelled", "Resource edit cancelled.")
                            return
                        else:
                            break
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
                                if owner_name == None:
                                    msgbox.showinfo("Cancelled", "Resource edit cancelled.")
                                    return
                                elif owner_name == "":
                                    msgbox.showerror("Error", "Owner name cannot be empty.")
                                elif owner_name in self.users.users:
                                    break
                                else:
                                    msgbox.showerror("Error", "Owner does not exist. Please enter a valid username.")
                    else:
                        owner_name = self.resources.resources[resource_name]["owner"]
                    self.resources.resources[resource_name] = {
                        "description": description,
                        "available": availability,
                        "owner": owner_name,
                        "days_booked": self.resources.resources[resource_name].get("days_booked", []),
                    }
                    #Update bookings again
                    for booking_name, booking in list(self.bookings.bookings.items()):
                        if booking["resource"] == old_resource_name:
                            self.bookings.bookings[booking_name]["resource"] = resource_name
                    msgbox.showinfo("Success", f"Resource '{resource_name}' edited successfully.")
                    self.resources.save_resources()
                    break
            else:
                msgbox.showerror("Error", "Resource does not exist.")

    def delete_resource(self):
        self.users.load_users()
        self.resources.load_resources()
        self.bookings.load_bookings()
        while True:
            resource_name = dialog.askstring("Delete Resource", "Enter resource name to delete:")
            if resource_name == None:
                msgbox.showinfo("Cancelled", "Resource deletion cancelled.")
                return
            elif resource_name == "":
                msgbox.showerror("Error", "Resource name cannot be empty.")
            elif resource_name in self.resources.resources:
                if "owner" in self.resources.resources[resource_name] == None:
                    confirm = msgbox.askyesno("Confirm Delete", f"Are you sure you want to delete resource '{resource_name}'?")
                    if confirm:
                        del self.resources.resources[resource_name]
                        self.resources.save_resources()
                        #Remove resource from bookings
                        for booking_name, booking in list(self.bookings.bookings.items()):
                            if booking["resource"] == resource_name:
                                del self.bookings.bookings[booking_name]
                        self.bookings.save_bookings()
                        msgbox.showinfo("Success", f"Resource '{resource_name}' deleted successfully.")
                        break
                    else:
                        msgbox.showinfo("Cancelled", "Resource deletion cancelled.")
                        break
                else:
                    owner = self.resources.resources[resource_name]["owner"]
                    while True:
                        password = dialog.askstring("Login", "Enter password to edit resource:", show='*')
                        if password == None:
                            msgbox.showinfo("Cancelled", "Resource deletion cancelled.")
                            return
                        elif password == "":
                            msgbox.showerror("Error", "Password cannot be empty.")
                        elif password == self.users.users[owner]["password"]:
                            break
                        else:
                            msgbox.showerror("Error", "Incorrect password.")
                            return
                    confirm = msgbox.askyesno("Confirm Delete", f"Are you sure you want to delete resource '{resource_name}'?")
                    if confirm:
                        del self.resources.resources[resource_name]
                        self.resources.save_resources()
                        #Remove resource from bookings again
                        for booking_name, booking in list(self.bookings.bookings.items()):
                            if booking["resource"] == resource_name:
                                del self.bookings.bookings[booking_name]
                        self.bookings.save_bookings()
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
        self.users.load_users()
        self.resources.load_resources()
        self.bookings.load_bookings()
        while True:
            booking_name = dialog.askstring("Create Booking", "Enter booking name:")
            if booking_name == None:
                msgbox.showinfo("Cancelled", "Booking creation cancelled.")
                return
            elif booking_name == "":
                msgbox.showerror("Error", "Booking name cannot be empty.")
            elif booking_name not in self.bookings.bookings:
                while True:
                    username = dialog.askstring("User Name", "Enter username for booking:")
                    if username == None:
                        msgbox.showinfo("Cancelled", "Booking creation cancelled.")
                        return
                    elif username == "":
                        msgbox.showerror("Error", "Username cannot be empty.")
                    elif username in self.users.users:
                        while True:
                            password = dialog.askstring("Login", "Enter password to book resource:", show='*')
                            if password == None:
                                msgbox.showinfo("Cancelled", "Booking creation cancelled.")
                                return
                            elif password == "":
                                msgbox.showerror("Error", "Password cannot be empty.")
                            elif password == self.users.users[username]["password"]:
                                break
                            else:
                                msgbox.showerror("Error", "Incorrect password.")
                                return
                        break
                    else:
                        msgbox.showerror("Error", "User does not exist. Please enter a valid username.")
                while True:
                    resource_name = dialog.askstring("Resource Name", "Enter resource name to book:")
                    if resource_name == None:
                        msgbox.showinfo("Cancelled", "Booking creation cancelled.")
                        return
                    elif resource_name == "":
                        msgbox.showerror("Error", "Resource name cannot be empty.")
                    elif resource_name in self.resources.resources:
                        if self.resources.resources[resource_name]["available"]:
                            break
                        else:
                            msgbox.showerror("Error", "Resource is not available for booking.")
                    else:
                        msgbox.showerror("Error", "Resource does not exist. Please enter a valid resource name.")
                while True:
                    booking_start_date = dialog.askstring("Booking Date", "Enter booking date (YYYY-MM-DD):")
                    if booking_start_date == None:
                        msgbox.showinfo("Cancelled", "Booking creation cancelled.")
                        return
                    elif booking_start_date == "":
                        msgbox.showerror("Error", "Booking date cannot be empty.")
                    else:
                        try:
                            booking_start_date = datetime.datetime.strptime(booking_start_date, "%Y-%m-%d").date()
                            if booking_start_date < datetime.date.today():
                                msgbox.showerror("Error", "Booking date cannot be in the past.")
                            else:
                                #Check if resource is already booked for date
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
                    if booking_end_date == None:
                        msgbox.showinfo("Cancelled", "Booking creation cancelled.")
                        return
                    elif booking_end_date == "":
                        msgbox.showerror("Error", "Booking end date cannot be empty.")
                    else:
                        try:
                            booking_end_date = datetime.datetime.strptime(booking_end_date, "%Y-%m-%d").date()
                            if booking_end_date <= booking_start_date:
                                msgbox.showerror("Error", "End date must be after start date.")
                            else:
                                #Check if resource is already booked for date again
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
                #Create booking and update resource availability
                days_booked = [(booking_start_date + datetime.timedelta(days=i)).isoformat()
                    for i in range((booking_end_date - booking_start_date).days + 1)]
                self.resources.resources[resource_name]["days_booked"].extend(days_booked)
                self.resources.save_resources()
                self.bookings.bookings[booking_name] = {
                    "owner": username,
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
        self.users.load_users()
        self.resources.load_resources()
        self.bookings.load_bookings()
        while True:
            booking_name = dialog.askstring("Edit Booking", "Enter booking name to edit:")
            if booking_name == None:
                msgbox.showinfo("Cancelled", "Booking edit cancelled.")
                return
            elif booking_name == "":
                msgbox.showerror("Error", "Booking name cannot be empty.")
            elif booking_name in self.bookings.bookings:
                username = self.bookings.bookings[booking_name]["owner"]
                while True:
                    password = dialog.askstring("Login", "Enter password to edit booking:", show='*')
                    if password == None:
                        msgbox.showinfo("Cancelled", "Booking edit cancelled.")
                        return
                    elif password == "":
                        msgbox.showerror("Error", "Password cannot be empty.")
                    elif password == self.users.users[username]["password"]:
                        while True:
                            new_booking_name = dialog.askstring("Edit Booking Name", "Enter new booking name:", initialvalue=booking_name)
                            if new_booking_name == None:
                                msgbox.showinfo("Cancelled", "Booking edit cancelled.")
                                return
                            elif new_booking_name == "":
                                msgbox.showerror("Error", "Booking name cannot be empty.")
                            elif new_booking_name != booking_name:
                                if new_booking_name in self.bookings.bookings:
                                    msgbox.showerror("Error", "Booking name already exists.")
                                else:
                                    booking_name = new_booking_name
                                    break
                            else:
                                break
                        resource_name = self.bookings.bookings[booking_name]["resource"]
                        while True:
                            new_resource_name = dialog.askstring("Resource Name", "Enter new resource name:", initialvalue=resource_name)
                            if new_resource_name in self.resources.resources:
                                if self.resources.resources[new_resource_name]["available"]:
                                    resource_name = new_resource_name
                                    break
                                else:
                                    msgbox.showerror("Error", "Resource is not available for booking.")
                            else:
                                msgbox.showerror("Error", "Resource does not exist. Please enter a valid resource name.")
                        while True:
                            booking_start_date = dialog.askstring("Booking Date", "Enter new booking start date (YYYY-MM-DD):")
                            if booking_start_date == None:
                                msgbox.showinfo("Cancelled", "Booking edit cancelled.")
                                return
                            elif booking_start_date == "":
                                msgbox.showerror("Error", "Booking start date cannot be empty.")
                            else:
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
                            booking_end_date = dialog.askstring("Booking Date", "Enter new booking end date (YYYY-MM-DD):")
                            if booking_end_date == None:
                                msgbox.showinfo("Cancelled", "Booking edit cancelled.")
                                return
                            elif booking_end_date == "":
                                msgbox.showerror("Error", "Booking end date cannot be empty.")
                            else:
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
                        self.resources.resources[resource_name]["days_booked"] = [
                            d for d in self.resources.resources[resource_name]["days_booked"]
                            if d not in days_booked
                        ]
                        self.resources.resources[resource_name]["days_booked"].extend(days_booked)
                        self.resources.save_resources() 
                        self.bookings.bookings[booking_name] = {
                            "owner": username,
                            "resource": resource_name,
                            "start_date": booking_start_date.isoformat(),
                            "end_date": booking_end_date.isoformat(),
                        }
                        self.bookings.save_bookings()
                        msgbox.showinfo("Success", f"Booking '{booking_name}' edited successfully.")
                        break
                    else:
                        msgbox.showerror("Error", "Incorrect password.")
                        break
            else:
                msgbox.showerror("Error", "Booking does not exist.")
                  
    def delete_booking(self):
        self.users.load_users()
        self.resources.load_resources()
        self.bookings.load_bookings()
        while True:
            booking_name = dialog.askstring("Delete Booking", "Enter booking name to delete:")
            if booking_name == None:
                msgbox.showinfo("Cancelled", "Booking deletion cancelled.")
                return
            elif booking_name == "":
                msgbox.showerror("Error", "Booking name cannot be empty.")    
            elif booking_name in self.bookings.bookings:
                username = self.bookings.bookings[booking_name]["owner"]
                while True:    
                    password = dialog.askstring("Login", "Enter password to delete booking:", show='*')
                    if password == None:
                        msgbox.showinfo("Cancelled", "Booking deletion cancelled.")
                        return
                    elif password == "":
                        msgbox.showerror("Error", "Password cannot be empty.")
                    elif password == self.users.users[username]["password"]:
                        confirm = msgbox.askyesno("Confirm Delete", f"Are you sure you want to delete booking '{booking_name}'?")
                        if confirm:
                            resource_name = self.bookings.bookings[booking_name]["resource"]
                            start_date = datetime.datetime.strptime(self.bookings.bookings[booking_name]["start_date"], "%Y-%m-%d").date()
                            end_date = datetime.datetime.strptime(self.bookings.bookings[booking_name]["end_date"], "%Y-%m-%d").date()
                            days_booked = [(start_date + datetime.timedelta(days=i)).isoformat()
                                for i in range((end_date - start_date).days + 1)]
                            self.resources.resources[resource_name]["days_booked"] = [
                                d for d in self.resources.resources[resource_name]["days_booked"]
                                if d not in days_booked
                            ]
                            self.resources.save_resources()
                            del self.bookings.bookings[booking_name]
                            self.bookings.save_bookings()
                            msgbox.showinfo("Success", f"Booking '{booking_name}' deleted successfully.")
                            break
                        else:
                            msgbox.showinfo("Cancelled", "Booking deletion cancelled.")
                            break
                    else:
                        msgbox.showerror("Error", "Incorrect password.")
                        break
                break
            else:
                msgbox.showerror("Error", "Booking does not exist.")
        
        
class ViewerPage(ttk.Frame):
    title = "Item Viewer"
    def __init__(self, parent, main_app):
        super().__init__(parent, padding=10)
        self.main_app = main_app 
        self.users = get_users()
        self.resources = get_resources()
        self.bookings = get_bookings()
        
        ttk.Button(self, text="View users", command=self.view_users).pack(pady=5)
        ttk.Button(self, text="View resources", command=self.view_resources).pack(pady=5)
        ttk.Button(self, text="View bookings", command=self.view_resources).pack(pady=5)
    
    def view_users(self):
        self.users.load_users()
        user_list = "\n".join(self.main_app.pages['UserPage'].users.users.keys())
        if user_list:
            msgbox.showinfo("Users", f"Current Users:\n{user_list}")
        else:
            msgbox.showinfo("Users", "No users found.")
    
    def view_resources(self):
        self.resources.load_resources()
        resource_list = "\n".join(self.main_app.pages['ResourcePage'].resources.resources.keys())
        if resource_list:
            msgbox.showinfo("Resources", f"Current Resources:\n{resource_list}")
        else:
            msgbox.showinfo("Resources", "No resources found.")
    
    def view_bookings(self):
        self.bookings.load_bookings()
        booking_list = "\n".join(self.main_app.pages['BookerPage'].bookings.bookings.keys())
        if booking_list:
            msgbox.showinfo("Bookings", f"Current Bookings:\n{booking_list}")
        else:
            msgbox.showinfo("Bookings", "No bookings found.")
        
if __name__ == "__main__":
    MyApp = App()
    MyApp.mainloop()