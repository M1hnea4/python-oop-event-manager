"""
Defines the validator class for Event entities.
"""
import re
from domain.event import Event
from validation.exceptions import ValidationException

class EventValidator:
    """Validates Event objects."""
    
    def validate(self, event):
        """
        Validates a given Event object.
        
        :param event: The Event object to validate.
        :return: None
        """
        errors = []
        if not event.event_id.isdigit():
            errors.append("Event ID must be a number.")

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", event.date):
            errors.append("Date must be in YYYY-MM-DD format.")

        if not re.match(r"^\d{2}:\d{2}$", event.time):
            errors.append("Time must be in HH:MM format.")

        if len(event.description.strip()) == 0:
            errors.append("Event description cannot be empty.")

        if errors:
            raise ValidationException("\n".join(errors))