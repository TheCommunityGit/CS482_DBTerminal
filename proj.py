
# python version used was 3.13


# essential imports for functionality
import mysql.connector as sql
import sys


# Connect to the MySQL database as required in project description
mydb = sql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="abc"
)

# debug helpers
#print("Connected to the database successfully.")
#print()

# this is the connect used while developing and testing
'''
mydb = sql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="abc"
)
'''

# Create a cursor object
mycursor = mydb.cursor()


# Q1 : fidn the sites that are on a given street
def find_site_on_street(street_name):
    query = "SELECT * FROM Site WHERE address LIKE %s"

    search_term = f"%{street_name}%"

    # Executing the query
    mycursor.execute(query, (search_term,))

    # Fetching all the results
    sites = mycursor.fetchall()

    # Printing the table header
    print(f"{'Site Code':<10} {'Type':<15} {'Address':<25} {'Phone':<16}")
    print("-" * 60)

    # Iterate through the results and print them in a  table
    for site in sites:
        site_code, type_of_site, address, phone = site
        print(f"{site_code:<10} {type_of_site:<15} {address:<25} {phone:<16}")

    return


# Q2 Find the digital displays with a given scheduler system
def find_DD_with_SS(scheduler_system):

    # Query to fetch digital display info, model number, and technical support name
    query = """
    SELECT dd.serialNo, dd.modelNo, ts.name
    FROM DigitalDisplay AS dd, Specializes AS sp, TechnicalSupport AS ts
    WHERE dd.modelNo = sp.modelNo
      AND sp.empId = ts.empId
      AND dd.schedulerSystem = %s;

    """
    # Execute the query
    mycursor.execute(query, (scheduler_system,))

    # Fetch the results
    results = mycursor.fetchall()

    # Print the header
    print(f"{'Serial No':<12} {'Model No':<10} {'Technical Support':<20}")
    print("-" * 42)

    # Iterate through the results and print them in a  table
    for serial_no, model_no, tech_support in results:
        print(f"{serial_no:<12} {model_no:<10} {tech_support:<20}")

    return


#Q3 List the distinct names of all salesmen and the number of salesmen with that name.
def list_all_salesmen_and_sales():

    # Query to list distinct names and count how many salesmen have each name
    count_query = """
    SELECT name, COUNT(*) AS cnt
    FROM Salesman
    GROUP BY name
    ORDER BY name;
    """

    # Query to show details of all salesmen with duplicate names
    details_query = """
    SELECT empId, name, gender
    FROM Salesman
    WHERE name IN (
        SELECT name
        FROM Salesman
        GROUP BY name
        HAVING COUNT(*) > 1
    )
    ORDER BY name, empId;
    """

    # execute the count and get the numbers
    mycursor.execute(count_query)
    name_counts = mycursor.fetchall()

    # Print header
    print(f"{'Name':<20} {'Count':<5}")
    print("-" * 25)

    # Store name counts in a dictionary
    name_count_dict = {}
    salesman_details_dict = {}

    for name, count in name_counts:
        name_count_dict[name] = int(str(count))

    # Fetch all salesman details at once
    mycursor.execute(details_query)
    all_salesmen = mycursor.fetchall()

    # Organize salesman details by name
    for empId, name, gender in all_salesmen:
        if name in salesman_details_dict:
            salesman_details_dict[name].append((empId, name, gender))
        else:
            salesman_details_dict[name] = [(empId, name, gender)]

    # Print name counts and details ( Sorted alphabetically)
    for name in sorted(name_count_dict.keys()):
        count = name_count_dict[name]
        print(f"{name:<20} {count:<5}", end="")

    # Check if there are duplicates and print their details
        if count > 1:
            duplicates_output = ', '.join([f"({empId},{name},'{gender}')" for empId, name, gender in salesman_details_dict[name]])
            print(f" {duplicates_output}")
        else:
            # ensure there is a new line when only 1 salesman has this name
            print()
    return


# Q4 Find the clients with a given phone number
def find_clients_with_num(num):

    # query to find the specific client(s)
    query = "SELECT * FROM Client WHERE phone = %s"

    search_term = f"{num}"

    # run query
    mycursor.execute(query, (search_term,))


    clients = mycursor.fetchall()

    # no format was specified so we just print the tuples as they are
    for client in clients:
        print(client)

    return


#Q5 Find the total working hours of each administrator.
def total_admin_work_hours():

    # query to calculate total work hours of each admin
    query = """
    SELECT a.empId, a.name,
           (SELECT SUM(aw.hours)
            FROM AdmWorkHours AS aw
            WHERE aw.empId = a.empId) AS total_hours
    FROM Administrator AS a
    ORDER BY total_hours ASC;
    """

    # Execute the query
    mycursor.execute(query)

    # Fetch all results
    results = mycursor.fetchall()

    # Print the header
    print(f"{'Emp ID':<10} {'Name':<20} {'Total Hours':<15}")
    print("-" * 50)

    # iterate through results and print them formatted
    for empId, name, total_hours in results:
        # If total_hours is None, print 0 instead
        if total_hours is None:
            total_hours = 0
        print(f"{empId:<10} {name:<20} {total_hours:<15}")

    return


# Q6 Find the technical supports that specialize a specified model.
def techsupport_in_model(model):

    # logic to get the names of those to specialize in model
    query = """
    SELECT ts.name
    FROM TechnicalSupport AS ts, Specializes AS sp
    WHERE  ts.empId = sp.empId AND sp.modelNo = %s
    """
    particular_model = f"{model}"

    # execute the query
    mycursor.execute(query,(particular_model,))

    # get results
    tech_support = mycursor.fetchall()

    # unpack tuples and prints names
    for tech in tech_support:
        print(tech[0])

    return


# Q7 Order the salesmen with descending order of their average commission rates.
def average_salesmen_commission():

    # query to get salesman ordered by their avg commission
    query = """
     SELECT s.name, AVG(p.commissionRate) AS avg_commission
     FROM Salesman AS s, Purchases AS p
     WHERE s.empId = p.empId
     GROUP BY s.name
     ORDER BY avg_commission DESC;
     """

    # run query
    mycursor.execute(query)
    results = mycursor.fetchall()

    # print header
    print(f"{'Salesman Name':<20} {'Average Commission':<20}")
    print("-" * 40)

    # print formatted details
    for name, avg_commission in results:
        print(f"{name:<20} {avg_commission:<20.2f}")

    return


# Q8 Calculate the number of administrators, salesmen, and technical supports.
def num_of_adm_salesmen_ts():
    # SQL queries to count the number of administrators, salesmen, and technical supports
    query_admins = "SELECT COUNT(*) FROM administrator;"
    query_salesmen = "SELECT COUNT(*) FROM salesman;"
    query_tech_supports = "SELECT COUNT(*) FROM TechnicalSupport;"

    # Execute the queries and unpack the tuples so we only get the number we need
    mycursor.execute(query_admins)
    admin_count = mycursor.fetchall()[0][0]

    mycursor.execute(query_salesmen)
    salesman_count = mycursor.fetchall()[0][0]

    mycursor.execute(query_tech_supports)
    tech_count = mycursor.fetchall()[0][0]

    # Print the results in the specified format
    print("Role        cnt")
    print("------------------")
    print(f"Administrator  {admin_count}")
    print(f"Salesmen       {salesman_count}")
    print(f"Technicians    {tech_count}")

    return


# main function where all the core logic is for handeling cmd arguments
def main():
    args = []
    if len(sys.argv) >= 2:
            args = sys.argv[1:]
    else:
        print("not enough args, terminating program")
        return


    match(int(args[0])):
        case 1:
            return find_site_on_street(args[1])
        case 2:
            return find_DD_with_SS(args[1])
        case 3:
            return list_all_salesmen_and_sales()
        case 4:
            return find_clients_with_num(args[1])
        case 5:
            return total_admin_work_hours()
        case 6:
            return techsupport_in_model(args[1])
        case 7:
            return average_salesmen_commission()
        case 8:
            return num_of_adm_salesmen_ts()
        case _:
            return print("invalid argument, terminating")

    return 0

if __name__ == '__main__':
    main()
