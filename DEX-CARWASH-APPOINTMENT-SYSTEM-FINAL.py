from datetime import datetime
users = []
appointments = []
LINE = "=" * 58
DIVIDER = "-" * 58
ADMIN_USERNAME = "MIKEY"
ADMIN_PASSWORD = "IGLESIA0326082" 
STAFF_USERNAME1 = "STAFF1"
STAFF_PASSWORD1 = "STAFF1234"
PHONE_NUMBERS = "09948065140 / 09762465090"
car_prices = {
        "Taxi": 100, "Avanza Taxi": 120, "Hilux": 220, "Motorcycle": 170,"Jeep": 130, "Multicab": 120,
        "SUV": 200, "Sedan": 150, "Pickup Truck": 220, "Van": 180,"Mini Van": 160,"AUV": 170,
        "L300": 180, "Tricycle": 100, "Bus": 350,"Truck": 400, "Family Car": 150,
        "Electric Car": 200
    }

BOOKED = "Successfully Booked"
COMPLETED = "Completed"
statuses = [COMPLETED, "Cancelled"]
locations = ["Lumbia", "Bulua", "Lapasan", "Kauswagan", "Balulang", "Camaman-an", "Puerto", "Tumpagon", "Carmen", "Consolacion", "Macabalan", "Puntod", "Tablon", "Bugo", "Cugman", "Iponan", "Indahag", "Agusan", "Baikingon", "Balubal", "Bayabas",
                "Bayanga", "Besigan", "Bonbon", "Canitoan", "Dansolihon", "FS Catanico", "Gusa", "Macasandig", "Mambuaya", "Nazareth", "Pagalungan", "Pagatpat", "Patag", "Pigsag-an", "San Simon", "Taglimao", "Tagpangi", "Tignapoloan", "Tuburan"
    ]
# Cagayan de Oro locations: 40 named barangays plus numbered Barangays 1-40.
for number in range(1, 41):
        locations.append("Barangay " + str(number))
OPENING_TIME = datetime.strptime("04:00AM", "%I:%M%p").time()
CLOSING_TIME = datetime.strptime("09:00PM", "%I:%M%p").time()
def header(title):
        print()
        print(LINE)
        print(title)
        print(LINE)
def show_menu(title, options):
        header(title)
        for index, option in enumerate(options, start=1):
            print(str(index) + ". " + option)
        return input("Choose an option: ")
def run_menu(title, actions, greeting=None):
        """Repeat a menu until the last option (logout) is chosen. Actions is a list of (label, function) pairs. The last pair'sfunction is called once and then the menu closes."""
        labels = [label for label, _ in actions]
        while True:
            if greeting:
                greeting()
            choice = show_menu(title, labels)
            if not choice.isdigit() or not 1 <= int(choice) <= len(actions):
                print("Invalid choice.")
                continue
            index = int(choice) - 1
            actions[index][1]()
            if index == len(actions) - 1:
                break
def choose_from_list(prompt, options, error):
        """Ask for a number until a valid option is picked."""
        while True:
            choice = input(prompt)
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice) - 1]
            print(error)
def find_appointment(appointment_id):
        for appointment in appointments:
            if appointment["id"] == appointment_id:
                return appointment
        return None
def find_client(username):
        for client in users:
            if client["username"].lower() == username.lower():
                return client
        return None
def print_appointment(appointment, show_client=True):
        print()
        print("=" * 65)
        print("              DEX CAR WASH APPOINTMENT")
        print("=" * 65)
        print(f"{'Appointment Details':<25} | {'Information':<30}")
        print("-" * 65)
        print(f"{'Appointment ID':<25} | {appointment['id']}")
        if show_client:
            print(f"{'Client Username':<25} | {appointment['username']}")
        print(f"{'Location':<25} | {appointment['location']}")
        print(f"{'Car Model':<25} | {appointment['car']}")
        print(f"{'Plate Number':<25} | {appointment['plate']}")
        print(f"{'Date':<25} | {appointment['date']}")
        print(f"{'Time':<25} | {appointment['time']}")
        print(f"{'Price':<25} | PHP {appointment['price']}")
        print(f"{'Status':<25} | {appointment['status']}")
        print("=" * 65)

def print_summary(appointment, fields):
        """Print one appointment on a single line, e.g. ID | Date | Time."""
        parts = ["ID: " + str(appointment["id"])]
        for label, key in fields:
            parts.append(label + ": " + str(appointment[key]))
        print(" | ".join(parts))
def ask_appointment_id(prompt):
        choice = input(prompt)
        if not choice.isdigit():
            print("Invalid appointment ID.")
            return None
        return int(choice)
def active_appointments(user):
        return [
            appointment for appointment in appointments
            if appointment["username"] == user["username"]
            and appointment["status"] == BOOKED
        ]
# ===== PLATE NUMBER VALIDATION =====:
def ask_plate(prompt):
        while True:
            plate = input(prompt)
            if plate == "":
                print("Plate number cannot be empty.")
                continue
            has_letter = False
            has_number = False
            invalid_character = False
            for character in plate:
                if "A" <= character <= "Z" or "a" <= character <= "z":
                    has_letter = True
                elif "0" <= character <= "9":
                    has_number = True
                elif character == "-":
                    pass
                else:
                    invalid_character = True
            if invalid_character:
                print("Invalid plate number. Use only letters and numbers.")
                continue
            if not has_letter:
                print("Invalid plate number. It must contain letters.")
                continue
            if not has_number:
                print("Invalid plate number. It must contain numbers.")
                continue
            if plate[0] == "-" or plate[-1] == "-":
                print("Invalid plate number. Do not start or end with a hyphen.")
                continue
            double_hyphen = False
            for index in range(len(plate) - 1):
                if plate[index] == "-" and plate[index + 1] == "-":
                    double_hyphen = True
            if double_hyphen:
                print("Invalid plate number. Do not use consecutive hyphens.")
                continue
            return plate
def admin_menu():
        run_menu("ADMIN MENU", [
            ("View Client Appointments", view_all_appointments),
            ("View Registered Clients", view_registered_clients),
            ("Logout", lambda: print("Admin logged out."))
        ])
def staff_menu(staff_username):
        def greeting():
            print()
            print("Welcome,", staff_username)
        run_menu("STAFF MENU", [
            ("View Client Appointments", view_all_appointments),
            ("View Registered Clients", view_registered_clients),
            ("Update Appointment Status", update_appointment_status),
            ("Logout", lambda: print("Staff logged out."))
        ], greeting)
def update_appointment_status():
        header("UPDATE APPOINTMENT STATUS")
        if len(appointments) == 0:
            print("No appointments found.")
            return
        for appointment in appointments:
            print_summary(appointment, [
                ("Client", "username"),
                ("Date", "date"),
                ("Time", "time"),
                ("Status", "status")
            ])
        appointment_id = ask_appointment_id("Enter appointment ID: ")
        if appointment_id is None:
            return
        appointment = find_appointment(appointment_id)
        if appointment is None:
            print("Appointment not found.")
            return
        print()
        print_appointment(appointment)
        for index, status in enumerate(statuses, start=1):
            print(str(index) + ". " + status)
        choice = input("Choose new status: ")
        if not choice.isdigit() or not 1 <= int(choice) <= len(statuses):
            print("Invalid status.")
            return
        appointment["status"] = statuses[int(choice) - 1]
        print("Appointment status updated successfully!")
def view_all_appointments():
        header("ALL CLIENT APPOINTMENTS")
        if len(appointments) == 0:
            print("No client appointments found.")
            return
        for appointment in appointments:
            print_appointment(appointment)
def view_registered_clients():
        header("REGISTERED CLIENTS")
        if len(users) == 0:
            print("No registered clients.")
            return
        for client in users:
            print("Name:", client["name"])
            print("Username:", client["username"])
            print("Phone:", client["phone"])
            print("Location:", client["location"])
            print(DIVIDER)
def is_valid_name(name):
        parts = name.split(" ")
        if len(parts) < 2 or "" in parts:
            return False
        for part in parts:
            if part.endswith(".") and len(part) == 2:
                if not ("A" <= part[0] <= "Z"):
                    return False
            else:
                if not ("A" <= part[0] <= "Z"):
                    return False
                for ch in part[1:]:
                    if not ("a" <= ch <= "z"):
                        return False
        return True
def ask_name():
        while True:
            name = input("Enter full name (Example: First, Middle, Last): ")
            if not is_valid_name(name):
                print("Invalid full name. Use correct capitalization, like Marlou R. Iglesia.")
                print("Use one space between names; a middle initial may include a period.")
                continue
            if any(c["name"].lower() == name.lower() for c in users):
                print("This full name is already registered. Please check your name.")
                continue
            return name
def ask_username(full_name):
        while True:
            username = input("Enter username (Example: Jake0326): ")

            if username == "":
                print("Username cannot be empty.")
                continue

            if " " in username:
                print("Username cannot contain spaces.")
                continue

            # The username must begin with the customer's registered first name.
            first_name = full_name.split(" ")[0]
            if len(username) <= len(first_name):
                print("Add at least two numbers after your first name.")
                print("Example: " + first_name.lower() + "0326")
                continue

            if username[:len(first_name)].lower() != first_name.lower():
                print("Username must begin with your registered first name.")
                print("Example: " + first_name.lower() + "0326")
                continue

            number_part = username[len(first_name):]
            valid_numbers = True

            for ch in number_part:
                if ch < "0" or ch > "9":
                    valid_numbers = False
                    break

            if not valid_numbers or len(number_part) < 2:
                print("After your first name, enter at least two numbers only.")
                print("Example: " + first_name.lower() + "0326")
                continue

            if find_client(username) is not None:
                print("Username already exists. Please choose another username.")
                continue

            return username
def ask_password():
        while True:
            password = input("Enter password (Example: MyPassword123!): ")
            has_upper = False
            has_lower = False
            has_digit = False
            has_symbol = False
            for ch in password:
                if "A" <= ch <= "Z":
                    has_upper = True
                elif "a" <= ch <= "z":
                    has_lower = True
                elif "0" <= ch <= "9":
                    has_digit = True
                else:
                    has_symbol = True
            if len(password) < 8:
                print("Password must contain at least 8 characters.")
                continue
            if not has_upper:
                print("Password must contain at least one uppercase letter.")
                continue
            if not has_lower:
                print("Password must contain at least one lowercase letter.")
                continue
            if not has_digit:
                print("Password must contain at least one number.")
                continue
            if not has_symbol:
                print("Password must contain at least one symbol,!, @, #, $, %, ^, &, * or .")
                continue
            return password

def ask_phone():
        while True:
            phone = input("Enter phone number (Example: 09 or +639): ")
            valid_phone = False
            if phone.startswith("09") and len(phone) == 11 and phone.isdigit():
                valid_phone = True
            elif phone.startswith("+63") and len(phone) == 13 and phone[3:].isdigit():
                valid_phone = True
            if not valid_phone:
                print("Invalid phone number. Use 09XXXXXXXXX or +639XXXXXXXXX.")
                continue
            if any(c["phone"] == phone for c in users):
                print("This phone number is already registered. Please use another number.")
                continue
            return phone
def ask_location():
        header("SELECT LOCATION")
        print("Enter your Barangay or Location.")
        while True:
            location_input = input("Enter your location:(Example: Carmen): ")
            for location in locations:
                if location.lower() == location_input.lower():
                    return "Cagayan de Oro City - " + location
            print("Location not found.")
            print("Please enter a valid listed location.")
def register():
        header("CLIENT REGISTRATION")

        full_name = ask_name()
        username = ask_username(full_name)
        password = ask_password()
        phone = ask_phone()
        location = ask_location()

        # Save the registered client
        users.append({
            "name": full_name,
            "username": username,
            "password": password,
            "phone": phone,
            "location": location
        })

        header("REGISTRATION SUCCESSFUL")
        print("Your account has been created successfully! You can now log in to the system.")
def customer_menu(user):
        def greeting():
            print()
            print("Welcome,", user["name"])
            print("Your Location:", user["location"])
        run_menu("CUSTOMER MENU", [
            ("View Car Wash Prices", display_prices),
            ("Book Appointment", lambda: book_appointment(user)),
            ("View My Appointments", lambda: view_my_appointments(user)),
            ("Edit Appointment", lambda: edit_appointment(user)),
            ("Cancel Appointment", lambda: cancel_appointment(user)),
            ("Logout", lambda: print("Logged out successfully."))
        ], greeting)
def display_prices():
        header("CAR WASH PRICES")
        print(f"{'CAR MODEL':<22} {'PRICE'}")
        print("-" * 35)
        for car, price in car_prices.items():
            print(f"{car:<22} PHP {price}")
        print(LINE)
        print("Maximum of 4 bookings per time slot.")
        print("Operating hours: 4:00 AM - 9:00 PM.")
        print("For inquiries:", PHONE_NUMBERS)
def select_car():
        header("SELECT CAR TYPE")

        print("Available car models and prices:")
        print(f"{'CAR MODEL':<22} {'PRICE'}")
        print("-" * 35)
        for car, price in car_prices.items():
            print(f"{car:<22} PHP {price}")

        print()
        print("Enter your vehicle type or model by name, not a menu number.")
        print("If it is not listed above, enter a recognized make and model, then")
        print("choose the closest vehicle category for standard pricing.")

        # Common recognized models. Add models here when your group verifies them.
        approved_models = [
            "toyota vios", "toyota wigo", "toyota avanza", "toyota innova",
            "toyota hilux", "toyota fortuner", "toyota rush", "toyota corolla",
            "toyota raize", "toyota yaris", "toyota hiace", "toyota land cruiser",
            "honda civic", "honda city", "honda brio", "honda jazz",
            "honda cr-v", "honda hr-v", "honda br-v", "honda click",
            "mitsubishi mirage", "mitsubishi xpander", "mitsubishi montero",
            "mitsubishi strada", "mitsubishi l300", "nissan almera", "nissan navara",
            "nissan terra", "nissan kicks", "ford ranger", "ford everest",
            "ford ecosport", "suzuki swift", "suzuki ertiga", "suzuki spresso",
            "suzuki carry", "isuzu mu-x", "isuzu d-max", "isuzu traviz",
            "hyundai accent", "hyundai tucson", "hyundai stargazer", "kia seltos",
            "kia soluto", "kia carnival", "chevrolet trailblazer", "tesla model 3",
            "yamaha mio", "yamaha nmax", "yamaha sniper", "honda wave",
            "honda beat", "kawasaki ninja", "kawasaki barako", "vespa primavera"
        ]

        while True:
            car_input = input("Enter car type or model name (Example: Sedan or Honda Civic): ")
            # Reject empty input and input made only of spaces.
            if car_input == "" or car_input.isspace():
                print("Car model cannot be empty.")
                continue

            existing_car = None
            for car in car_prices:
                if car_input.lower() == car.lower():
                    existing_car = car
                    break
            if existing_car is not None:
                print("Selected car:", existing_car)
                print("Car wash price: PHP", car_prices[existing_car])
                return existing_car

            normalized_input = " ".join(car_input.lower().replace("-", " ").split())
            approved_match = False
            for model in approved_models:
                if normalized_input == " ".join(model.replace("-", " ").split()):
                    approved_match = True
                    break

            # Only accept an unlisted model when it matches a recognized model.
            # This prevents numbers-only or random text such as 'asfasfa' or
            # 'Toyota asfasfa' from being accepted as a valid vehicle model.
            if not approved_match:
                print("Unrecognized vehicle model. Please enter a listed car type or a verified model.")
                print("Examples: Toyota Vios, Honda Civic, Mitsubishi Mirage, or Sedan.")
                continue

            print()
            print("This verified model is not in the price list:", car_input)
            print("Choose the category that best matches your vehicle:")
            custom_categories = [
                ("Other small car / sedan", 150),
                ("Other compact utility vehicle", 170),
                ("Other SUV / electric car", 200),
                ("Other van / L300-sized vehicle", 180),
                ("Other pickup / large utility vehicle", 220),
                ("Other motorcycle", 170),
                ("Other tricycle", 100),
                ("Other bus", 350),
                ("Other heavy truck", 400)
            ]
            for index, (category, price) in enumerate(custom_categories, start=1):
                print(f"{index}. {category:<35} PHP {price}")

            while True:
                category_choice = input("Choose vehicle category (number): ")
                if category_choice.isdigit() and 1 <= int(category_choice) <= len(custom_categories):
                    selected_category, custom_price = custom_categories[int(category_choice) - 1]
                    car_prices[car_input] = custom_price
                    print("Vehicle model added for this session:", car_input)
                    print("Pricing category:", selected_category)
                    print("Assigned car wash price: PHP", custom_price)
                    return car_input
                print("Invalid category. Please choose a number from 1 to " + str(len(custom_categories)) + ".")

def validate_date():
        while True:
            date_input = input("Enter appointment date (YYYY-MM-DD - Example: 2026-10-20): ")
            try:
                selected_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Please use a current date or a future date in YYYY-MM-DD format.")
                continue
            if selected_date < datetime.now().date():
                print("Invalid date. Past dates are not allowed.")
                continue
            return date_input
def validate_time(date_input=None):
        """Ask for a time. If the chosen date is today, the time must still be ahead."""
        while True:
            time_input = input("Enter appointment time (4:00 AM - 9:00 PM - Example: 10:00AM): ")
            normalized_time = time_input.replace(" ", "").upper()
            try:
                selected_time = datetime.strptime(
                    normalized_time, "%I:%M%p"
                ).time()
            except ValueError:
                print("Invalid time format.")
                continue
            if not OPENING_TIME <= selected_time <= CLOSING_TIME:
                print("Time must be between 4:00 AM and 9:00 PM.")
                continue
            if date_input == datetime.now().strftime("%Y-%m-%d") and selected_time <= datetime.now().time():
                print("That time has already passed today. Please choose a later time.")
                continue
            return selected_time.strftime("%I:%M%p")
def ask_schedule():
        """Ask for a date and a time that have not passed yet."""
        while True:
            date = validate_date()
            if date == datetime.now().strftime("%Y-%m-%d") and datetime.now().time() >= CLOSING_TIME:
                print("No more available times today. Please choose another date.")
                continue
            return date, validate_time(date)
MAX_BOOKINGS_PER_SLOT = 4
def count_bookings_for_slot(date, time, excluded_id=None):
        """Count bookings (Successfully Booked or Completed) for a date and time, excluding an edited booking."""
        count = 0
        for appointment in appointments:
            if appointment["date"] == date and appointment["time"] == time:
                if appointment["status"] in (BOOKED, COMPLETED) and appointment["id"] != excluded_id:
                    count += 1
        return count
def is_slot_available(date, time, excluded_id=None):
        """A time slot is available while fewer than four bookings are booked or completed."""
        return count_bookings_for_slot(date, time, excluded_id) < MAX_BOOKINGS_PER_SLOT
def book_appointment(user):
        header("BOOK APPOINTMENT")
        print("Your registered location:", user["location"])
        car = select_car()
        plate = ask_plate("Enter plate number:(Example: ABC-1234 or XYZ-5678): ")
        date, time = ask_schedule()
        if not is_slot_available(date, time):
            print("This time slot has reached its maximum of 4 bookings.Please choose another date or time.")
            return
        appointment = {
            "id": max((a["id"] for a in appointments), default=0) + 1,
            "username": user["username"],
            "location": user["location"],
            "car": car,
            "plate": plate,
            "date": date,
            "time": time,
            "price": car_prices[car],
            "status": BOOKED
        }
        appointments.append(appointment)
        header("BOOKING CONFIRMATION")
        print("Client:", user["name"])
        print_appointment(appointment, show_client=False)
def view_my_appointments(user):
        header("MY APPOINTMENTS")
        mine = [a for a in appointments if a["username"] == user["username"]]
        if len(mine) == 0:
            print("You have no appointments.")
            return
        for appointment in mine:
            print_appointment(appointment, show_client=False)
def edit_car(appointment):
        appointment["car"] = select_car()
        appointment["price"] = car_prices[appointment["car"]]
        print("Car model and price updated.")
def edit_plate(appointment):
        plate = ask_plate("Enter new plate number:(Example: ABC-1234 or XYZ-5678): ")
        appointment["plate"] = plate
        print("Plate number updated.")
def edit_schedule(appointment):
        new_date, new_time = ask_schedule()
        if is_slot_available(new_date, new_time, appointment["id"]):
            appointment["date"] = new_date
            appointment["time"] = new_time
            print("Appointment schedule updated.")
        else:
            print("The selected schedule has reached its maximum of 4 bookings.")
            print("Your original schedule remains unchanged.")
EDIT_OPTIONS = [
        ("Change car model", edit_car),
        ("Change plate number", edit_plate),
        ("Change date and time", edit_schedule),
    ]
def edit_appointment(user):
        header("EDIT APPOINTMENT")
        active = active_appointments(user)
        if len(active) == 0:
            print("You have no appointments available to edit.")
            return
        for appointment in active:
            print_summary(appointment, [
                ("Car", "car"),
                ("Date", "date"),
                ("Time", "time")
            ])
        appointment_id = ask_appointment_id("Enter appointment ID to edit: ")
        if appointment_id is None:
            return
        appointment = find_appointment(appointment_id)
        if appointment not in active:
            print("Appointment not found or cannot be edited.")
            return
        print()
        for index, (label, _) in enumerate(EDIT_OPTIONS, start=1):
            print(str(index) + ". " + label)
        print(str(len(EDIT_OPTIONS) + 1) + ". Return")
        choice = input("Choose what to edit: ")
        if choice == str(len(EDIT_OPTIONS) + 1):
            return
        if not choice.isdigit() or not 1 <= int(choice) <= len(EDIT_OPTIONS):
            print("Invalid choice.")
            return
        EDIT_OPTIONS[int(choice) - 1][1](appointment)
        print("Appointment ID:", appointment["id"])
        print("Current status:", appointment["status"])
def cancel_appointment(user):
        header("CANCEL APPOINTMENT")
        active = active_appointments(user)
        if len(active) == 0:
            print("You have no active appointments.")
            return
        for appointment in active:
            print_summary(appointment, [
                ("Date", "date"),
                ("Time", "time"),
                ("Car", "car")
            ])
        appointment_id = ask_appointment_id("Enter appointment ID to cancel: ")
        if appointment_id is None:
            return
        appointment = find_appointment(appointment_id)
        if appointment not in active:
            print("Appointment not found.")
            return
        appointment["status"] = "Cancelled"
        print("Appointment cancelled successfully!")
def login_client():
        header("CLIENT LOGIN")
        username = input("Username: ")
        password = input("Password: ")
        for client in users:
            if client["username"] == username and client["password"] == password:
                print("Login successful!")
                customer_menu(client)
                return
        print("Invalid username or password.")
def login_admin():
        header("ADMIN LOGIN")
        username = input("Admin username: ")
        password = input("Admin password: ")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("Admin login successful!")
            admin_menu()
        else:
            print("Invalid admin username or password.")
def login_staff():
        header("STAFF LOGIN")
        username = input("Staff username: ")
        password = input("Staff password: ")
        if username == STAFF_USERNAME1 and password == STAFF_PASSWORD1:
            print("Staff login successful!")
            staff_menu(username)
        else:
            print("Invalid staff username or password.")
def login_menu():
        while True:
            choice = show_menu("LOGIN MENU", [
                "Customer Login", "Admin Login", "Staff Login","Return to Main Menu"
            ])
            if choice == "1":
                login_client()
            elif choice == "2":
                login_admin()
            elif choice == "3":
                login_staff()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please choose from 1 to 4.")
def main():
        while True:
            choice = show_menu("DEX CARWASH APPOINTMENT SYSTEM", [
                "Register", "Login", "Logout"
            ])
            if choice == "1":
                register()
            elif choice == "2":
                login_menu()
            elif choice == "3":
                print("You have logged out of DEX CARWASH APPOINTMENT SYSTEM. Thank you!")
                break
            else:
                print("Invalid choice. Please choose from 1 to 3.")

# ==========================================================
# RUN PROGRAM
# ==========================================================
if __name__ == "__main__":
        try:
            main()
        except (KeyboardInterrupt, EOFError):
            print("Program closed. Thank you for using DEX CARWASH!")