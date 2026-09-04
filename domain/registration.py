class Registration:
    """
    Represents a Registration of a Person to an Event.
    
    """
    def __init__(self, person_id, event_id, date):
        """
        Initializes a new Registration instance.

        :param person_id: The unique ID of the person registering.
        :param event_id: The unique ID of the event.
        :param date: The date of the registration.
        """
        self.__person_id = person_id
        self.__event_id = event_id
        self.__date = date

    @property
    def person_id(self):
        """
        Gets the person's ID.
        :return: The person ID.
        """
        return self.__person_id

    @property
    def event_id(self):
        """
        Gets the event's ID.
        :return: The event ID.
        """
        return self.__event_id

    @property
    def date(self):
        """
        Gets the registration date.
        :return: The date string.
        """
        return self.__date

    def __str__(self):
        """
        Provides a user-friendly string representation of the Registration.
        :return: A formatted string linking Person and Event.
        """
        return f"Person ID: {self.person_id} -> Event ID: {self.event_id} | Date: {self.date}"

    def __eq__(self, other):
        """
        Checks equality between two registration objects.
        
        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        """
        if not isinstance(other, Registration):
            return False
        return self.person_id == other.person_id and self.event_id == other.event_id