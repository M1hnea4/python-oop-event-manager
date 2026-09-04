"""
Defines the repository class for Event entities.
"""
from domain.event import Event 
from repository.exceptions import RepositoryException

class EventRepository:
    """Manages the collection of Event objects in memory."""
    
    def __init__(self):
        """
        Initializes the EventRepository with an empty in-memory store.
        """
        self.__events = {}

    def add(self, event):
        """
        Adds a new event to the repository.
        
        :param event: The Event object to add.
        :return: None
        """
        if event.event_id in self.__events:
            raise RepositoryException(f"Event with ID {event.event_id} already exists.")
        self.__events[event.event_id] = event

    def delete(self, event_id):
        """
        Deletes an event by its ID.
        
        :param event_id: The ID of the event to delete.
        :return: None
        """
        if event_id not in self.__events:
            raise RepositoryException(f"Event with ID {event_id} not found.")
        del self.__events[event_id]

    def update(self, event_id, new_date, new_time, new_description):
        """
        Updates an event's details.
        
        :param event_id: The ID of the event to update.
        :param new_date: The new date for the event.
        :param new_time: The new time for the event.
        :param new_description: The new description for the event.
        :return: None
        """
        event = self.find_by_id(event_id)
        event.date = new_date
        event.time = new_time
        event.description = new_description

    def find_by_id(self, event_id):
        """
        Finds an event by its ID.
        
        :param event_id: The ID of the event to find.
        :return: The found Event object.
        """
        if event_id not in self.__events:
            raise RepositoryException(f"Event with ID {event_id} not found.")
        return self.__events[event_id]

    def get_all(self):
        """
        Returns a list of all events in the repository.
        
        :return: A list containing all Event objects.
        """
        return list(self.__events.values())

    def search_by_description(self, query):
        """
        Searches for events whose description contains the query string (case-insensitive).
        
        :param query: The search query string.
        :return: A list of matching Event objects.
        """
        query = query.lower()
        return [e for e in self.__events.values() if query in e.description.lower()]