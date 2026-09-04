from validation.exceptions import ValidationException
from repository.exceptions import RepositoryException

class ConsoleUI:
    def __init__(self, controller):
        """
        Initializes the ConsoleUI.
        
        :param controller: The main controller instance.
        """
        self._controller = controller

    def _print_menu(self):
        print("\n--- Event Organization Menu ---")
        print("1. Manage Persons")
        print("2. Manage Events")
        print("3. Manage Registrations")
        print("4. Reports")  
        print("0. Exit")

    def run(self):
        """Starts the main application loop."""
        while True:
            self._print_menu()
            cmd = input("Enter command: ").strip()
            if cmd == "1":
                self._run_person_menu()
            elif cmd == "2":
                self._run_event_menu()
            elif cmd == "3":
                self._run_registration_menu()
            elif cmd == "4":
                self._run_reports_menu()  
            elif cmd == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid command.")

    def _run_person_menu(self):
        while True:
            print("\n  --- Manage Persons ---")
            print("  1. Add Person")
            print("  2. Delete Person")
            print("  3. Modify Person")
            print("  4. Display All Persons")
            print("  5. Search Persons by Name")
            print("  0. Back to Main Menu")
            cmd = input("  Enter person command: ").strip()
            if cmd == "1": self._ui_add_person()
            elif cmd == "2": self._ui_delete_person()
            elif cmd == "3": self._ui_update_person()
            elif cmd == "4": self._ui_display_all_persons()
            elif cmd == "5": self._ui_search_person_by_name()
            elif cmd == "0": break
            else: print("Invalid command.")

    def _run_event_menu(self):
        while True:
            print("\n  --- Manage Events ---")
            print("  1. Add Event")
            print("  2. Delete Event")
            print("  3. Modify Event")
            print("  4. Display All Events")
            print("  5. Search Events by Description")
            print("  0. Back to Main Menu")
            cmd = input("  Enter event command: ").strip()
            if cmd == "1": self._ui_add_event()
            elif cmd == "2": self._ui_delete_event()
            elif cmd == "3": self._ui_update_event()
            elif cmd == "4": self._ui_display_all_events()
            elif cmd == "5": self._ui_search_event_by_description()
            elif cmd == "0": break
            else: print("Invalid command.")

    def _run_registration_menu(self):
        while True:
            print("\n  --- Manage Registrations ---")
            print("  1. Register Person for Event")
            print("  2. Display All Registrations")
            print("  0. Back")
            cmd = input("  Enter command: ").strip()
            if cmd == "1": self._ui_register()
            elif cmd == "2": self._ui_display_registrations()
            elif cmd == "0": break
            else: print("Invalid command.")

    def _ui_add_person(self):
        try:
            pid = input("  Enter Person ID (CNP): ")
            name = input("  Enter Name: ")
            self._controller.add_person(pid, name)
            print("Person added!")
        except Exception as e: print(e)
    
    def _ui_delete_person(self):
        try:
            pid = input("  Enter Person ID to delete: ")
            self._controller.delete_person(pid)
            print("Deleted.")
        except Exception as e: print(e)

    def _ui_update_person(self):
        try:
            pid = input("  Enter Person ID to update: ")
            n = input("  Enter new Name: ")
            self._controller.update_person(pid, n)
            print("Updated.")
        except Exception as e: print(e)

    def _ui_display_all_persons(self):
        for p in self._controller.get_all_persons(): print(p)

    def _ui_search_person_by_name(self):
        q = input("  Search: ")
        for p in self._controller.search_person_by_name(q): print(p)

    def _ui_add_event(self):
        try:
            eid = input("  Event ID: ")
            d = input("  Date: ")
            t = input("  Time: ")
            desc = input("  Description: ")
            self._controller.add_event(eid, d, t, desc)
            print("Event added!")
        except Exception as e: print(e)

    def _ui_delete_event(self):
        try:
            eid = input("  Delete Event ID: ")
            self._controller.delete_event(eid)
            print("Deleted.")
        except Exception as e: print(e)

    def _ui_update_event(self):
        try:
            eid = input("  Event ID: ")
            d = input("  New Date: ")
            t = input("  New Time: ")
            desc = input("  New Desc: ")
            self._controller.update_event(eid, d, t, desc)
            print("Updated.")
        except Exception as e: print(e)

    def _ui_display_all_events(self):
        for e in self._controller.get_all_events(): print(e)

    def _ui_search_event_by_description(self):
        q = input("  Search: ")
        for e in self._controller.search_event_by_description(q): print(e)

    def _ui_register(self):
        try:
            pid = input("  Person ID: ")
            eid = input("  Event ID: ")
            d = input("  Date (YYYY-MM-DD): ")
            self._controller.register_person_for_event(pid, eid, d)
            print("Registered!")
        except Exception as e: print(e)

    def _ui_display_registrations(self):
        for r in self._controller.get_all_registrations(): print(r)


    def _run_reports_menu(self):
        while True:
            print("\n  --- Reports ---")
            print("  1. Events for a Person (Ordered)")
            print("  2. Most Active Persons (Top 3)")
            print("  3. Top 20% Events")
            print("  4. Persons for Event (Sorted by Reg Date)")
            print("  0. Back")
            
            cmd = input("  Enter command: ").strip()
            if cmd == "1":
                self._ui_report_person_events()
            elif cmd == "2":
                self._ui_report_top_persons()
            elif cmd == "3":
                self._ui_report_top_events()
            elif cmd == "4":
                self._ui_report_persons_by_reg_date()
            elif cmd == "0":
                break
            else:
                print("Invalid command.")

    def _ui_report_person_events(self):
        person_id = input("  Enter Person ID: ").strip()
        print("  Sort by: 1. Description  2. Date")
        sort_opt = input("  Choice: ").strip()
        
        sort_by_date = False
        if sort_opt == "2":
            sort_by_date = True
            
        try:
            events = self._controller.get_events_for_person_ordered(person_id, sort_by_date)
            if not events:
                print("  No events found for this person.")
            else:
                print(f"\n  Events for Person {person_id}:")
                for e in events:
                    print(e)
        except RepositoryException as e:
            print(f"Error: {e}")

    def _ui_report_top_persons(self):
        results = self._controller.get_most_active_persons()
        print("\n  --- Top 3 Most Active Persons ---")
        for person, count in results:
            print(f"{person.name} (ID: {person.person_id}) - {count} events")

    def _ui_report_top_events(self):
        results = self._controller.get_top_20_percent_events()
        print("\n  --- Top 20% Events by Participants ---")
        for desc, count in results:
            print(f"Event: {desc} - {count} participants")
    
    def _ui_report_persons_by_reg_date(self):
        event_id = input("  Enter Event ID: ").strip()
        try:
            results = self._controller.get_persons_for_event_by_reg_date(event_id)
            
            if not results:
                print("  No participants found for this event.")
            else:
                print(f"\n  Persons registered for Event {event_id} (by Registration Date):")
                for person, date in results:
                    print(f"  {date}: {person.name} (ID: {person.person_id})")                 
        except RepositoryException as e:
            print(f"Error: {e}")