import sqlite3

# Fucntion to connect to the database 
def connect_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('flight_management.db')
    return conn

# Function to create a cursor
def create_cursor(conn):
    # Create a cursor object to execute SQL commands.
    return conn.cursor()

# Function to add a new flight - prompts the user for flight details and inserts the data into the Flight table
def add_new_flight(cursor, conn):
    # try block attempts to execute code that may raise exceptions (e.g., invalid input or database errors).
    try:
        # SQL query to select the last flight_id from the Flight table
        cursor.execute("SELECT MAX(flight_id) FROM Flight")
        # Cursor object used to fetch the last flight_id
        result = cursor.fetchone()
        last_flight_id = result[0] if result[0] is not None else 0
        new_flight_id = last_flight_id + 1

        # Prompt for the input details for the new flight
        departure_date = input("Enter Departure Date (YYYY-MM-DD): ")
        departure_time = input("Enter Departure Time (HH:MM:SS): ")
        status = input("Enter Flight Status (On-Time/Delayed/Cancelled): ")
        destination_id = int(input("Enter Destination ID: "))
        pilot_id = int(input("Enter Pilot ID: "))
        airplane_id = int(input("Enter Airplane ID: "))

        # Insert the new flight into the table
        # Excecute the SQL INSERT command, using ? as placeholders which are replaced by the user input
        cursor.execute('''
            INSERT INTO Flight (flight_id, departure_date, departure_time, status, destination_id, pilot_id, airplane_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)''', (new_flight_id, departure_date, departure_time, status, destination_id, pilot_id, airplane_id))
        # Save changes to the database
        conn.commit()
        print("Flight added.")
    # except blocks handle ValueError (for input issues) and sqlite3.Error (for database errors), ensuring the program doesn't crash.
    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function to view flights by criteria with a cursor parameter - allows the user to view flights based on the criteria; destination, status, or departure date
def view_flights_by_criteria(cursor):
    try:
        # Instruct user to enter the specific criteria for filtering the flights
        destination_id = input("Enter Destination ID (leave blank if not applicable): ")
        status = input("Enter Status (On-Time/Delayed/Cancelled) (leave blank if not applicable): ")
        departure_date = input("Enter Departure Date (YYYY-MM-DD) (leave blank if not applicable): ")

        # Base SQL query that selects all rows from the Flight table. 1=1 used to allow for addition of AND conditions
        query = "SELECT * FROM Flight WHERE 1=1"
        params = []

        # If statements ensure that if the user leaves an option blank then the application does not filter based off this
        # SQL condition appended to the base SQL query to filter by destination_id and/or status and/or departure_date
        # The value inputed is added to the params list
        if destination_id:
            query += " AND destination_id = ?"
            params.append(int(destination_id))
        if status:
            query += " AND status = ?"
            params.append(status)
        if departure_date:
            query += " AND departure_date = ?"
            params.append(departure_date)
        # Database interaction - execute the SQL SELECT command with the constructed query and parameters
        cursor.execute(query, params)
        # Cursor object used to fetch all matching rows from Flight table and store them in variable flights
        flights = cursor.fetchall()
        # Check if there are any flights matching the criteria and print out all the details of each flight
        if flights:
            for flight in flights:
                print(f"Flight ID: {flight[0]}, Departure Date: {flight[1]}, Departure Time: {flight[2]}, Status: {flight[3]}, Destination ID: {flight[4]}, Pilot ID: {flight[5]}, Airplane ID: {flight[6]}")
        else:
            print("No flights found for that criteria.")
    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function to update flight information - they can update the departure date, departure time, or status of a flight
# Takes parameters cursor and conn to interact and execute SQL commands (cursor) and make changes (conn)
def update_flight_info(cursor, conn):
    try:
        # Ask user to input information
        flight_id = int(input("Enter Flight ID to update: "))
        new_date = input("Enter new Departure Date (YYYY-MM-DD) (leave blank if no change): ")
        new_time = input("Enter new Departure Time (HH:MM:SS) (leave blank if no change): ")
        new_status = input("Enter new Status (On-Time/Delayed/Cancelled) (leave blank if no change): ")

        # Construct the update query dynamically based on user input
        # update_feilds list will store parts of the SQL UPDATE statement that need to change
        update_fields = []
        # params list will store the input values that replace the ? placeholder
        params = []
        
        # If statements update the lists if user entered an input
        if new_date:
            update_fields.append("departure_date = ?")
            params.append(new_date)
        if new_time:
            update_fields.append("departure_time = ?")
            params.append(new_time)
        if new_status:
            update_fields.append("status = ?")
            params.append(new_status)
        
        if update_fields:
            # SQL query - Updates the specific feilds in the Flight table, setting them to the inputted values only for the specific flight_id chosen (WHERE).
            query = f"UPDATE Flight SET {', '.join(update_fields)} WHERE flight_id = ?"
            params.append(flight_id)
            # Database interaction - execute the SQL UPDATE command with the constructed query and parameters
            cursor.execute(query, params)
            conn.commit()
            print("Flight information updated.")
        else:
            print("No changes made.")
    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function to assign a pilot to a flight, with parameters cursor and conn to allow for database interaction
def assign_pilot_to_flight(cursor, conn):
    try:
        flight_id = int(input("Enter Flight ID: "))
        new_pilot_id = int(input("Enter New Pilot ID: "))

        # SQL Query - updates the Flight table field pilot_id for a given flight_id to set it to the value inputted
        # Database interaction - cursor.execute used to execute the SQL UPDATE command
        cursor.execute("UPDATE Flight SET pilot_id = ? WHERE flight_id = ?", (new_pilot_id, flight_id))
        conn.commit()
        print("Pilot assigned.")
    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function to view a pilot's schedule - retrieves all flights assigned to a particular pilot
def view_pilot_schedule(cursor):
    try:
        pilot_id = int(input("Enter Pilot ID: "))
        # Execute SQL SELECT command that selects the row from the FLIGHT  table for a given pilot_id
        cursor.execute("SELECT * FROM Flight WHERE pilot_id = ?", (pilot_id,))
        # Fetch the specific rows selected and store the information in a list called flights
        flights = cursor.fetchall()
        if flights:
            for flight in flights:
                print(f"Flight ID: {flight[0]}, Departure Date: {flight[1]}, Departure Time: {flight[2]}, Status: {flight[3]}, Destination ID: {flight[4]}, Airplane ID: {flight[6]}")
        else:
            print("No flights found for that pilot ID.")
    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function to view or update destination information - take parameters cursor and conn to execute SQL commands and save changes to the database
def view_or_update_destination(cursor, conn):
    try:
        print("1. View Destination Information")
        print("2. Update Destination Information")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            destination_id = int(input("Enter Destination ID: "))
            # Execute SQL query that selects all feilds from the Destination table where the destination_id matches the value provided by the user.
            cursor.execute("SELECT * FROM Destination WHERE destination_id = ?", (destination_id,))
            # Fetch the single selected row from the result of the SELECT query and stores in the variable destination
            destination = cursor.fetchone()
            if destination:
                print(f"Destination ID: {destination[0]}, City: {destination[1]}, Country: {destination[2]}")
            else:
                print("No destination with that given ID.")
        elif choice == 2:
            destination_id = int(input("Enter Destination ID to update: "))
            new_city = input("Enter new City: ")
            new_country = input("Enter new Country: ")
            # Execute SQL UPDATE command to set the city and country fields to the value inputted by the user for the chosen detination_id
            cursor.execute("UPDATE Destination SET city = ?, country = ? WHERE destination_id = ?", (new_city, new_country, destination_id))
            conn.commit()
            print("Destination information updated.")
        else:
            print("Invalid input.")
    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function to view all flights in the database
def view_all_flights(cursor):
    try:
        # Execute SQL query to select all flights from the Flight table
        cursor.execute("SELECT * FROM Flight")
        flights = cursor.fetchall()
        # If flights are available, print each flight's details
        if flights:
            for flight in flights:
                print(f"Flight ID: {flight[0]}, Departure Date: {flight[1]}, Departure Time: {flight[2]}, Status: {flight[3]}, Destination ID: {flight[4]}, Pilot ID: {flight[5]}, Airplane ID: {flight[6]}")
        else:
            print("No flights available.")
    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function to view flight summary based on destinations, pilots, and airplanes
def view_flight_summary(cursor):
    try:
        # Number of flights to each destination
        print("\nNumber of flights to each destination:")
        # SQL Query that gives number of flights to each destination: 
        # Selects destination_id, city and country from the Destination table and counts the number of flights for each destination 
        # Using a LEFT JOIN connects Destination table with Flight table, ensuring that all destinations are included even if there are no flights to that destination.
        # Groups results by destination to calculate the count of flights for each
        cursor.execute('''
            SELECT d.destination_id, d.city, d.country, COUNT(f.flight_id) AS number_of_flights
            FROM Destination d
            LEFT JOIN Flight f ON d.destination_id = f.destination_id
            GROUP BY d.destination_id, d.city, d.country''')
        destinations = cursor.fetchall()
        for destination in destinations:
            print(f"Destination ID: {destination[0]}, City: {destination[1]}, Country: {destination[2]}, Number of Flights: {destination[3]}")

        # Number of flights assigned to each pilot
        print("\nNumber of flights assigned to each pilot:")
        # SQL Query that gives number of flights to each pilot:  
        # Selects pilot_id and name from the Pilot table and counts the number of flights for a specifc pilot. Then specifies Pilot as the main table 
        # Using a LEFT JOIN connects Pilot table with Flight table, ensuring all pilots are included even if they are not assigned to any flights
        # Groups results by pilot to calculate the count of flights for each
        cursor.execute('''
            SELECT p.pilot_id, p.name, COUNT(f.flight_id) AS number_of_flights
            FROM Pilot p
            LEFT JOIN Flight f ON p.pilot_id = f.pilot_id
            GROUP BY p.pilot_id, p.name''')
        pilots = cursor.fetchall()
        for pilot in pilots:
            print(f"Pilot ID: {pilot[0]}, Name: {pilot[1]}, Number of Flights: {pilot[2]}")

        # Number of flights for each airplane
        print("\nNumber of flights for each airplane:")
        # SQL Query that gives number of flights to each airplane:  
        # Selects airplane_id and model from the Airplane table and counts the number of flights for a specifc airplane. Then specifies Airplane as the main table 
        # Using a LEFT JOIN connects Airplane table with Flight table, ensuring all airplanes are included even if they are not assigned to any flights
        # Groups results by airplane to calculate the count of flights for each
        cursor.execute('''
            SELECT a.airplane_id, a.model, COUNT(f.flight_id) AS number_of_flights
            FROM Airplane a
            LEFT JOIN Flight f ON a.airplane_id = f.airplane_id
            GROUP BY a.airplane_id, a.model''')
        airplanes = cursor.fetchall()
        for airplane in airplanes:
            print(f"Airplane ID: {airplane[0]}, Model: {airplane[1]}, Number of Flights: {airplane[2]}")

    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function to delet a flight entry 
def delete_flight(cursor, conn):
    try:
        flight_id = int(input("Enter Flight ID to delete: "))
        #
        cursor.execute("DELETE FROM Flight WHERE flight_id = ?", (flight_id,))
        conn.commit()
        print("Flight deleted.")
    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function view complete flight details including departure information, destination details, pilot name, and airplane model and capacity.
def view_complete_flight_details(cursor):
    try:
        #SQL SELECT query combining information from all four tables using EQUI JOIN. Gives the rows that meet the WHERE conditions. 
        query = '''
            SELECT 
                f.flight_id,
                f.departure_date,
                f.departure_time,
                f.status,
                d.city AS destination_city,
                d.country AS destination_country,
                p.name AS pilot_name,
                a.model AS airplane_model,
                a.capacity AS airplane_capacity
            FROM 
                Flight f, Destination d, Pilot p, Airplane a
            WHERE 
                f.destination_id = d.destination_id
                AND f.pilot_id = p.pilot_id
                AND f.airplane_id = a.airplane_id;'''
        
        cursor.execute(query)
        flights = cursor.fetchall()
        
        if flights:
            for flight in flights:
                print(f"Flight ID: {flight[0]}, Departure Date: {flight[1]}, Departure Time: {flight[2]}, Status: {flight[3]}, "
                      f"Destination: {flight[4]}, {flight[5]}, Pilot: {flight[6]}, Airplane: {flight[7]}, Capacity: {flight[8]}")
        else:
            print("No flights available.")

    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# This function displays the main menu and handles user input to perform the corresponding operations
def main():
    # Connect to the database
    conn = connect_db()
    # Create a cursor to execute the SQL commands 
    cursor = create_cursor(conn)
    
    # Infinite loop to keep displaying the menu unitl the user exits
    while True:
        print("\nFlight Management System")
        print("1. Add a New Flight")
        print("2. View Flights by Criteria")
        print("3. Update Flight Information")
        print("4. Assign Pilot to Flight")
        print("5. View Pilot Schedule")
        print("6. View/Update Destination Information")
        print("7. View All Flights")
        print("8. View Flight Summary")
        print("9. Delete a Flight Entry")
        print("10. View Complete Flight Details")
        print("11. Exit")

        try:
            choice = int(input("Enter a number (1-11): "))

            if choice == 1:
                add_new_flight(cursor, conn)
            elif choice == 2:
                view_flights_by_criteria(cursor)
            elif choice == 3:
                update_flight_info(cursor, conn)
            elif choice == 4:
                assign_pilot_to_flight(cursor, conn)
            elif choice == 5:
                view_pilot_schedule(cursor)
            elif choice == 6:
                view_or_update_destination(cursor, conn)
            elif choice == 7:
                view_all_flights(cursor)
            elif choice == 8:
                view_flight_summary(cursor)
            elif choice == 9:
                delete_flight(cursor, conn)
            elif choice == 10:
                view_complete_flight_details(cursor)
            elif choice == 11:
                break
            else:
                print("Invalid input - enter a number between 1 and 11.")
        except ValueError:
            print("Invalid input.")
    # Close the connection before exiting
    conn.close()

if __name__ == "__main__":
    main()