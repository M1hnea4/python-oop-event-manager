class Event:
    """
    Represents an Event entity.
    
    Attributes:
        __event_id (str): The unique ID of the event (private).
        __date (str): The date of the event (private).
        __time (str): The time of the event (private).
        __description (str): The description of the event (private).
    """
    def __init__(self, event_id, date, time, description):
        """
        Initializes a new Event instance.
        
        :param event_id: The unique ID of the event.
        :param date: The date (YYYY-MM-DD).
        :param time: The time (HH:MM).
        :param description: The description.
        """
        self.__event_id = event_id
        self.__date = date
        self.__time = time
        self.__description = description

    @property
    def event_id(self):
        """Getter for the event ID."""
        return self.__event_id

    @property
    def date(self):
        """Getter for the event date."""
        return self.__date

    @date.setter
    def date(self, new_date):
        """Setter for the event date."""
        self.__date = new_date

    @property
    def time(self):
        """Getter for the event time."""
        return self.__time

    @time.setter
    def time(self, new_time):
        """Setter for the event time."""
        self.__time = new_time

    @property
    def description(self):
        """Getter for the event description."""
        return self.__description

    @description.setter
    def description(self, new_description):
        """Setter for the event description."""
        self.__description = new_description

    def __str__(self):
        """Provides a user-friendly string representation."""
        return f"ID: {self.event_id} | Date: {self.date} | Time: {self.time} | Desc: {self.description}"

    def __eq__(self, other):
        """Checks equality based on ID."""
        if not isinstance(other, Event):
            return False
        return self.__event_id == other.event_id