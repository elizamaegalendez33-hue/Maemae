from datetime import datetime, timedelta, time
 
users = {}
teachers = {}
appointments = []
next_appointment_id = 1
 
 
def choose_date():
    today = datetime.now().date()
 
    print("\n========== SELECT AVAILABLE DATE ==========")
    print("Today's Date:", today.strftime("%A, %B %d, %Y"))
    print("\nAvailable Dates:")
 
    dates = []
    for number in range(7, 15):
        date = today + timedelta(days=number)
        dates.append(date)
        print(f"{len(dates)}. {date.strftime('%A - %B %d, %Y')}")
 
    print(f"{len(dates) + 1}. Back")
 
    choice = input("\nSelect date: ").strip()
 
    if not choice.isdigit():
        print("Invalid selection.")
        return None
 
    choice = int(choice)
 
    if choice == len(dates) + 1:
        return None
 
    if not 1 <= choice <= len(dates):
        print("Invalid selection.")
        return None
 
    return dates[choice - 1]
 
 
def choose_time():
    morning_times = [
        time(8, 0), time(8, 30), time(9, 0), time(9, 30),
        time(10, 0), time(10, 30), time(11, 0), time(11, 30)
    ]
 
    afternoon_times = [
        time(13, 30), time(14, 0), time(14, 30),
        time(15, 0), time(15, 30), time(16, 0)
    ]
 
    print("\n========== SELECT TIME ==========")
    print("1. Morning (8:00 AM - 11:30 AM)")
    print("2. Afternoon (1:30 PM - 4:00 PM)")
    print("3. Back")
 
    period = input("Choose time period: ").strip()
 
    if period == "3":
        return None
    elif period == "1":
        selected_times = morning_times
    elif period == "2":
        selected_times = afternoon_times
    else:
        print("Invalid selection.")
        return None
 
    print("\nAvailable Times:")
 
    for index, selected_time in enumerate(selected_times, start=1):
        print(f"{index}. {selected_time.strftime('%I:%M %p')}")
 
    print(f"{len(selected_times) + 1}. Back")
 
    choice = input("Select time: ").strip()
 
    if not choice.isdigit():
        print("Invalid selection.")
        return None
 
    choice = int(choice)
 
    if choice == len(selected_times) + 1:
        return None
 
    if not 1 <= choice <= len(selected_times):
        print("Invalid selection.")
        return None
 
    return selected_times[choice - 1]
 
 
def register():
    print("\n========== REGISTER ==========")
 
    while True:
        username = input("Enter username (letters only): ").strip()
 
        if not username.isalpha():
            print("Username must contain letters only.")
            continue
 
        if username in users:
            print("Username already exists.")
            continue
 
        break
 
    password = input("Create password: ")
 
    if password == "":
        print("Password cannot be empty.")
        return
 
    print("\nSelect account type:")
    print("1. Student")
    print("2. Teacher")
 
    account_type = input("Choose account type: ").strip()
 
    if account_type not in ("1", "2"):
        print("Invalid account type.")
        return
 
    if account_type == "1":
        users[username] = {"password": password, "type": "student"}
    else:
        users[username] = {"password": password, "type": "teacher"}
        teachers[username] = {"availability_slots": []}
 
    print("Registration successful!")
 
 
def login():
    print("\n========== LOGIN ==========")
 
    username = input("Username: ").strip()
    password = input("Password: ")
 
    if username not in users:
        print("Account not found.")
        return
 
    if users[username]["password"] != password:
        print("Incorrect password.")
        return
 
    if users[username]["type"] == "student":
        student_dashboard(username)
    else:
        teacher_dashboard(username)
 
 
def get_available_slots(teacher):
    today = datetime.now().date()
    earliest_date = today + timedelta(days=7)
    latest_date = today + timedelta(days=14)
 
    available = []
 
    for slot in teacher["availability_slots"]:
        schedule = slot["schedule"]
 
        if (
            slot["active"]
            and earliest_date <= schedule.date() <= latest_date
            and schedule > datetime.now()
        ):
            available.append(slot)
 
    available.sort(key=lambda slot: slot["schedule"])
    return available
 
 
def add_teacher_availability(teacher_username):
    teacher = teachers[teacher_username]
 
    selected_date = choose_date()
 
    if selected_date is None:
        return
 
    print("\nSelected Date:", selected_date.strftime("%A, %B %d, %Y"))
 
    while True:
        selected_time = choose_time()
 
        if selected_time is None:
            break
 
        schedule = datetime.combine(selected_date, selected_time)
 
        exists = False
        for slot in teacher["availability_slots"]:
            if slot["schedule"] == schedule:
                exists = True
 
        if exists:
            print("This availability slot already exists.")
        else:
            teacher["availability_slots"].append({
                "schedule": schedule,
                "active": True
            })
            print("\nAvailability added successfully!")
            print("Date:", schedule.strftime("%B %d, %Y"))
            print("Time:", schedule.strftime("%I:%M %p"))
 
        again = input("\nAdd another time for this date? (y/n): ").strip().lower()
 
        if again != "y":
            break
 
 
def view_teacher_availability(teacher_username):
    teacher = teachers[teacher_username]
    slots = get_available_slots(teacher)
 
    print("\n========== MY AVAILABILITY ==========")
 
    if not slots:
        print("No available slots.")
        return
 
    print("-" * 60)
    print(f"{'No.':<6}{'Date':<30}{'Time':<15}")
    print("-" * 60)
 
    for index, slot in enumerate(slots, start=1):
        schedule = slot["schedule"]
        print(
            f"{index:<6}"
            f"{schedule.strftime('%A, %B %d, %Y'):<30}"
            f"{schedule.strftime('%I:%M %p'):<15}"
        )
 
    print("-" * 60)
 
 
def print_appointments_table(records):
    if not records:
        print("No appointments found.")
        return
 
    print()
    print("=" * 110)
    print(
        f"{'ID':<5}"
        f"{'Student':<16}"
        f"{'Teacher':<16}"
        f"{'Date':<20}"
        f"{'Time':<12}"
        f"{'Status':<13}"
        f"{'Purpose':<20}"
        f"Reason"
    )
    print("=" * 110)
 
    for appointment in records:
        schedule = appointment["schedule"]
 
        print(
            f"{appointment['id']:<5}"
            f"{appointment['student'][:15]:<16}"
            f"{appointment['teacher'][:15]:<16}"
            f"{schedule.strftime('%b %d, %Y'):<20}"
            f"{schedule.strftime('%I:%M %p'):<12}"
            f"{appointment['status']:<13}"
            f"{appointment['purpose'][:19]:<20}"
            f"{appointment['reason']}"
        )
 
    print("=" * 110)
 
 
def book_appointment(student_username):
    global next_appointment_id
 
    print("\n========== BOOK CONSULTATION ==========")
 
    available_teachers = []
 
    for teacher_username, teacher in teachers.items():
        slots = get_available_slots(teacher)
 
        if slots:
            available_teachers.append((teacher_username, slots))
 
    if not available_teachers:
        print("No teachers have available consultation slots.")
        return
 
    print("\nAvailable Teachers:")
 
    for index, (teacher_username, slots) in enumerate(available_teachers, start=1):
        print(f"{index}. {teacher_username} ({len(slots)} available slots)")
 
    print(f"{len(available_teachers) + 1}. Back")
 
    choice = input("Select teacher: ").strip()
 
    if not choice.isdigit():
        print("Invalid selection.")
        return
 
    choice = int(choice)
 
    if choice == len(available_teachers) + 1:
        return
 
    if not 1 <= choice <= len(available_teachers):
        print("Invalid selection.")
        return
 
    teacher_username, slots = available_teachers[choice - 1]
 
    print("\nAvailable Consultation Slots:")
 
    for index, slot in enumerate(slots, start=1):
        schedule = slot["schedule"]
        print(
            f"{index}. {schedule.strftime('%A, %B %d, %Y')} "
            f"at {schedule.strftime('%I:%M %p')}"
        )
 
    print(f"{len(slots) + 1}. Back")
 
    choice = input("Select slot: ").strip()
 
    if not choice.isdigit():
        print("Invalid selection.")
        return
 
    choice = int(choice)
 
    if choice == len(slots) + 1:
        return
 
    if not 1 <= choice <= len(slots):
        print("Invalid selection.")
        return
 
    selected_slot = slots[choice - 1]
 
    section = input("Enter your section: ").strip()
    purpose = input("Enter consultation purpose: ").strip()
 
    if not section or not purpose:
        print("Section and purpose cannot be empty.")
        return
 
    appointment = {
        "id": next_appointment_id,
        "student": student_username,
        "section": section,
        "teacher": teacher_username,
        "schedule": selected_slot["schedule"],
        "purpose": purpose,
        "status": "Pending",
        "reason": "",
        "approved_at": None
    }
 
    appointments.append(appointment)
    selected_slot["active"] = False
    next_appointment_id += 1
 
    print("\nAppointment booked successfully!")
    print("Appointment ID:", appointment["id"])
    print("Status: Pending")
 
 
def view_student_appointments(student_username):
    records = [
        appointment for appointment in appointments
        if appointment["student"] == student_username
    ]
 
    print("\n========== MY APPOINTMENTS ==========")
    print_appointments_table(records)
 
 
def search_student_appointment(student_username):
    search_id = input("Enter appointment ID: ").strip()
 
    if not search_id.isdigit():
        print("Appointment ID must be a number.")
        return
 
    found = None
    for item in appointments:
        if item["student"] == student_username and item["id"] == int(search_id):
            found = item
 
    if found:
        print_appointments_table([found])
        print("Section:", found["section"])
    else:
        print("Appointment not found.")
 
 
def free_the_slot(appointment):
    teacher = teachers.get(appointment["teacher"])
 
    if teacher:
        for slot in teacher["availability_slots"]:
            if slot["schedule"] == appointment["schedule"]:
                slot["active"] = True
                break
 
 
def cancel_student_appointment(student_username):
    view_student_appointments(student_username)
 
    appointment_id = input("\nEnter appointment ID to cancel: ").strip()
 
    if not appointment_id.isdigit():
        print("Appointment ID must be a number.")
        return
 
    appointment = None
    for item in appointments:
        if item["student"] == student_username and item["id"] == int(appointment_id):
            appointment = item
 
    if not appointment:
        print("Appointment not found.")
        return
 
    if appointment["status"] == "Cancelled":
        print("This appointment is already cancelled.")
        return
 
    if appointment["status"] == "Rejected":
        print("Rejected appointments cannot be cancelled.")
        return
 
    if appointment["status"] == "Approved":
        unlock_date = appointment["approved_at"] + timedelta(days=2)
 
        if datetime.now() < unlock_date:
            print("You can cancel this appointment only after 2 days.")
            print("Cancellation allowed after:",
                  unlock_date.strftime("%B %d, %Y at %I:%M %p"))
            return
 
    appointment["status"] = "Cancelled"
    free_the_slot(appointment)
 
    print("Appointment cancelled successfully.")
 
 
def view_teacher_appointments(teacher_username):
    records = [
        appointment for appointment in appointments
        if appointment["teacher"] == teacher_username
    ]
 
    print("\n========== CONSULTATION APPOINTMENTS ==========")
    print_appointments_table(records)
 
 
def manage_appointment(teacher_username):
    pending = [
        appointment for appointment in appointments
        if appointment["teacher"] == teacher_username
        and appointment["status"] == "Pending"
    ]
 
    print("\n========== MANAGE APPOINTMENTS ==========")
 
    if not pending:
        print("No pending appointments.")
        return
 
    print_appointments_table(pending)
 
    appointment_id = input("\nEnter appointment ID to manage: ").strip()
 
    if not appointment_id.isdigit():
        print("Appointment ID must be a number.")
        return
 
    appointment = None
    for item in pending:
        if item["id"] == int(appointment_id):
            appointment = item
 
    if not appointment:
        print("Pending appointment not found.")
        return
 
    print("\n1. Approve")
    print("2. Reject")
    print("3. Back")
 
    choice = input("Choose action: ").strip()
 
    if choice == "1":
        appointment["status"] = "Approved"
        appointment["approved_at"] = datetime.now()
        appointment["reason"] = ""
        print("Appointment approved successfully.")
 
    elif choice == "2":
        reason = input("Enter reason for rejection: ").strip()
 
        if not reason:
            print("Rejection reason cannot be empty.")
            return
 
        appointment["status"] = "Rejected"
        appointment["reason"] = reason
        free_the_slot(appointment)
 
        print("Appointment rejected successfully.")
 
    elif choice == "3":
        return
 
    else:
        print("Invalid selection.")
 
 
def student_dashboard(student_username):
    while True:
        print("\n========== STUDENT DASHBOARD ==========")
        print("1. View Teacher Availability")
        print("2. Book Consultation")
        print("3. View My Appointments")
        print("4. Search Appointment")
        print("5. Cancel Appointment")
        print("6. Log Out")
 
        choice = input("Choose an option: ").strip()
 
        if choice == "1":
            print("\n========== TEACHER AVAILABILITY ==========")
 
            found = False
 
            for teacher_username in teachers:
                slots = get_available_slots(teachers[teacher_username])
 
                if slots:
                    found = True
                    print(f"\nTeacher: {teacher_username}")
 
                    for slot in slots:
                        schedule = slot["schedule"]
                        print(
                            f"- {schedule.strftime('%A, %B %d, %Y')} "
                            f"at {schedule.strftime('%I:%M %p')}"
                        )
 
            if not found:
                print("No available teacher slots.")
 
        elif choice == "2":
            book_appointment(student_username)
 
        elif choice == "3":
            view_student_appointments(student_username)
 
        elif choice == "4":
            search_student_appointment(student_username)
 
        elif choice == "5":
            cancel_student_appointment(student_username)
 
        elif choice == "6":
            print("Logged out successfully.")
            break
 
        else:
            print("Invalid selection. Please try again.")
 
 
def teacher_dashboard(teacher_username):
    while True:
        print("\n========== TEACHER DASHBOARD ==========")
        print("1. View Consultation Appointments")
        print("2. Approve or Reject Appointment")
        print("3. Add Availability Slots")
        print("4. View My Availability")
        print("5. Log Out")
 
        choice = input("Choose an option: ").strip()
 
        if choice == "1":
            view_teacher_appointments(teacher_username)
 
        elif choice == "2":
            manage_appointment(teacher_username)
 
        elif choice == "3":
            add_teacher_availability(teacher_username)
 
        elif choice == "4":
            view_teacher_availability(teacher_username)
 
        elif choice == "5":
            print("Logged out successfully.")
            break
 
        else:
            print("Invalid selection. Please try again.")
 
 
def main():
    while True:
        print("\n========== CONSULTATION APPOINTMENT SYSTEM ==========")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
 
        choice = input("Choose an option: ").strip()
 
        if choice == "1":
            register()
 
        elif choice == "2":
            login()
 
        elif choice == "3":
            print("Thank you for using the system!")
            break
 
        else:
            print("Invalid selection. Please try again.")
 
 
main()