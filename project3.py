from simple_term_menu import TerminalMenu
from rich.table import Table
from rich.console import Console
import mysql.connector as sql
import sys
import getpass
import os

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
                        "Please press 'l' to confirm and log in, 'r' to reset the form, or 'q' to quit: ").lower()

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

        elif action == 'q' :
            print("\nQuitting terminal login.")
            quit()

        else:
            print("Invalid input.\nPlease press 'l' to log in, 'r' to reset the form, or 'q' to quit:")

def display_table_only():
    console = Console()
    table = Table(title="Digital Displays")

    # Add table columns for all attributes in the DigitalDisplay schema
    table.add_column("Serial No", justify="left")
    table.add_column("Scheduler System", justify="left")
    table.add_column("Model No", justify="left")

    # Fetch all digital displays from the database
    queryAllDigitalDisplays()

    # Populate the table with all rows
    for display in digital_displays:
        table.add_row(
            display["serial_no"],
            display["scheduler_system"],
            display["model_no"]
        )

    # Print the table
    console.print(table)

def display_all():
    console = Console()
    table = Table(title="Digital Displays")

    # Add table columns for all attributes in the DigitalDisplay schema
    table.add_column("Serial No", justify="left")
    table.add_column("Scheduler System", justify="left")
    table.add_column("Model No", justify="left")

    # Fetch all digital displays from the database
    queryAllDigitalDisplays()

    # Populate the table with all rows
    for display in digital_displays:
        table.add_row(
            display["serial_no"],
            display["scheduler_system"],
            display["model_no"]
        )

    # Print the table
    console.print(table)

    # Prepare a list of unique model numbers for the menu
    unique_models = list({display["model_no"] for display in digital_displays})

    while True:  # Keep the user in the display menu until they choose "Return to Main Menu"
        # Create menu options with unique model numbers
        options = [
            f"{model_no}" for model_no in unique_models
        ]
        options.append("Return to Main Menu")

        # Create and display the menu
        terminal_menu = TerminalMenu(options, title="\nSelect a model number to view more information:")
        choice = terminal_menu.show()

        if choice is not None and choice < len(unique_models):
            # Fetch more information using the selected model number
            selected_model_number = unique_models[choice]
            model_table = queryMoreInfo(selected_model_number)

            if model_table:
                # Display the model information as a table
                console.print(model_table)
            else:
                print(f"\nNo information found for Model No: {selected_model_number}")
        elif choice == len(unique_models):  # User chooses "Return to Main Menu"
            print("\nReturning to the main menu...")
            clear_terminal()
            break  # Exit the loop and return to the main menu



def search_display():
    global dbCursor  # Use the global database cursor

    # Fetch available scheduler systems from the database
    query_scheduler = "SELECT DISTINCT schedulerSystem FROM DigitalDisplay"
    dbCursor.execute(query_scheduler)
    scheduler_list = [row[0] for row in dbCursor.fetchall()]

    # Get input for the scheduler system
    scheduler_system = input("Enter a Scheduler System: ")

    # Check if the scheduler system exists
    if scheduler_system not in scheduler_list:
        print("\nInvalid Scheduler System. Exiting...\n")
        return

    print(f"\nSearching for digital displays by scheduler system: {scheduler_system}...\n")

    # Prepare to display results in a table
    console = Console()
    table = Table(title=f"Digital Displays for Scheduler System: {scheduler_system}")

    # Add table columns (all fields in DigitalDisplay schema)
    table.add_column("Serial No", justify="left")
    table.add_column("Scheduler System", justify="left")
    table.add_column("Model No", justify="left")

    # Query for digital displays with the given scheduler system
    query_display = """
        SELECT serialNo, schedulerSystem, modelNo
        FROM DigitalDisplay
        WHERE schedulerSystem = %s
    """
    dbCursor.execute(query_display, (scheduler_system,))
    displays = dbCursor.fetchall()

    # Populate the table with all retrieved fields
    for serial_no, scheduler_system, model_no in displays:
        table.add_row(serial_no, scheduler_system, model_no)

    # Print the table
    console.print(table)

    # Handle case when no results are found
    if not displays:
        print("\nNo digital displays found for the selected scheduler system.\n")
        return

    # Menu for further actions
    while True:
        # Create menu options with serial number and model number
        options = [f"Serial No: {display[0]}, Model No: {display[2]}" for display in displays]
        options.append("Return to Main Menu")

        # Show menu and get user choice
        terminal_menu = TerminalMenu(options, title="\nSelect a Display to view Model information:")
        choice = terminal_menu.show()

        if choice is not None and choice < len(displays):
            # Fetch selected display details
            selected_display = displays[choice]
            serial_no, scheduler_system, model_no = selected_display

            # Query detailed model information
            query_model = """
                SELECT modelNo, width, height, weight, depth, screenSize
                FROM Model
                WHERE modelNo = %s
            """
            dbCursor.execute(query_model, (model_no,))
            model_info = dbCursor.fetchone()

            # Display the detailed model information in a table
            if model_info:
                detailed_table = Table(title=f"Model Details for Model No: {model_no}")

                detailed_table.add_column("Field", justify="left")
                detailed_table.add_column("Value", justify="left")

                fields = ["Model No", "Width", "Height", "Weight", "Depth", "Screen Size"]
                for field, value in zip(fields, model_info):
                    detailed_table.add_row(field, str(value))

                console.print(detailed_table)
            else:
                print(f"\nNo additional model information found for Model No: {model_no}")
        elif choice == len(displays):  # User chooses "Return to Main Menu"
            print("\nReturning to the main menu...")
            break

def insert_display():
    global dbCursor, mydb  # Use the global database connection and cursor

    print("\nEnter Digital Display Information...\n")
    # Get input for the new digital display
    serial_no = input("Enter Serial No (max 10 chars): ").strip()
    scheduler_system = input("Enter Scheduler System (max 10 chars): ").strip()
    model_no = input("Enter Model No (max 10 chars): ").strip()

    # Validate input lengths
    if len(serial_no) > 10 or len(scheduler_system) > 10 or len(model_no) > 10:
        print("\nError: Inputs exceed maximum length. Please try again.")
        return

    # Check if the model exists in the Model table
    query_check_model = "SELECT modelNo FROM Model WHERE modelNo = %s"
    dbCursor.execute(query_check_model, (model_no,))
    model_exists = dbCursor.fetchone()

    if not model_exists:
        # Model does not exist, collect model information
        print(f"\nModel '{model_no}' does not exist. Please enter new model details.\n")

        try:
            width = float(input("Enter Model Width (numeric, max 6 digits, 2 decimals): "))
            height = float(input("Enter Model Height (numeric, max 6 digits, 2 decimals): "))
            weight = float(input("Enter Model Weight (numeric, max 6 digits, 2 decimals): "))
            depth = float(input("Enter Model Depth (numeric, max 6 digits, 2 decimals): "))
            screen_size = float(input("Enter Model Screen Size (numeric, max 6 digits, 2 decimals): "))

            # Validate numeric constraints (e.g., non-negative dimensions)
            if width <= 0 or height <= 0 or weight <= 0 or depth <= 0 or screen_size <= 0:
                print("\nError: All dimensions must be positive numbers. Aborting.")
                return

            # Insert the new model into the Model table
            query_insert_model = """
                INSERT INTO Model (modelNo, width, height, weight, depth, screenSize)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            dbCursor.execute(query_insert_model, (model_no, width, height, weight, depth, screen_size))
            mydb.commit()
            print("\nNew model inserted successfully.\n")

        except ValueError:
            print("\nError: Invalid numeric input. Aborting.")
            return
        except sql.Error as e:
            print(f"\nError inserting new model: {e}")
            return

    # Insert the new digital display
    print("\nInserting a new Digital Display...\n")
    try:
        query_insert_display = """
            INSERT INTO DigitalDisplay (serialNo, schedulerSystem, modelNo)
            VALUES (%s, %s, %s)
        """
        dbCursor.execute(query_insert_display, (serial_no, scheduler_system, model_no))
        mydb.commit()
        print("\nNew digital display inserted successfully.\n")

        # Display all digital displays after insertion
        display_table_only()

    except sql.Error as e:
        print(f"\nError inserting new digital display: {e}")

def delete_display():
    global dbCursor, mydb  # Use global variables for database connection and cursor

    console = Console()

    # Display all available digital displays for user selection
    display_table_only()

    # Prompt user to enter the Serial No of the display to delete
    serial_no_to_delete = input("\nEnter the Serial No of the display to delete: ").strip()

    try:
        # Check if the display exists
        query_check_display = "SELECT * FROM digitalDisplay WHERE serialNo = %s"
        dbCursor.execute(query_check_display, (serial_no_to_delete,))
        display_to_delete = dbCursor.fetchone()

        if not display_to_delete:
            print(f"\nNo digital display found with Serial No: {serial_no_to_delete}.")
            return

        # Confirm deletion
        confirmation = input(f"Are you sure you want to delete the display with Serial No '{serial_no_to_delete}'? (yes/no): ").lower()
        if confirmation != "yes":
            print("\nDeletion canceled.")
            return

        # Get the associated Model No before deletion
        model_no_to_delete = display_to_delete[2]  # Assuming modelNo is the 3rd column in the table

        # Delete the digital display from the database
        query_delete_display = "DELETE FROM digitalDisplay WHERE serialNo = %s"
        dbCursor.execute(query_delete_display, (serial_no_to_delete,))
        mydb.commit()

        print(f"\nDigital display with Serial No '{serial_no_to_delete}' has been deleted successfully.")

        # Check if any other displays are using the same Model No
        query_check_model = "SELECT COUNT(*) FROM digitalDisplay WHERE modelNo = %s"
        dbCursor.execute(query_check_model, (model_no_to_delete,))
        model_count = dbCursor.fetchone()[0]

        if model_count == 0:
            # No other displays use this Model No, so delete the model
            query_delete_model = "DELETE FROM Model WHERE modelNo = %s"
            dbCursor.execute(query_delete_model, (model_no_to_delete,))
            mydb.commit()
            print(f"Model No '{model_no_to_delete}' has also been deleted as it is no longer in use.")

        # Refresh the list of digital displays
        queryAllDigitalDisplays()
        console.print("\nUpdated list of digital displays:")
        display_table_only()

    except sql.Error as e:
        print(f"\nError occurred during deletion: {e}")


def update_display():
    console = Console()
    clear_terminal()
    print("\n--- Update Digital Display ---\n")

    # Step 1: Display current digital displays
    display_table_only()  # Show all digital displays for reference

    # Step 2: Get the Serial No of the display to update
    serial_no_to_update = input("Enter the Serial No of the display you want to update: ").strip()

    try:
        # Check if the display exists
        query_fetch_display = "SELECT * FROM DigitalDisplay WHERE serialNo = %s"
        dbCursor.execute(query_fetch_display, (serial_no_to_update,))
        display = dbCursor.fetchone()

        if not display:
            print(f"\nNo digital display found with Serial No: {serial_no_to_update}.")
            return

        # Step 3: Display current details
        print(f"\nCurrent details for Digital Display (Serial No: {serial_no_to_update}):")
        print(f"Scheduler System: {display[1]}")  # Assuming 2nd column is schedulerSystem
        print(f"Model No: {display[2]}")  # Assuming 3rd column is modelNo

        # Step 4: Prompt for new values
        scheduler_system = input("Enter new Scheduler System (leave blank to keep current): ").strip()
        model_no = input("Enter new Model No (leave blank to keep current): ").strip()

        # Use existing values if no input is provided
        if not scheduler_system:
            scheduler_system = display[1]
        if not model_no:
            model_no = display[2]

        # Step 5: Validate new Model No if changed
        if model_no != display[2]:
            query_check_model = "SELECT * FROM Model WHERE modelNo = %s"
            dbCursor.execute(query_check_model, (model_no,))
            model_exists = dbCursor.fetchone()

            if not model_exists:
                print(f"\nError: Model No '{model_no}' does not exist. Please ensure the model is created first.")
                return

        # Step 6: Update the record
        query_update_display = """
            UPDATE DigitalDisplay
            SET schedulerSystem = %s, modelNo = %s
            WHERE serialNo = %s
        """
        dbCursor.execute(query_update_display, (scheduler_system, model_no, serial_no_to_update))
        mydb.commit()

        print(f"\nDigital Display (Serial No: {serial_no_to_update}) updated successfully.")

        # Step 7: Display updated list
        print("\n--- Updated Digital Displays ---")
        display_table_only()

    except sql.Error as e:
        print(f"\nError updating the digital display: {e}")

    input("Press Enter to return to the main menu...")


def logout():
    clear_terminal()
    print("\nUser has been logged out.\n")
    login()


def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS or Linux
    else:
        os.system('clear')



# Main menu options
options = [
    "1. Display all digital displays",
    "2. Search for digital displays",
    "3. Insert a new digital display",
    "4. Delete a digital display",
    "5. Update a digital display",
    "6. Logout",
    "7. Logout and exit"
]
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
            logout()
        elif choice ==6:
            clear_terminal()
            quit()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
