from domain.person import Person
from domain.event import Event
from domain.registration import Registration
from validation.exceptions import ValidationException
from repository.exceptions import RepositoryException

class MainController:
    """
    Coordinates the operations for the application.
    """
    def __init__(self, person_repo, event_repo, registration_repo, 
                 person_validator, event_validator, registration_validator):
        """
        Initializes the MainController.

        :param person_repo: The repository for persons.
        :param event_repo: The repository for events.
        :param registration_repo: The repository for registrations.
        :param person_validator: The validator for persons.
        :param event_validator: The validator for events.
        :param registration_validator: The validator for registrations.
        """
        self._person_repo = person_repo
        self._event_repo = event_repo
        self._registration_repo = registration_repo
        
        self._person_validator = person_validator
        self._event_validator = event_validator
        self._registration_validator = registration_validator

    # --- Person Operations ---

    def add_person(self, person_id, name):
        """
        Creates, validates, and adds a new person.

        :param person_id: The ID of the new person.
        :param name: The name of the new person.
        :return: None.
        """
        person = Person(person_id, name)
        self._person_validator.validate(person)
        self._person_repo.add(person)

    def delete_person(self, person_id):
        """
        Deletes a person by their ID.

        :param person_id: The ID of the person to delete.
        :return: None.
        """
        self._person_repo.delete(person_id)

    def update_person(self, person_id, new_name):
        """
        Updates an existing person's name.

        :param person_id: The ID of the person to update.
        :param new_name: The new name for the person.
        :return: None.
        """
        temp_person = Person(person_id, new_name)
        self._person_validator.validate(temp_person)
        self._person_repo.update(person_id, new_name)

    def get_all_persons(self):
        """
        Retrieves all persons.

        :return: A list of all Person objects.
        """
        return self._person_repo.get_all()

    def search_person_by_name(self, query):
        """
        Searches for persons by name.

        :param query: The search string.
        :return: A list of matching Person objects.
        """
        return self._person_repo.search_by_name(query)

    # --- Event Operations ---

    def add_event(self, event_id, date, time, description):
        """
        Creates, validates, and adds a new event.

        :param event_id: The ID of the new event.
        :param date: The date of the event.
        :param time: The time of the event.
        :param description: The description of the event.
        :return: None.
        """
        event = Event(event_id, date, time, description)
        self._event_validator.validate(event)
        self._event_repo.add(event)

    def delete_event(self, event_id):
        """
        Deletes an event by its ID.

        :param event_id: The ID of the event to delete.
        :return: None.
        """
        self._event_repo.delete(event_id)

    def update_event(self, event_id, new_date, new_time, new_description):
        """
        Updates an existing event's details.

        :param event_id: The ID of the event to update.
        :param new_date: The new date for the event.
        :param new_time: The new time for the event.
        :param new_description: The new description for the event.
        :return: None.
        """
        temp_event = Event(event_id, new_date, new_time, new_description)
        self._event_validator.validate(temp_event)
        self._event_repo.update(event_id, new_date, new_time, new_description)

    def get_all_events(self):
        """
        Retrieves all events.

        :return: A list of all Event objects.
        """
        return self._event_repo.get_all()

    def search_event_by_description(self, query):
        """
        Searches for events by description.

        :param query: The search string.
        :return: A list of matching Event objects.
        """
        return self._event_repo.search_by_description(query)

    # --- Registration Operations (Iteration 2) ---

    def register_person_for_event(self, person_id, event_id, date):
        """
        Registers a person for an event.

        :param person_id: The ID of the person to register.
        :param event_id: The ID of the event to register for.
        :param date: The date of registration.
        :return: None.
        """
        # 1. Check if Person exists
        try:
            self._person_repo.find_by_id(person_id)
        except RepositoryException:
            raise RepositoryException(f"Cannot register: Person with ID {person_id} does not exist.")

        # 2. Check if Event exists
        try:
            self._event_repo.find_by_id(event_id)
        except RepositoryException:
            raise RepositoryException(f"Cannot register: Event with ID {event_id} does not exist.")

        # 3. Create and Validate Registration
        registration = Registration(person_id, event_id, date)
        self._registration_validator.validate(registration)

        # 4. Save
        self._registration_repo.add(registration)

    def get_all_registrations(self):
        """
        Retrieves all registrations.

        :return: A list of all Registration objects.
        """
        return self._registration_repo.get_all()

    # --- Reports  ---

    def get_events_for_person_ordered(self, person_id, sort_by_date=False):
        """
        Returns the list of events a person is participating in.
        
        :param person_id: The ID of the person.
        :param sort_by_date: If True, sort by date. If False, sort by description.
        :return: List of Event objects.
        """
        self._person_repo.find_by_id(person_id)

        all_regs = self._registration_repo.get_all()
        person_event_ids = [reg.event_id for reg in all_regs if reg.person_id == person_id]

        person_events = []
        for e_id in person_event_ids:
            event = self._event_repo.find_by_id(e_id)
            person_events.append(event)
        if sort_by_date:
            person_events.sort(key=lambda e: e.date)
        else:
            person_events.sort(key=lambda e: e.description)

        return person_events

    def get_most_active_persons(self):
        """
        Returns the top 3 persons participating in the most events.
        
        :return: List of tuples (Person, count).
        """
        all_persons = self._person_repo.get_all()
        all_regs = self._registration_repo.get_all()

        counts = {}
        for p in all_persons:
            counts[p.person_id] = 0 
        
        for reg in all_regs:
            if reg.person_id in counts:
                counts[reg.person_id] += 1

        # Convert to list of (Person, count)
        result_list = []
        for p_id, count in counts.items():
            person = self._person_repo.find_by_id(p_id)
            result_list.append((person, count))

        result_list.sort(key=lambda x: x[1], reverse=True)

        return result_list[:3]

    def get_top_20_percent_events(self):
        """
        Returns top 20% of events with most participants.
        
        :return: List of tuples (Event Description, participant_count).
        """
        all_events = self._event_repo.get_all()
        all_regs = self._registration_repo.get_all()

        # Count participants per event
        counts = {}
        for e in all_events:
            counts[e.event_id] = 0
            
        for reg in all_regs:
            if reg.event_id in counts:
                counts[reg.event_id] += 1

        # Create list of (description, count)
        result_list = []
        for e_id, count in counts.items():
            event = self._event_repo.find_by_id(e_id)
            result_list.append((event.description, count))

        result_list.sort(key=lambda x: x[1], reverse=True)

        total_events = len(result_list)
        if total_events == 0:
            return []

        limit = int(total_events * 0.2)
        if limit == 0 and total_events > 0:
            limit = 1
            
        return result_list[:limit]

    def get_persons_for_event_by_reg_date(self, event_id):
        """
        Returns the list of persons registered for a specific event,
        ordered by the date they registered.
        
        :param event_id: The ID of the event.
        :return: List of tuples (Person object, registration_date_string).
        """
        self._event_repo.find_by_id(event_id)

        all_regs = self._registration_repo.get_all()
        event_regs = [reg for reg in all_regs if reg.event_id == event_id]

        event_regs.sort(key=lambda r: r.date)

        result = []
        for reg in event_regs:
            person = self._person_repo.find_by_id(reg.person_id)
            result.append((person, reg.date))

        return result