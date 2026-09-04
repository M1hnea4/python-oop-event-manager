"""
Defines the validator class for Person entities.
"""
from domain.person import Person
from validation.exceptions import ValidationException

class PersonValidator:
    """Validates Person objects."""
    
    def validate(self, person):
        """
        Validates a given Person object.
        
        :param person: The Person object to validate.
        :return: None
        """
        errors = []
        if not person.person_id.isdigit() or len(person.person_id) != 13:
            errors.append("Person ID (CNP) must be 13 digits.")
            
        if len(person.name.strip()) == 0:
            errors.append("Person name cannot be empty.")

        if errors:
            raise ValidationException("\n".join(errors))