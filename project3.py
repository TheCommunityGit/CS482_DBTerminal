from simple_term_menu import TerminalMenu
from rich.table import Table
from rich.console import Console
import mysql.connector as sql
import sys
import getpass

# Global variable for storing digital display data
digital_displays = None
dbCursor = None
mydb = None  # Global variable for the database connection

# Connect to the MySQL database as required in project description
def connectToDb(hostin, name, username, password):
    global dbCursor, mydb  # Declare as global so they are accessible outside this function
    if hostin == "localhost":
        hostin = "127.0.0.1"

    try:
        # Connect to the database
        mydb = sql.connect(
            host=hostin,
            port=3306,
            user=username,
            password=password,
            database=name
        )

        # Create a cursor object
        dbCursor = mydb.cursor()

        # Check if dbCursor is created successfully
        if dbCursor is not None:
            return True
        else:
            return False
    except sql.Error as e:
        print(f"Error connecting to the database: {e}")
        return False

# Fetch all digital displays from the database
def queryAllDigitalDisplays():
    global digital_displays
    query = "SELECT * FROM digitaldisplay"

    # Executing the query
    dbCursor.execute(query)

    # Fetching all the results
    results = dbCursor.fetchall()

    # Convert results into a list of dictionaries for easier access
    digital_displays = [
        {"serial_no": row[0], "scheduler_system": row[1], "model_no": row[2]}
        for row in results
    ]


def queryMoreInfo(modelNumber):
    # Updated query to fetch all fields from the 'model' table
    query = "SELECT * FROM model WHERE modelNo = %s"

    dbCursor.execute(query, (modelNumber,))

    # Fetching the result
    info = dbCursor.fetchall()

    if info:
        # Create a table to display the fetched information
        console = Console()
        table = Table(title=f"Details for Model No: {modelNumber}")

        # Add table columns based on the schema
        table.add_column("Model No", justify="left")
        table.add_column("Width", justify="right")
        table.add_column("Height", justify="right")
        table.add_column("Weight", justify="right")
        table.add_column("Depth", justify="right")
        table.add_column("Screen Size", justify="right")

        # Populate the table with the result
        for row in info:
            table.add_row(
                row[0],  # Model No
                str(row[1]),  # Width
                str(row[2]),  # Height
                str(row[3]),  # Weight
                str(row[4]),  # Depth
                str(row[5])   # Screen Size
            )

        # Return the formatted table
        return table
    else:
        return None




# Function to prompt for database login
def login():
    while True:  # Loop until the user confirms login or resets the form
        print("\n--- Database Login ---")

        # Collect input from the user
        db_host = input("Enter database host: ")
        db_name = input("Enter database name: ")
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")

        clear_terminal()
        # Ask the user to confirm or reset the form
        action = input("\nYou have entered the following details:\n"
                        f"Host: {db_host}\n"
                        f"Database: {db_name}\n"
                        f"Username: {username}\n"
                        "Press 'l' to confirm and log in, or 'r' to reset the form: ").lower()

        if action == 'l':
            # After confirmation, attempt to connect to the database
            print(f"\nAttempting to connect to the database '{db_name}' at '{db_host}' with user '{username}'...")

            connected = connectToDb(db_host, db_name, username, password)

            if connected:
                print("Connection successful!\n")
                return
                break  # Exit the loop after a successful login
            else:
                clear_terminal()
                print("Connection failed. Please check your credentials and try again.\n")
                continue

        elif action == 'r':
            clear_terminal()
            print("\nForm reset. Please enter the details again.")
            continue  # Restart the form collection process
        else:
            print("Invalid input. Please press 'l' to log in or 'r' to reset the form.")


# Function to display all digital displays
def display_all():
    console = Console()
    table = Table(title="Digital Displays")

    # Add table columns (only relevant columns from the schema)
    table.add_column("Model No", justify="left")

    queryAllDigitalDisplays()
    # Populate the table with data
    for display in digital_displays:
        table.add_row(
            display["model_no"]
        )

    # Print the table
    console.print(table)

    while True:  # Keep the user in the display menu until they choose "Return to Main Menu"
        # Create a list of options for the TerminalMenu
        options = [
            f"{display['model_no']}"
            for display in digital_displays
        ]
        options.append("Return to Main Menu")

        # Create and display the menu
        terminal_menu = TerminalMenu(options, title="\nSelect a display to view more information:")
        choice = terminal_menu.show()

        if choice is not None and choice < len(digital_displays):
            selected_display = digital_displays[choice]
            model_number = selected_display["model_no"]

            # Fetch more information using the model number
            model_table = queryMoreInfo(model_number)

            if model_table:
                # Display the model information as a table
                console.print(model_table)
            else:
                print(f"\nNo information found for Model No: {model_number}")
        elif choice == len(digital_displays):  # User chooses "Return to Main Menu"
            print("\nReturning to the main menu...")
            break  # Exit the loop and return to the main menu


# Main menu options
options = [
    "1. Display all digital displays",
    "2. Search for digital displays",
    "3. Insert a new digital display",
    "4. Delete a digital display",
    "5. Update a digital display",
    "6. reset connection",
    "7. Logout"
]

def search_display():
    global dbCursor  # Use the global database cursor

    # Fetch available scheduler systems from the database
    scheduler_List = []
    query_scheduler = "SELECT DISTINCT schedulerSystem FROM DigitalDisplay"
    dbCursor.execute(query_scheduler)
    scheduler_List = [row[0] for row in dbCursor.fetchall()]

    # Get input for the scheduler system
    scheduler_system = input("Enter a Scheduler System: ")

    # Check if the scheduler system exists
    if scheduler_system not in scheduler_List:
        print("\nInvalid Scheduler System. Exiting...\n")
        return

    print(f"\nSearching for digital displays by scheduler system: {scheduler_system}...\n")

    # Prepare to display results in a table
    console = Console()
    table = Table(title=f"DDs for SS: {scheduler_system}")

    # Add table columns
    table.add_column("Model No", justify="left")

    # Query for digital displays with the given scheduler system
    query_display = "SELECT modelNo FROM DigitalDisplay WHERE schedulerSystem = %s"
    dbCursor.execute(query_display, (scheduler_system,))

    # Store results for menu and populate the table
    displays = [{"model_no": row[0]} for row in dbCursor.fetchall()]
    for display in displays:
        table.add_row(display["model_no"])

    # Print the table
    console.print(table)

    if not displays:
        print("\nNo digital displays found for the selected scheduler system.\n")
        return

    while True:
        # Create a menu for selecting a display or returning to the main menu
        options = [f"{display['model_no']}" for display in displays]
        options.append("Return to Main Menu")

        # Show menu and get user choice
        terminal_menu = TerminalMenu(options, title="\nSelect a display to view more information:")
        choice = terminal_menu.show()

        if choice is not None and choice < len(displays):
            # Fetch and display more information for the selected display
            selected_display = displays[choice]
            model_number = selected_display["model_no"]

            # Use the queryMoreInfo function to get additional details
            model_table = queryMoreInfo(model_number)

            if model_table:
                console.print(model_table)
            else:
                print(f"\nNo additional information found for Model No: {model_number}")
        elif choice == len(displays):  # User chooses "Return to Main Menu"
            print("\nReturning to the main menu...")
            break

def insert_display():
    print("\nInserting a new digital display...\n")
    input("Press Enter to return to the main menu.")

def delete_display():
    print("\nDeleting a digital display...\n")
    input("Press Enter to return to the main menu.")

def update_display():
    print("\nUpdating a digital display...\n")
    input("Press Enter to return to the main menu.")

def logout():
    print("\nLogging out...\n")
    clear_terminal()
    exit()


import os

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS or Linux
    else:
        os.system('clear')

# Main program loop
def main():
    login()  # Prompt for login before showing the menu
    while True:
        terminal_menu = TerminalMenu(options, title="\nDigital Display Management System\nSelect an option:")
        choice = terminal_menu.show()

        if choice == 0:
            display_all()
        elif choice == 1:
            search_display()
        elif choice == 2:
            insert_display()
        elif choice == 3:
            delete_display()
        elif choice == 4:
            update_display()
        elif choice == 5:
            clear_terminal()
            login()
        elif choice == 6:
            logout()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
