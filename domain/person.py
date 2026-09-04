
class Person:
    """
    Represents a Person entity.
    
    Attributes:
        __person_id (str): The unique ID (CNP) of the person (private).
        __name (str): The name of the person (private).
    """
    def __init__(self, person_id, name):
        """
        Initializes a new Person instance.
        
        :param person_id: The unique ID (CNP).
        :param name: The name of the person.
        """
        self.__person_id = person_id
        self.__name = name

    @property
    def person_id(self):
        """Getter for the person's ID."""
        return self.__person_id

    @property
    def name(self):
        """Getter for the person's name."""
        return self.__name

    @name.setter
    def name(self, new_name):
        """Setter for the person's name."""
        self.__name = new_name

    def __str__(self):
        """Provides a user-friendly string representation."""
        return f"ID: {self.person_id}\nName: {self.name}\n"

    def __eq__(self, other):
        """Checks equality based on ID."""
        if not isinstance(other, Person):
            return False
        return self.__person_id == other.person_id