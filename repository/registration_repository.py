from domain.registration import Registration
from repository.exceptions import RepositoryException

class RegistrationRepository:
    """Manages the collection of Registration objects in memory using a List."""
    
    def __init__(self):
        """
        Initializes the RegistrationRepository with an empty list.
        """
        self._registrations = []

    def add(self, registration):
        """
        Adds a new registration to the list.

        :param registration: The Registration object to add.
        :return: None.
        """
        for reg in self._registrations:
            if reg.person_id == registration.person_id and reg.event_id == registration.event_id:
                raise RepositoryException("Person is already registered for this event.")
        
        self._registrations.append(registration)

    def delete(self, person_id, event_id):
        """
        Deletes a registration identified by Person ID and Event ID.

        :param person_id: The ID of the person.
        :param event_id: The ID of the event.
        :return: None.
        """
        reg_to_delete = None
        for reg in self._registrations:
            if reg.person_id == person_id and reg.event_id == event_id:
                reg_to_delete = reg
                break
        
        if reg_to_delete is None:
            raise RepositoryException("Registration not found.")
            
        self._registrations.remove(reg_to_delete)

    def get_all(self):
        """
        Returns a list of all registrations.

        :return: A copy of the list of registrations.
        """
        return self._registrations[:]