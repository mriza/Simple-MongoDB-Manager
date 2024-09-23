import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from pymongo import MongoClient
import random
import string
import json
import os
import threading

CONFIG_FILE = "mongodbcreator.json"
USER_ROLES = ["read", "readWrite", "dbAdmin", "dbOwner"]

def load_servers():
    """Load the list of server connection strings from the configuration JSON file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            data = json.load(file)
            return data
    return {}

def generate_random_password(length=10):
    """Generate a random password consisting of digits and letters."""
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choice(characters) for _ in range(length))

def connect_to_mongodb(db_name, username, selected_server_url, selected_role):
    """Connect to MongoDB and create database, collection, and user on the selected server."""
    def run():
        global generated_url
        try:
            client = MongoClient(selected_server_url, serverSelectionTimeoutMS=5000)  # 5 seconds timeout
            
            # Create a database and a test collection
            db = client[db_name]
            test_collection = db['test_collection']
            test_collection.insert_one({"test_field": "test_value"})

            # Generate a random password for the user
            password = generate_random_password()

            # Create a user for the database with the selected role
            db.command("createUser", username, pwd=password, roles=[selected_role])

            # Generate the connection string for the new user
            generated_url = f"mongodb://{username}:{password}@{selected_server_url.split('@')[-1].rstrip('/')}/{db_name}"

            # Update UI in the main thread
            result_text.config(state=NORMAL)
            result_text.delete(1.0, 'end')  # Clear previous results
            result_text.insert('end', generated_url)
            result_text.config(state=DISABLED)

            # Enable the copy button after successful creation
            copy_button.config(state=NORMAL)

            messagebox.showinfo("Success", f"Database '{db_name}' and user '{username}' created successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to MongoDB: {str(e)}")
            generated_url = None

    thread = threading.Thread(target=run)
    thread.start()

def on_submit():
    """Handle submit button click."""
    db_name = db_name_entry.get()
    username = username_entry.get()
    selected_server_name = server_var.get()
    selected_role = role_var.get()

    if not db_name or not username:
        messagebox.showwarning("Input Error", "Both database name and username are required!")
        return

    if not selected_server_name:
        messagebox.showwarning("Selection Error", "Please select a server!")
        return

    if not selected_role:
        messagebox.showwarning("Selection Error", "Please select a user role!")
        return

    # Retrieve the actual connection URL based on the selected server name
    selected_server_url = servers[selected_server_name]['url']
    connect_to_mongodb(db_name, username, selected_server_url, selected_role)

def copy_to_clipboard():
    """Copy the generated connection URL to the clipboard."""
    if generated_url:
        root.clipboard_clear()
        root.clipboard_append(generated_url)
        messagebox.showinfo("Copied", "Connection URL copied to clipboard!")
    else:
        messagebox.showerror("Error", "No URL available to copy.")

def populate_dropdowns():
    """Populate the dropdowns with available servers and roles."""
    # Server dropdown
    server_menu['menu'].delete(0, 'end')  # Clear previous entries
    for name in servers.keys():
        server_menu['menu'].add_command(label=name, command=lambda value=name: server_var.set(value))

    # User role dropdown
    role_menu['menu'].delete(0, 'end')  # Clear previous entries
    for role in USER_ROLES:
        role_menu['menu'].add_command(label=role, command=lambda value=role: role_var.set(value))

# Load the list of server connections
servers = load_servers()

# Create the main window using ttkbootstrap
root = ttk.Window(themename="superhero")  # Default theme
root.title("MongoDB Manager")

generated_url = None

# Set a common width for entries and text field
entry_width = 30

# Theme selection dropdown
ttk.Label(root, text="Select Theme").grid(row=0, column=0, padx=10, pady=10, sticky=E)
theme_var = ttk.StringVar(root, "superhero")  # Default theme
theme_menu = ttk.OptionMenu(root, theme_var, "superhero", "flatly", "darkly", "cyborg", "lumen", "solar",
                             command=lambda value: ttk.Style().theme_use(value))
theme_menu.grid(row=0, column=1, padx=10, pady=10, sticky=W)

# Database name input
ttk.Label(root, text="Database Name").grid(row=1, column=0, padx=10, pady=10, sticky=E)
db_name_entry = ttk.Entry(root, width=entry_width)
db_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)

# Username input
ttk.Label(root, text="Username").grid(row=2, column=0, padx=10, pady=10, sticky=E)
username_entry = ttk.Entry(root, width=entry_width)
username_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)

# Server selection dropdown
ttk.Label(root, text="Select MongoDB Server").grid(row=3, column=0, padx=10, pady=10, sticky=E)
server_var = ttk.StringVar(root)
server_menu = ttk.OptionMenu(root, server_var, *servers.keys())
server_menu.grid(row=3, column=1, padx=10, pady=10, sticky=W)

# User role selection dropdown
ttk.Label(root, text="Select User Role").grid(row=4, column=0, padx=10, pady=10, sticky=E)
role_var = ttk.StringVar(root)
role_menu = ttk.OptionMenu(root, role_var, *USER_ROLES)
role_menu.grid(row=4, column=1, padx=10, pady=10, sticky=W)

# Submit button with capsule style
submit_button = ttk.Button(root, text="Create Database & User", command=on_submit, bootstyle=(SUCCESS, OUTLINE))
submit_button.grid(row=5, columnspan=2, pady=10)

# Copyable Text Box for connection URL
ttk.Label(root, text="Generated Connection URL").grid(row=6, column=0, padx=10, pady=10, sticky=E)
result_text = ttk.Text(root, width=entry_width + 10, height=2, state=DISABLED)
result_text.grid(row=6, column=1, padx=(10, 0), pady=10, sticky="ew")

# Copy URL button placed next to the Text field without space and capsule style
copy_button = ttk.Button(root, text="Copy", command=copy_to_clipboard, state=DISABLED, bootstyle=(INFO, OUTLINE))
copy_button.grid(row=6, column=2, padx=(0, 10), pady=10, sticky="w")

# Populate dropdowns with servers and roles
populate_dropdowns()

# Start the main loop
root.mainloop()
