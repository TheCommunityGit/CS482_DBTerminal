# Function to prompt for database login
def connectToDb(db_host, db_name, username, password):
    return True

def login():
    while True:  # Loop until the user confirms login or resets the form
        print("\n--- Database Login ---")

        # Collect input from the user
        db_host = input("Enter database host: ")
        db_name = input("Enter database name: ")
        username = input("Enter username: ")
        password = input("Enter password: ")

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
                break  # Exit the loop after a successful login
            else:
                print("Connection failed. Please check your credentials and try again.\n")
                break  # Exit the loop on failed connection (optional, can retry as per needs)

        elif action == 'r':
            print("\nForm reset. Please enter the details again.")
            continue  # Restart the form collection process
        else:
            print("Invalid input. Please press 'l' to log in or 'r' to reset the form.")
